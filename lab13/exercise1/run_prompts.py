import time

from openai import OpenAI

MODEL = "Qwen/Qwen3-1.7B"
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")


# Prompts are GEMINI generated
prompts = [
    "Tell me a long story about a robot.",
    "Explain quantum physics to a five year old.",
    "Write a Python script to scrape a website.",
    "What are the benefits of exercise?",
    "Summarize the history of Poland in 3 sentences.",
    "How does a internal combustion engine work?",
    "Write a poem about the moon.",
    "List 10 healthy breakfast ideas.",
    "What is the capital of France and its history?",
    "Explain the importance of biodiversity.",
]


def run_benchmark():
    start_time = time.perf_counter()

    for i, p in enumerate(prompts):
        chat_response = client.chat.completions.create(
            model="",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant."},
                {"role": "user", "content": p},
            ],
            max_completion_tokens=1000,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        )

        content = chat_response.choices[0].message.content.strip()
        print(f"\n--- Prompt {i + 1} ---")
        print(content)

    end_time = time.perf_counter()
    total_time = end_time - start_time
    print("\n--- Results ---")
    print(f"Total time for 10 prompts: {total_time:.2f} seconds")
    print(f"Average time per prompt: {total_time / 10:.2f} seconds")


if __name__ == "__main__":
    run_benchmark()
