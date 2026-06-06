from ollama import chat #LLM to generate answers(gen AI , here for text).

def generate_answer(prompt):

    response = chat(
        model="qwen3:8b",#This is the particular module that I'm using inside ollama
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]