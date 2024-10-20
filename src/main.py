import openai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")



story = """Once upon a time, there was a little restaurant that served delicious fruits. The friendly owner, Maria, decided to add some new exotic fruits to the menu to surprise her customers. She went to the market and bought some kiwis, mangos, and papayas, in addition to her usual apples, bananas, and cherries.
She quickly turned the fruits into tasty dishes. Maria made a colorful kiwi salad with a zesty lime dressing. The mango smoothie was sweet and refreshing, perfect"""

target_language = "English"
familiar_words = ["apple", "banana", "cherry"]
new_words = ["kiwi", "mango", "papaya"]
cefr = "A2"
theme = "Restaurant"


def build_prompt():
    prompt = (
        f"Write a story based on the CEFR level {cefr} and in langugae {target_language} using the following words: "
        + ", ".join(familiar_words)
        + ". Additionally, include these new or more difficult words: "
        + ", ".join(new_words)
        + ". The text should be understandable for a language learner who knows basic words but is learning more complex ones. "
        + f"The theme of the story should be {theme}."
    )
    return prompt

def main():
    prompt = build_prompt()
    print("PROMPT\n", prompt, "\n")
    openai.api_key = api_key
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )

    print("GENERATED TEXT:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()

