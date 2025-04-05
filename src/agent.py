"""
    Ignore this file for now. It is only for testing purposes.
"""

import ollama_tool
import re
# from src.utils import *
from github import get_github_issue

class Agent():
    def __init__(self, config):
        # TODO add config parsing code

        self.model = "llama3"
        self.client = ollama_tool.Client()

    # temp function only for testing
    def parse(self, query):
        thought_pattern = r"THOUGHT:\s*(.?)\sACTION:"
        thought_match = re.search(thought_pattern, query, re.DOTALL)
        if thought_match:
            thought_text = thought_match.group(1).strip()
        else:
            thought_text = ""

        action_pattern = r"ACTION:\s*(.*)"
        action_match = re.search(action_pattern, query, re.DOTALL)
        if action_match:
            action_text = action_match.group(1).strip()
        else:
            action_text = ""

        output_dict = {
            "thought": thought_text,
            "action": action_text,
        }

        return output_dict

    def request(self, query):
        response = ollama_tool.chat(model=self.model, messages=[{"role": "user", "content": query}])
        print(response['message']['content'])
        output_dict = self.parse(response['message']['content'])

        print(output_dict)


if __name__ == "__main__":
    agent = Agent(None)

    owner = "Jeli04"
    repo = "SWE-Agent-test"
    issue_number = 3

    # Retrieve the issue details
    issue_details = get_github_issue(owner, repo, issue_number)
    issue_title = issue_details.get("title", "").strip()
    issue_body = issue_details['body']
    print("Issue Title:", issue_title)
    print("Issue Details:", issue_body)


    prompt = f"""
    You are an AI software engineer. Given the following GitHub issue, write the raw code to solve the issue. 
    After writing the code add "complete" if the issue is completely solved. 

    GitHub Issue:
    {issue_body}
        """

    agent.request(prompt)





    query = """
        GitHub Issue:

        Create an issue called "Hello World" to be created in Python

        THOUGHT:
        The issue is asking for the creation of a simple "Hello World" program in Python, which is a classic introduction to programming. The issue doesn't provide any specific requirements or constraints, so we can assume it's a straightforward task.

        ACTION:

        Here's a suggested code edit:

        ```python
        print("Hello, World!")
        ```

        This is a simple Python script that prints the string "Hello, World!" to the console. It's a classic example of a "Hello World" program and should meet the requirements specified in the issue.
    """
    
    # thought_pattern = r"THOUGHT:\s*(.+?)\s*ACTION:"
    # thought_match = re.search(thought_pattern, query, re.DOTALL)
    # if thought_match:
    #     thought_text = thought_match.group(1).strip()
    # else:
    #     thought_text = ""
    # print(thought_text)