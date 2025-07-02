from chat_client.groq_client import chat_with_groq
from chat_client.together_ai import chat_with_together

def chat(prompt, backend=''):
    if backend == "groq":
        return chat_with_groq(prompt)
    elif backend == "together":
        return chat_with_together(prompt)
    else:
        return "Unknown backend"
    


user_prompt = input("Enter simple queries:\t")
chat(prompt=user_prompt, backend='groq')

