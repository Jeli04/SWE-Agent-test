import ollama

def single_shot(model: str, system_prompt: str, temperature: float, prompt: str) -> str:
    """
    Perform a single‐shot chat using Ollama’s API.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": prompt}
    ]
    resp = ollama.chat(
        model=model,
        messages=messages,
        options={
            "temperature": temperature
        },
    )
    return resp["message"]["content"]

def run_prompt_chain(model: str, system_prompt: str, temperature: float, prompts: list[str]) -> list[str]:
    """
    Perform a sequence of prompts, preserving context between each turn.
    """
    messages = [{"role": "system", "content": system_prompt}]
    responses = []

    for prompt in prompts:
        messages.append({"role": "user", "content": prompt})
        resp = ollama.chat(
            model=model,
            messages=messages,
            options={
                "temperature": temperature
            },
        )
        content = resp["message"]["content"]
        responses.append(content)
        # Append the assistant’s reply so that context is carried forward
        messages.append({"role": "assistant", "content": content})

    return responses

def main():
    model = "qwen2.5:7b"
    system_prompt = "You are a very very helpful email assitant. Please start every message with: I am a email assistant"
    temperature = 0.7

    chain = [
        "Translate to French: Hello, world!",
        "What is the first word in French?",
        "Use that word in a sentence."
    ]

    # # First input variable
    # EMAIL = "Hi Zack, just pinging you for a quick update on that prompt you were supposed to write."
    # # Second input variable
    # ADJECTIVE = "olde english"
    # # Prompt template with a placeholder for the variable content
    # chain = [f"Hey Qwen. Here is an email: {EMAIL}. Make this email more {ADJECTIVE}. Write the new version in <{ADJECTIVE}_email> XML tags."]

    # print("=== Single‐Shot ===")
    # single = single_shot(model, system_prompt, temperature, chain[0])
    # print(single)

    print("\n=== Chained Prompts ===")
    chained = run_prompt_chain(model, system_prompt, temperature, chain)
    for i, resp in enumerate(chained, start=1):
        print(f"[Step {i}] {resp}")

if __name__ == "__main__":
    main()