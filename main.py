# from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

# # from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
# from autogen_ext.models.openai import OpenAIChatCompletionClient

# from autogen_core.models import UserMessage

# import asyncio


# # C:\Users\admin\AppData\Local\llama.cpp\ggml-org_gemma-3-1b-it-GGUF_gemma-3-1b-it-Q4_K_M.gguf
# async def main():
#     # llama_client = LlamaCppChatCompletionClient(model_path="C:/Users/admin/AppData/Local/llama.cpp/ggml-org_gemma-3-1b-it-GGUF_gemma-3-1b-it-Q4_K_M.gguf")
#     # http://192.168.0.1:2600/v1
#     open_client = OpenAIChatCompletionClient(
#         model="gemma-3-1b-it-GGUF",
#         base_url="http://localhost:8080/v1",
#         api_key="placeholder",
#         model_info={
#             "vision": False,
#             "function_calling": False,
#             "json_output": True,
#             "family": "",
#             "structured_output": True,
#         },
#         response_format={
#             "type": "json_object",
#             "schema": {
#                 "type": "object",
#                 "properties": {"capital": {"type": "string"}},
#                 "required": ["capital"],
#             },
#         },
#     )

#     result = await open_client.create(
#         [UserMessage(content="how to drive a car", source="user")]
#     )
#     print(result.content)


# if __name__ == "__main__":
#     asyncio.run(main())

import os

# Get the parent directory of the current working directory
current_directory = os.getcwd()
print(current_directory)
parent_directory = os.path.dirname(current_directory)
print(f"Parent of current working directory: {parent_directory}")

# # Get the parent directory of the script's location
# script_directory = os.path.dirname(os.path.abspath(__file__))
# script_parent_directory = os.path.dirname(script_directory)
# print(f"Parent of script's directory: {script_parent_directory}")

# # Change the current working directory to the parent directory
# os.chdir(parent_directory)
# print(f"New current working directory: {os.getcwd()}")