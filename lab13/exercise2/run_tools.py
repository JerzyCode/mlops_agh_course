import json
from typing import Callable

import pandas as pd
import requests
from openai import OpenAI


def make_llm_request(prompt: str) -> str:
    client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

    messages = [
        {"role": "developer", "content": "You are a datasets analyzer."},
        {"role": "user", "content": prompt},
    ]

    tool_definitions, tool_name_to_func = get_tool_definitions()

    for _ in range(10):
        response = client.chat.completions.create(
            model="",
            messages=messages,
            tools=tool_definitions,
            tool_choice="auto",
            max_completion_tokens=1000,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        )
        resp_message = response.choices[0].message
        messages.append(resp_message.model_dump())

        print(f"Generated message: {resp_message.model_dump()}")
        print()

        if resp_message.tool_calls:
            for tool_call in resp_message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                func = tool_name_to_func[func_name]
                func_result = func(**func_args)

                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(func_result),
                        "tool_call_id": tool_call.id,
                    }
                )
        else:
            return resp_message.content

    last_response = resp_message.content
    return f"Could not resolve request, last response: {last_response}"


def get_tool_definitions() -> tuple[list[dict], dict[str, Callable]]:
    tool_definitions = [
        {
            "type": "function",
            "function": {
                "name": "get_apis_tox_dataset_info",
                "description": "Get information about APIs Tox dataset.",
                "parameters": {},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_apis_tox_dataset_csv",
                "description": 'Get the "APIs Tox" dataset as a CSV string.',
                "parameters": {},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_new_york_taxi_dataset_csv",
                "description": "Get New York taxi dataset as a CSV string.",
                "parameters": {},
            },
        },
    ]

    tool_name_to_callable = {
        "get_apis_tox_dataset_info": get_apis_tox_dataset_info,
        "get_apis_tox_dataset_csv": get_apis_tox_dataset_csv,
        "get_new_york_taxi_dataset_csv": get_new_york_taxi_dataset_csv,
    }

    return tool_definitions, tool_name_to_callable


def get_apis_tox_dataset_info() -> str:
    url = (
        "https://raw.githubusercontent.com/j-adamczyk/ApisTox_dataset/master/README.md"
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_apis_tox_dataset_csv() -> str:
    url = "https://raw.githubusercontent.com/j-adamczyk/ApisTox_dataset/master/outputs/dataset_final.csv"
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_new_york_taxi_dataset_csv() -> str:
    df = pd.read_parquet("taxi_data.parquet", engine="pyarrow")
    return df.head(20).to_csv(index=False)


if __name__ == "__main__":
    # prompt = "What is included in the APIs Tox dataset?"
    # response = make_llm_request(prompt)
    # print("Response:\n", response)

    # prompt = "What is SMILES of Ethanedioic acid and Calcium carbonate?"  # O=C(O)C(=O)O	 and O=C([O-])[O-].[Ca+2]
    # response = make_llm_request(prompt)
    # print("Response:\n", response)

    # print()

    prompt = "What are the columns of taxi dataset?"
    response = make_llm_request(prompt)
    print("Response:\n", response)
