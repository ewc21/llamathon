from llama_stack_client import LlamaStackClient

client = LlamaStackClient(base_url="http://localhost:8321")

def call_llama_for_nutrition(user_input: str) -> str:
    models = client.models.list()
    model_id = next(m for m in models if m.model_type == "llm").identifier

    response = client.inference.chat_completion(
        model_id=model_id,
        messages=[
            {"role": "system", "content": "You are a nutrition assistant. Given a user's meal, return food items and their nutrition facts in JSON."},
            {"role": "user", "content": user_input},
        ],
    )
    return response.completion_message.content
