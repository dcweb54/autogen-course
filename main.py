# from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

# # from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
# from autogen_ext.models.openai import OpenAIChatCompletionClient

# from autogen_core.models import UserMessage

# import asyncio


# # # C:\Users\admin\AppData\Local\llama.cpp\ggml-org_gemma-3-1b-it-GGUF_gemma-3-1b-it-Q4_K_M.gguf
# async def main():
#     # llama_client = LlamaCppChatCompletionClient(model_path="C:/Users/admin/AppData/Local/llama.cpp/ggml-org_gemma-3-1b-it-GGUF_gemma-3-1b-it-Q4_K_M.gguf")
#     # http://192.168.0.1:2600/v1
#     open_client = OpenAIChatCompletionClient(
#         model="llama3.1:latest",
#         base_url="https://dashing-mosquito-dominant.ngrok-free.app/v1",
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
#         [UserMessage(content="what is the capital of india", source="user")]
#     )
#     print(result.content)


# if __name__ == "__main__":
#     asyncio.run(main())

import os
from pathlib import Path

# from ollama import chat
from ollama import ChatResponse
from ollama import Client
import base64
import json
import shutil

from pydantic import BaseModel

# class Country(BaseModel):
#   name: str

client = Client(
    host="https://9mftdz9lkul9.share.zrok.io"
    #   host='https://dashing-mosquito-dominant.ngrok-free.app',
    # headers={'x-some-header': 'some-value'}
)




def extract_img(img: str):
    # img = os.path.join(os.getcwd(), "4475.png")

    img = Path(img).read_bytes()

    response: ChatResponse = client.chat(
        model="qwen2.5vl:3b",
        messages=[
            {"role": "user", "content": "extract text", "images": [img]},
        ],
        format="json",
    )
    data = json.loads(response["message"]["content"])
    print(data["text"])
    return data["text"]
    # or access fields directly from the response object
    # print(response.message.content)


def rename_file(img: str):
    file_name = extract_img(img=img)
    for x in os.listdir('cap-r'):
        if file_name in x:
            print("file exist")
            print("skip the copy")
        else:
            print("if not exist then create new file")
            shutil.copy(img, os.path.join('cap-r',f"{file_name}.png"))
    # os.rename(img, os.path.join('cap-r',f"{file_name}.png"))


img_paths = [os.path.join("cap-1", x) for x in os.listdir("cap-1")]
for x in img_paths:
  rename_file(img=x)
# text_sample = "9gzsr"
# print(os.listdir('cap-r'))




# Get the parent directory of the current working directory
# current_directory = os.getcwd()
# print(current_directory)
# parent_directory = os.path.dirname(current_directory)
# print(f"Parent of current working directory: {parent_directory}")

# # Get the parent directory of the script's location
# script_directory = os.path.dirname(os.path.abspath(__file__))
# script_parent_directory = os.path.dirname(script_directory)
# print(f"Parent of script's directory: {script_parent_directory}")

# # Change the current working directory to the parent directory
# os.chdir(parent_directory)
# print(f"New current working directory: {os.getcwd()}")
