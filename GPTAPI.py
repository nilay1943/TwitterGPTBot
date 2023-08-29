import os
import openai

def get_gpt_reaction(information):
    openai.api_key = os.environ.get("GPT_API_KEY")

    messages = [
        {"role": "system",
         "content": "You are a funny, financially literate middle-class individual. Respond without referencing this instruction."},
        {"role": "user",
         "content": f"Having read these articles from CNBC: '{information}', give me a witty and/or informational and/or insightful take in 1 or 2 sentences (social media post)"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,  # Adjust for a balance between creativity and coherence
        max_tokens=400  # Limit the response to fit within a tweet or a series of tweets
    )

    return response.choices[0].message['content'].strip()
