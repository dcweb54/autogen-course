# from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
# from autogen_core.models import UserMessage

# import asyncio

# async def main():
#     llama_client = LlamaCppChatCompletionClient(
#         repo_id="unsloth/phi-4-GGUF", filename="phi-4-Q2_K_L.gguf", n_gpu_layers=-1, seed=1337, n_ctx=5000
#     )
#     result = await llama_client.create([UserMessage(content="What is the capital of France?", source="user")])
#     print(result)


# asyncio.run(main())
