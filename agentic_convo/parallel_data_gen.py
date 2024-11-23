import argparse
import asyncio
import time
import json
import os
import re
from itertools import islice

from agent_prompts import customer_sys_prompt, support_agent_sys_prompt
from autogen import ConversableAgent
from dotenv import load_dotenv
import aiofiles
from asyncio import Semaphore

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="Input query file to process.", required=True)
parser.add_argument("--output_file", help="Output file to write the conversations to.", required=True)
parser.add_argument("--parallel_batches", type=int, default=2, help="Number of query batches to process in parallel.")
args = parser.parse_args()

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "cache_seed": None,
        }
    ]
}


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
        silent=True
    )


async def process_batch(queries: dict, guidelines: str) -> list:
    """Processes a batch of queries concurrently."""

    async def process_single_query(query: str) -> dict:
        try:
            # "RESOLVED" is passed as the termination argument.
            # this works in both cases where the LLM outputs RESOLVED or UNRESOLVED
            customer_agent = create_agent(
                "Customer",
                customer_sys_prompt.format(
                    tone=queries.get("tone", ""),
                    style=queries.get("style", "")
                ),
                "NEVER",
                "RESOLVED",
            )
            support_agent = create_agent(
                "Support_Agent", support_agent_sys_prompt.format(guidelines=guidelines), "NEVER", "RESOLVED"
            )

            # remove number at the start if present
            cleaned_query = re.sub(r"^\d+\.\s*", "", query)

            chat_result = await customer_agent.a_initiate_chat(support_agent, message=cleaned_query)

            out_json = {
                "title": queries.get("title", ""),
                "tone": queries.get("tone", ""),
                "style": queries.get("style", ""),
                "conversation": chat_result.chat_history,
                "length": len(chat_result.chat_history),
                "status": "UNRESOLVED" if "UNRESOLVED" in chat_result.chat_history[-1]["content"]\
                          else "RESOLVED"
            }
            return out_json

        except Exception as e:
            return {
                "title": queries.get("title", ""),
                "tone": queries.get("tone", ""),
                "style": queries.get("style", ""),
                "conversation": [],
                "length": 0,
                "status": "ERROR",
                "error": str(e)
            }

    # process all queries concurrently within the batch
    tasks = [process_single_query(query) for query in queries.get("customer_queries", [])]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # prepare final results
    processed_results = []
    for result in results:
        if isinstance(result, Exception):
            # Log the exception or handle it as needed
            processed_results.append({
                "title": queries.get("title", ""),
                "tone": queries.get("tone", ""),
                "style": queries.get("style", ""),
                "conversation": [],
                "length": 0,
                "status": "ERROR",
                "error": str(result)
            })
        else:
            processed_results.append(result)

    return processed_results


async def async_batch_reader(file, batch_size):
    """Asynchronous generator to read the file in batches."""
    batch = []
    async for line in file:
        line = line.strip()
        if line:
            batch.append(line)
            if len(batch) == batch_size:
                yield batch
                batch = []
    if batch:
        yield batch


async def process_query_file(inp_file_str: str, out_file_str: str, parallel_batches: int = 2):
    semaphore = Semaphore(parallel_batches)  # Limit the number of concurrent batches

    async with aiofiles.open(inp_file_str, 'r') as inp_file, \
               aiofiles.open(out_file_str, 'a') as out_file:
        i = 1
        # it is possible to iterate over normal sync IOTextWrapper and not async iotextwrapper that is created by aiofiles.
        # hence async batch reader is used.
        async for batch_set in async_batch_reader(inp_file, parallel_batches):
            print(f"Processing batch set {i}.")
            start = time.time()

            # define a coroutine for processing each batch within the semaphore
            async def sem_process(queries_str):
                async with semaphore:
                    try:
                        queries = json.loads(queries_str)
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")
                        return [{
                            "title": "",
                            "tone": "",
                            "style": "",
                            "conversation": [],
                            "length": 0,
                            "status": "ERROR",
                            "error": f"JSON decode error: {e}"
                        }]

                    title = queries.get('title', 'default')
                    guidelines_path = f"/home/suchitg/amazon_help/leafdirs/{title}/t.txt"
                    try:
                        async with aiofiles.open(guidelines_path, 'r') as g_file:
                            guidelines = await g_file.read()
                    except Exception as e:
                        guidelines = ""
                        print(f"Error reading guidelines for title '{title}': {e}")

                    return await process_batch(queries, guidelines)

            # dreate tasks for the current set of batches
            tasks = [sem_process(qs) for qs in batch_set]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            # persist results to the output file
            for batch_result in batch_results:
                if isinstance(batch_result, Exception):
                    # Handle the exception or log it
                    error_json = {
                        "title": "",
                        "tone": "",
                        "style": "",
                        "conversation": [],
                        "length": 0,
                        "status": "ERROR",
                        "error": str(batch_result)
                    }
                    await out_file.write(json.dumps(error_json, ensure_ascii=False) + "\n")
                else:
                    for result in batch_result:
                        await out_file.write(json.dumps(result, ensure_ascii=False) + "\n")

            await out_file.flush()
            end = time.time()
            print(f"Time taken for batch set {i}: {end - start:.2f} sec(s)")
            i += 1

        print(f"Finished generation for file: {inp_file_str}")


def main():
    asyncio.run(process_query_file(args.input_file, args.output_file, args.parallel_batches))


if __name__ == "__main__":
    main()
