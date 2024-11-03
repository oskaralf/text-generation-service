from src.services.get_text_for_user import get_text_from_openai

assistant_text = ()


async def get_calibration_text():
    messages = [
        {"role": "system", "content": assistant_text},
        {"role": "user", "content": ""}
    ]
    generated_text = get_text_from_openai(messages)
    