from importlib import import_module
import os
import json


def read_model_config():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE_DIR, "../models_registry.json"), "r") as f:
        MODEL_REGISTRY = json.load(f)
        return MODEL_REGISTRY
    
MODEL_REGISTRY = read_model_config()

def get_model_handler(model_id):
    model_info = MODEL_REGISTRY[model_id]
    module = import_module(model_info["module"])
    func = getattr(module, model_info["function"])
    return func

