# %%
import json
import os

from agent_prompts import customer_sys_prompt, support_agent_sys_prompt
from autogen import ConversableAgent
from dotenv import load_dotenv

load_dotenv()

# %%
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "price": [0.000150, 0.000600],
            "cache_seed": None,
        }
    ]
}


# %%
def create_agent(
    name: str,
    sys_prompt: str,
    human_input_mode: str,
    termination_msg: str | None = None,
):
    return ConversableAgent(
        name=name,
        system_message=sys_prompt,
        is_termination_msg=lambda msg: termination_msg in msg["content"]
        if termination_msg
        else None,
        human_input_mode=human_input_mode,
        llm_config=llm_config,
    )


# %%
def process_queries(queries: dict[str, str | list[str]]):
    guidelines = queries["guidelines"]
    f = open("convo.txt", "a")
    for i, query in enumerate(queries["customer_queries"]):
        if i == 3:
            break
        customer_agent = create_agent(
            "Customer",
            customer_sys_prompt.format(guidelines=guidelines),
            "NEVER",
            "RESOLVED",
        )
        support_agent = create_agent(
            "Support_Agent", support_agent_sys_prompt, "NEVER", "RESOLVED"
        )
        chat_result = customer_agent.initiate_chat(support_agent, message=query)
        print(chat_result.chat_history, file=f)
        f.write("\n\n")
    f.close()


# %%
with open("../query_gen/queries.jsonl", "r") as f:
    for line in f:
        queries: dict = json.loads(line)
        process_queries(queries)
        break

# customer_agent = create_agent("Customer", customer_sys_prompt, "NEVER", "RESOLVED")
# support_agent = create_agent(
#     "Support_Agent", support_agent_sys_prompt, "NEVER", "RESOLVED"
# )
# chat_result = customer_agent.initiate_chat(
#     support_agent,
#     message="how da fuck do knoe if i can exchange my product in my city? y'all have not even put up proper instructions",
# )


# %%
print(chat_result.cost)
