from openai import OpenAI

# those settings use vLLM server
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

chat_response = client.chat.completions.create(
    model="",  # use the default server model
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How important is LLMOps on scale 0-10? "},
    ],
    max_completion_tokens=1000,
    # turn off thinking for Qwen with /no_think
    extra_body={"chat_template_kwargs": {"enable_thinking": False}},
)
content = chat_response.choices[0].message.content.strip()
print("Response:\n", content)
