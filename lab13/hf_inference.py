import torch.cuda
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_name = "Qwen/Qwen3-1.7B"

# use half-precision inference and GPU if available
# dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float16
dtype = torch.float16
# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, dtype=dtype, device_map=device)


def inference():
    # prepare the model input
    prompt = "How important is LLMOps on scale 0-10?"
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True,  # use thinking / reasoning?
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # conduct text completion
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=32768,  # if not provided, use max context 32k
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]) :].tolist()

    # parse only output, not thinking content
    try:
        # find token 151668 "</think>"
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
    print("Answer:\n", content)


def inference_simplified():
    model = pipeline(
        task="text-generation",
        model="Qwen/Qwen3-1.7B",
        dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float16,
        device="cuda" if torch.cuda.is_available() else "cpu",
    )

    prompt = "How important is LLMOps on scale 0-10?"
    messages = [{"role": "user", "content": prompt}]

    messages = model(messages, max_new_tokens=32768)[0]["generated_text"]
    content = messages[-1]["content"].strip()
    print("Answer:\n", content)


if __name__ == "__main__":
    print("Inference with low-level API:")
    inference()
    # print("\nInference with pipeline API:")
    # inference_simplified()
