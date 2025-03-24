import ollama
import re
# from src.utils import *

class Agent():
    def __init__(self, config):
        # TODO add config parsing code

        self.model = "llama3"
        self.client = ollama.Client()

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
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": query}])
        print(response['message']['content'])
        output_dict = self.parse(response['message']['content'])

        print(output_dict)


if __name__ == "__main__":
    agent = Agent(None)

    issue_description = "Create an issue called Hello World to be created in Python"

    prompt = f"""
    You are an AI software engineer. Given the following GitHub issue, propose a fix in the following format:
    THOUGHT: Explain your reasoning.
    ACTION: Suggest a code edit.
    GitHub Issue:
    {issue_description}
        """

    # agent.request(prompt)

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
    
    thought_pattern = r"THOUGHT:\s*(.+?)\s*ACTION:"
    thought_match = re.search(thought_pattern, query, re.DOTALL)
    if thought_match:
        thought_text = thought_match.group(1).strip()
    else:
        thought_text = ""
    print(thought_text)