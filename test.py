import os
import openai
from openai import AsyncAzureOpenAI
import asyncio
from dotenv import load_dotenv
import time
load_dotenv()
API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
deployment_name = "gpt4o"

client = AsyncAzureOpenAI(
  api_key = API_KEY,  
  api_version = "2024-09-01-preview",
  azure_endpoint = RESOURCE_ENDPOINT
)


async def request(messages):
    print("start")
    print(time.strftime("%X"))
    response = await client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=0.2,
    )
    print("finish")
    print(time.strftime("%X"))
    return response.choices[0].message.content


message1 = [{"role": "user","content":"hello"}]
message2 = [{"role": "user","content":"haha"}]

async def main():
    response = await asyncio.gather(request(message1),request(message2))
    return response

result = asyncio.run(main())
print(result)
