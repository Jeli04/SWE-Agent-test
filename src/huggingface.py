from smolagents import Tool, HfApiModel, load_tool, CodeAgent
from huggingface_hub import list_models

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

model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

agent = CodeAgent(tools=[], model=model, add_base_tools=True)
agent.tools[model_downloads_tool.name] = model_downloads_tool

# agent.run(
#     "Can you give me the name of the model that has the most downloads in the 'text-to-video' task on the Hugging Face Hub but reverse the letters?"
# )




"""
    Example 2 using git api
"""

# Example from the documentation to get most downloaded model
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
        # model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
        # return model.id
        return "Issue 100"

model_git_tool = GetLatestIssue()

model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

agent = CodeAgent(tools=[], model=model, add_base_tools=True)
agent.tools[model_git_tool.name] = model_git_tool

agent.run(
    "Can you give me latest description in the 'get_latest_issue' task?"
)