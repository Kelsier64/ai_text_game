import math
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Tuple
import asyncio
from openai import AzureOpenAI
from dotenv import load_dotenv
import os,json
import prompt
load_dotenv()
API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
deployment_name = "gpt4o"

client = AzureOpenAI(
  api_key = API_KEY,  
  api_version = "2024-09-01-preview",
  azure_endpoint = RESOURCE_ENDPOINT
)

def json_request(messages):
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)



messages = [{"role": "user","content":"give me 5 sentence in 5 json:{'sentence1':''} {'sentence2':''}"}]

print(json_request(messages))
