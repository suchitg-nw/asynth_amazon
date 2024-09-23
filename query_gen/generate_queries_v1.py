# %%
import json
import os
import re
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
    guidelines = open(f"/home/suchitg/amazon_help/leafdirs/{intent}/t.txt", "r").read()
    usr_prompts.append(
        f"""{{
    "title": "{intent}",
    "content": '''{guidelines}\n'''
}}"""
    )


@cache
def get_query(usr_prompt: str):
    """Generate customer queries for the given intent and its guidelines."""
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
def remove_numbers(queries_obj: dict):
    """Remove numbers from the start of the queries."""
    updated = {
        k: [re.sub(r"^\d+\.\s", "", i) for i in v]
        for k, v in queries_obj.items()
        if k == "customer_queries"
    }
    queries_obj["customer_queries"] = updated["customer_queries"]


with open("./queries.jsonl", "a") as f:
    for prompt in usr_prompts:
        res = get_query(prompt)
        queries_obj = json.loads(res)
        queries_obj["tone"] = "neutral"
        remove_numbers(queries_obj)
        json.dump(queries_obj, f)
        f.write("\n")


# %%
