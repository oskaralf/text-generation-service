from src.models.languages import Language
from src.services.get_text_for_user import get_text_from_openai

assistant_text = ("You are a helpful assistant for people learning a new language. "
                  "I will provide you a context that a user is interested in interested reading a text about "
                  "and you will give me a list of text types that would be suitable for that context. "
                  "Please only answer with a list of text types separated with commas and absolutely nothing else. "
                  "Example: News article, Blog post, Short story, Poem, Recipe, Conversation...")


async def get_text_types_from_context(context: str):
    messages = [
        {"role": "system", "content": assistant_text},
        {"role": "user", "content": context}
    ]
    generated_text_types = get_text_from_openai(messages)
    generated_text_types = generated_text_types.split(',')
    print(generated_text_types)
    return generated_text_types
