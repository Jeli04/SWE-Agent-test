from smolagents import Tool, HfApiModel, load_tool, CodeAgent, TransformersModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import list_models
from github import get_github_issue, get_issue_count

"""
    Example 1 from the documentation
"""

# Example from the documentation to get most downloaded model
class HFModelDownloadsTool(Tool):
    name = "model_download_counter"
    description = """
    This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub.
    It returns the name of the checkpoint."""
    inputs = {
        "task": {
            "type": "string",
            "description": "the task category (such as text-classification, depth-estimation, etc)",
        }
    }
    output_type = "string"

    def forward(self, task: str):
        model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
        print("task: ", task)
        return model.id

model_downloads_tool = HFModelDownloadsTool()

# model_name = "Qwen/Qwen2.5-7B-Instruct"  # Replace with the local model you want to use
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)
# model = HfApiModel(model_id="Qwen/Qwen2.5-7B-Instruct")   # API Inference call for Qwen, you can replace with another model as well
model = TransformersModel(model_id="HuggingFaceTB/SmolLM-135M-Instruct", max_new_tokens=512)    # very small model provided by HF
agent = CodeAgent(tools=[], model=model, add_base_tools=True)
agent.tools[model_downloads_tool.name] = model_downloads_tool

# you can comment this if you just want to test example 2
agent.run(
    "Can you give me the name of the model that has the most downloads in the 'text-to-video' task on the Hugging Face Hub but reverse the letters?"
)



"""
    Example 2 using git api
"""

# Create a Tool using the GitHub functions 
class GetLatestIssue(Tool):
    name = "get_latest_issue"
    description = """
    This is a tool that returns the latest issue on a Github repo.
    It returns the description of the issue."""
    inputs = {
        "task": {
            "type": "string",
            "description": "issue",
        }
    }
    output_type = "string"

    def forward(self, task: str):
        issue_count = get_issue_count(owner="Jeli04", repo="SWE-Agent-test")    
        issue_details = get_github_issue(owner="Jeli04", repo="SWE-Agent-test", issue_number=issue_count)
        return issue_details['body']

model_git_tool = GetLatestIssue()

agent = CodeAgent(tools=[], model=model, add_base_tools=True)
agent.tools[model_git_tool.name] = model_git_tool

agent.run(
    "Can you give me latest description in the 'get_latest_issue' task?"
)