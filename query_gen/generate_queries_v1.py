# %%
import json
import os
from functools import cache

from dotenv import load_dotenv
from openai import OpenAI
from prompts import sys_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

intents = ["AboutExchanges", "DamagedDefectiveOrWrongProductFAQ"]

# %%
usr_prompts = []
for intent in intents:
    sample_guidelines = open(
        f"/home/suchitg/amazon_help/leafdirs/{intent}/t.txt", "r"
    ).read()
    usr_prompts.append(
        f"""{{
    "title": "{intent}",
    "content": '''{sample_guidelines}\n'''
}}"""
    )

print(usr_prompts[1], file=open("test.txt", "w"))


@cache
def get_query(usr_prompt: str):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": usr_prompt},
        ],
        response_format={"type": "json_object"},
    )
    return res.choices[0].message.content


# %%
with open("./queries.jsonl", "a") as f:
    for prompt in usr_prompts:
        res = get_query(prompt)
        queries_obj = json.loads(res)
        queries_obj["guidelines"] = open(
            f"/home/suchitg/amazon_help/leafdirs/{queries_obj['title']}/t.txt"
        ).read()
        json.dump(queries_obj, f)
        f.write("\n")


# %%
print(
    open(
        f"/home/suchitg/amazon_help/leafdirs/DamagedDefectiveOrWrongProductFAQ/t.txt",
        "r",
    ).read()
)
