from importlib import import_module
import os
import json
import requests
from dotenv import load_dotenv


load_dotenv()
TOGETHER_API_KEY = os.getenv("together-api")
TOGETHER_BASE_URL = os.getenv("together-url")


def read_model_config():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE_DIR, "../models_registry.json"), "r") as f:
        MODEL_REGISTRY = json.load(f)
        return MODEL_REGISTRY
    
MODEL_REGISTRY = read_model_config()

# def get_model_handler(model_id):
#     model_info = MODEL_REGISTRY[model_id]
#     module = import_module(model_info["module"])
#     func = getattr(module, model_info["function"])
#     return func

def get_model_handler(model_key):
    model_config = MODEL_REGISTRY.get(model_key)

    if not model_config:
        raise ValueError("Invalid model key.")

    def handler(prompt: str):
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_config["id"],
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
        }

        response = requests.post(TOGETHER_BASE_URL, json=payload, headers=headers)
        result = response.json()

        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"]
        else:
            return "⚠️ No response received from the model."

    return handler



