import ollama 
import json
import requests
from rich import print
import time
import os
import logging
import sys
sys.path.append("/Users/jerryli/Desktop/python/SWE-Agent-test/ollama-tools")
from ollama_tools import generate_function_description, use_tools
from github import stage_and_commit_files, get_issue_count, get_github_issue, create_github_issue, close_github_issue, merge_github_branch, close_github_pull_request, get_pr_count, get_github_pr, create_pull_request, total_prs, create_new_branch, fetch_commit_history, fetch_files_from_codebase, edit_files_from_codebase, create_file
from shell_exec import run_command, open_subprocess, retrieve_subprocess_output

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

tools = [
    generate_function_description(stage_and_commit_files),
    generate_function_description(get_issue_count),
    generate_function_description(get_github_issue),
    generate_function_description(create_github_issue),
    generate_function_description(close_github_issue),
    generate_function_description(merge_github_branch),
    generate_function_description(close_github_pull_request),
    generate_function_description(get_pr_count),
    generate_function_description(get_github_pr),
    generate_function_description(create_pull_request),
    generate_function_description(total_prs),
    generate_function_description(create_new_branch),
    generate_function_description(fetch_commit_history),
    generate_function_description(fetch_files_from_codebase),
    generate_function_description(edit_files_from_codebase),
    generate_function_description(run_command),
    generate_function_description(open_subprocess),
    generate_function_description(retrieve_subprocess_output),
    generate_function_description(create_file),
]

logging.debug("Tools:")
logging.debug(json.dumps(tools, indent=4))
functions_desc = [ f["function"]["description"] for f in tools ]
print("I am a chatbot able to do run some functions.", "Functions:\n\t",  "\n\t".join(functions_desc))
functions = {function["function"]["name"]: globals()[function["function"]["name"]] for function in tools }

# Sets up the Ollama system prompt for the model
messages = [('system', "You are an assistant with access to tools, if you do not have a tool to deal with the user's request but you think you can answer do it so, if not explain your capabilities")]
while True:
    try:
        query = input()
    except EOFError:
        break
    if query == "quit":
        break
    if query.strip() == "":
        continue
    messages.append(("user", query))
    response = ollama.chat(
        model='qwen2.5:7b',
        messages=[ {'role': role, 'content': content} for role,content in messages ],
        tools=tools,
    )

    if response['message']['content'] == "":
        tools_calls = response['message']['tool_calls']
        logging.debug(tools_calls)  # runs the actual functions in your local environment
        result = use_tools(tools_calls, functions)
    else:
        result = response['message']['content']
    print(result)
    messages.append(("assistant", result))






# # define the tool that we want
# get_stock_price_tool = {
#     'type': 'function',
#     'function': {
#         'name': 'get_issue_count',
#         'description': 'Gets the number of issues in a GitHub repository',
#         'parameters': {
#             'type': 'object',
#             'required': ['owner', 'repo'],
#             'properties': {
#                 'owner': {'type': 'string', 'description': 'The owner of the GitHub repository'},
#                 'repo': {'type': 'string', 'description': 'The name of the GitHub repository'},
#             },
#         },
#     },
# }

# response = ollama.chat(
#     model="qwen2.5:7b",
#     messages=[
#         {"role": "user", "content": "Please tell me the number of issues in the GitHub repository 'Jeli04/SWE-Agent-test' where the owner is Jeli04."},
#     ],
#     tools=[get_stock_price_tool],
# )
# print(response['message'])
# print(response['message']['tool_calls']) 