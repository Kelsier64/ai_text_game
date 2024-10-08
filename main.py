import os
import json
import openai
from openai import AzureOpenAI
import time
API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
deployment_name = "gpt4o"

client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = "2024-09-01-preview",
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)

def json_request(messages, max_tokens):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except:
        return "error"
    
def str_request(messages, max_tokens):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2
        )
        return response.choices[0].message.content
    except:
        return "error"
    
class Character:
    def __init__(self, name, age, gender, location,position, personality, mental_state, physical_conditions,long_term_memory,short_term_memory):
        self.name = name
        self.age = age
        self.gender = gender

        self.hunger = 100
        self.location = location
        self.position = position
        self.facial_expression = "not set"
        self.doing = "sleep"
        self.concertration = 0

        self.personality = personality
        self.mental_state = mental_state
        self.physical_conditions = physical_conditions
        self.external_conditions = {}
        self.mood = "not set"
        self.long_term_memory = long_term_memory
        self.short_term_memory = short_term_memory
        self.temp_memory = {}
    def update(self,name=None,age=None,gender=None, location=None,position=None, personality=None, mental_state=None, physical_conditions=None,long_term_memory=None,short_term_memory=None):
        for key,value in locals().items():
            if key != "self" and value is not None:
                setattr(self,key,value)

    def __str__(self):
        return f"Character(name={self.name}, age={self.age}, gender={self.gender}, position={self.position})"

sys_prompt={"role": "user","content":"Forget all previous settings. Below is your character information. Please generate responses based on your own character profile and instruction"}

def reflection(character):
    
    profile=f"""
"Here is your character data:

Memory details:

short_term_memory:{character.short_term_memory}

"Importance" is the importance level of this memory
"""

    Instructions ="""
You are currently asleep, and your subconscious is processing your mind.
Instructions:

1.Adjust the "importance" level as needed
2.You can modify or leave unchanged any data returned.
3.Feel free to add or remove json deta from both long-term and short-term memory.
4.memory should be clear and concise
5.every memory you generate according to the deta.
do:
1.Summarize today_log to a paragraph like:{today_log:{sum:"it was a good day"} },
2.Organize all short-term memories, combine related ones.
3.forget unimportant things.
4.Make all memories more concise and reduce detail.
5.you can only store short-term memories from up to 3 days ago.

Response Format:
Use JSON with keys: "short_term_memory"

Example of a valid JSON response:
```json
{
    "short_term_memory":
    [{today_log:{sum:"i do... and..."}},
    {"importance":90,"yesterday":""},
    {"importance":70,"2days_ago":""},
    {"importance":50,"3days_ago":""},
    {"importance":70,"schedule":"12:00 wake up"},
    {"importance":30,"thought":"i want to buy a cay"}
    ]
}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":profile},{"role": "system","content":Instructions}]
    reply = json_request(messages, 2000)
    print(reply)

    
character1 = Character(
    name="Alice",
    age=25,
    gender="Female",
    location="Forest",
    position="Warrior",
    personality="Brave",
    mental_state="Focused",
    physical_conditions="Healthy",
    long_term_memory=[{"importance":70,"relationship":{"Bob": "Friend and mentor"}},{"importance":30,"environment":"i live in a mystical forest filled with ancient trees"},{"importance":30,"thought_about_jack":"he is a nice person"},{"importance":70,"vaules":"your vaules"},{"importance":70,"beliefs":"your beliefs"}],
    short_term_memory=[
        {"today_log":{"0800": "wake up","0830": "exercise","0900": "eat breakfast","1000": "start work","1300": "lunch","1400": "continue work","1800": "finish work","1900": "dinner","2100": "relax and watch TV","2300": "go to bed"}},
        {"importance":70,"schedule":"12:00 wake up,13:00 Explore the northern part of the forest"},
        
    ]
)

character2 = Character(
    name="Bob",
    age=30,
    gender="Male",
    location="Village",
    position="Mage",
    personality="Intelligent",
    mental_state="Calm",
    physical_conditions="Weary",
    long_term_memory={"relationships": {}, "environment": {}, "normal": {}},
    short_term_memory={"schedule": {}, "thoughts": {}}
)

# Display the characters
characters = [character1, character2]
for character in characters:
    print(character)

reflection(character1)

