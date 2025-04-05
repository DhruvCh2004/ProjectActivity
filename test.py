import google.generativeai as genai

genai.configure(api_key="AIzaSyBYw6v2wWuIxVab3xDba53Hl_nRD0BDTlE")
models = genai.list_models()
for model in models:
    print(model.name, model.supported_generation_methods)
