print("Hello world!")

import os

from functions import input_prompt, stream_prompt

print("This is my AI agent application.")

prompt = "Explain how AI works in a lotta words but in girly pop terms"
model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

print("Input entered as prompt: ", prompt)
print("Model selected: ", model)
print("\n")

try:
    print("\n--- normal return mode ---")
    output_response = input_prompt(prompt, model=model, logging_on=False)
    print("\nFinal returned text:")
    print(output_response)

    # print("\n--- streaming print mode ---")
    # stream_prompt(prompt, model=model, logging_on=False)
except Exception as exc:
    print(f"\n\nError: {exc}")

