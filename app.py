print("Hello world!")

from functions import input_prompt

print("This is my AI agent application.")

input = "Explain how AI works in a lotta words but in girly pop terms"
model = "gemini-3.8-flash"
# model = "gemini-3.5-flash-lite"

print("Input entered as prompt: ",input)
print("Model selected: ",model)
print("\n")

output_response = input_prompt(input, model, logging_on=True)
print("\n\nReturning output from Gemini API: \n","*"*100,"\n\n",output_response)

