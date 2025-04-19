from llama_stack import prompt

@prompt("parse_meal", template_file="prompts/parse_meal_items.txt")
async def parse_meal_items(user_input: str):
    return {"input": user_input}

async def handle_chat(user_input: str):
    structured = await parse_meal_items(user_input)
    return structured
