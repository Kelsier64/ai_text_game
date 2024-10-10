import os
import json
import openai
from openai import AzureOpenAI
import time
from datetime import datetime
import math
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
def position(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    
    return angle, distance

class Environment:
    def __init__(self,name,description,time:datetime):
        self.name = name
        self.description = description
        self.time = time
        self.weather = ""
        self.temperature = 25
        self.objects = []
    def __str__(self):
        return f"environment:{self.name},description:{self.description},time:{self.time.strftime("%H:%M")},date:{self.time.strftime("%m/%d %A")}"

class Item:
    def __init__(self,name,location,description):
        self.name = name
        self.location = location
        self.description = description
    def __str__(self):
        return f"name:{self.name},description:{self.description}"

class Character:
    def __init__(self, name, age, gender, location,position, personality, mental_state,long_term_memory,life_memory,short_term_memory):
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
        self.physical_conditions = ""
        self.external_conditions = {}
        self.mood = "not set"
        self.long_term_memory = long_term_memory
        self.life_memory = life_memory
        self.short_term_memory = short_term_memory
        self.today_log = []
        self.temp_memory = []

    def item(self,environment):
        objects = []
        for item in environment.objects:
            angle, distance = position(self.location,item.location)
            objects.append({"name":item.name,"description":item.description,"position":f"{int(angle)}degrees/{int(distance)}metters"})
        return objects
    def __str__(self):
        return f"Character(name={self.name}, age={self.age}, gender={self.gender}, position={self.position})"

sys_prompt={"role": "system","content":"Forget all previous settings. Below is your character information. Please generate responses based on your own character profile and instruction"}

def short_sum(character:Character):
    
    profile=f"""
"Here is your character data:

Memory details:

short_term_memory:{character.short_term_memory}

today_log:{character.today_log}

"""

    Instructions ="""
You are currently asleep, and you are processing your mind.
Instructions:


1.You can modify or leave unchanged any data returned.
2.Feel free to add or remove json data from short-term memory.
3.memory should be clear and concise.
4.every memory you generate according to the data,DO NOT fabricated any memories on your own.

***Do the following step by step:***


1.Summarize today_log to a paragraph like:today_sum:"it was a good day" with details and short_term_memory.
2.Summarize relative short_term_memory to some text for yourself.
3.delete unimportant memories or memories that you already done.
4.delete the schedule.

Response Format:
Use JSON with keys: "short_term_memory","today_sum"

Example of a valid JSON response:
```json
{
    "short_term_memory":
    [
    {"thought":"i want to buy a cay"},
    {"plan": "Meet friends after school on Friday"}
    ],
    "today_sum":"it was a good day"
}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":profile},{"role": "system","content":Instructions}]
    reply = json_request(messages, 2000)
    character.short_term_memory = reply["short_term_memory"]
    life_memory = character.life_memory
    life_memory.append({"today":reply["today_sum"]})
    character.today_log = []
    character.life_memory = life_memory

def life_sum(character:Character):
    
    profile=f"""
"Here is your character data:

Memory details:

life_memory:{character.life_memory}

"""

    Instructions ="""
You are currently asleep, and you are processing your mind.
Instructions:
1.memory should be clear and concise.
2.every memory you generate according to the data.
3.DO NOT fabricated any memories on your own.

***Do the following step by step:***
1.because you are sleeping,today become "yesterday","yesterday" become "2days_ago",and so on
2.if memories more than 3 days ago,summarize it into "old_days"
3.the older the memory the less clear it becomes.
4.summarize "old_days",make it more concise and less details;however,if the detail is important do not forget it.

Response Format:
Use JSON with keys: "yesterday","2days_ago","3days_ago","old_days"

Example of a valid JSON response:
```json
{
    "yesterday":"...",
    "2days_ago":"...",
    "3days_ago":"...",
    "old_days":"..."
}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":profile},{"role": "system","content":Instructions}]
    reply = json_request(messages, 2000)
    character.life_memory = [reply]
    character.today_log = []

def long_update(character:Character):
    profile=f"""
"Here is your character data:

Your basic information: name:{character.name},gender:{character.gender},age:{character.age}
Your current position:{character.position}

you are currently doing:{character.doing}

Your personality:{character.personality}

Your current mental state:{character.mental_state}

Your current physical condition:{character.physical_conditions}

Your external physical state(such as injuries):{character.external_conditions} 

Your attention level:{character.concertration} 
You may miss environmental changes if their significance is lower than your attention level.



Memory details:

long_term_memory:{character.long_term_memory}

life_memory:{character.life_memory}

short_term_memory:{character.short_term_memory}

"""

    Instructions ="""
You are currently asleep, and your subconscious is processing your mind.
Instructions:


1.You can modify or leave unchanged any data returned.
2.Feel free to add or remove json data from both long-term and short-term memory.
3.memory should be clear and concise.
4.every memory you generate according to the data,DO NOT fabricated any memories on your own.
5.you can add key to any memory as additional explanation,like {"thought":"i want to buy a cay","note":"do not forget"}
6.DO NOT update life_memory to long-term memory.

***Do the following step by step:***

1.update important short-term memory into long-term memory.
2.delete unimportant memories or memories that you already done.
3.delete short_term_memory that you have update.

Response Format:
Use JSON with keys: "long_term_memory","short_term_memory"

Example of a valid JSON response:
```json
{
  "long_term_memory":
  [
  {"relationship":{"Jack": "my class mate"}},
  {"environment":"i have a tv in my room"},
  {"thought_about_jack":"he is a nice person"},
  {"vaules":"your vaules"},
  {"beliefs":"your beliefs"}],
"short_term_memory":
    [
    {"plan": "Meet friends after school on Friday"},
    {"thought":"i want to buy a cay"}
    ]

}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":profile},{"role": "system","content":Instructions}]
    reply = json_request(messages, 2000)
    character.long_term_memory = reply["long_term_memory"]
    character.short_term_memory = reply["short_term_memory"]

def reflection(character:Character):
    profile=f"""
"Here is your character data:

Your basic information: name:{character.name},gender:{character.gender},age:{character.age}
Your current position:{character.position}

you are currently doing:{character.doing}

Your personality:{character.personality}

Your current mental state:{character.mental_state}

Your current physical condition:{character.physical_conditions}

Your external external conditions(such as injuries):{character.external_conditions} 

Your attention level:{character.concertration} 
You may miss environmental changes if their significance is lower than your attention level.

Memory details:

long_term_memory:{character.long_term_memory}

life_memory:{character.life_memory}

short_term_memory:{character.short_term_memory}



"""

    Instructions ="""
You are currently asleep, and your subconscious is processing your mind.
Instructions:


1.You can modify or leave unchanged any data returned.
2.Feel free to add or remove json data from both long-term and short-term memory.
3.memory should be clear and concise.
4.every memory you generate according to the data,DO NOT fabricated any memories on your own.
5.you can add key to any memory as additional explanation,like {"thought":"i want to buy a cay","note":"do not forget"}

***Do the following step by step:***

1.base on all data,do your self-reflection,than update data

self-reflection:
Self-Questioning
What did I learn today?
What challenges did I face, and how did I respond to them?
What am I proud of achieving recently?
What could I have done differently?
How do I feel about my progress?
What skills do I need to develop further?
What motivates me to improve?
What are my values, and am I living in alignment with them?

after self-reflection,
update long_term_memory like challenges,proud_of,goal,values,and so on.
update "self" about what a person you are in long_term_memory helping you get to know yourself better.


2.Update mental state and personality if needed.
3.make a new schedule for tomorrow,and delete the old one.
4.because you are waking up,update all memory referring to tomorrow to today,2days after to tomorrow,and so on.

Response Format:
Use JSON with keys: "personality","mental_state","long_term_memory","short_term_memory"

Example of a valid JSON response:
```json
{
  "personality":"Brave",
  "mental_state":"normal",
  "long_term_memory":
  [
  {"relationship":{"Jack": "my class mate"}},
  {"environment":"i have a tv in my room"},
  {"thought_about_jack":"he is a nice person"},
  {"vaules":"your vaules"},
  {"beliefs":"your beliefs"}],
"short_term_memory":
    [
    {"schedule":"7:00 wake up,8:00 eat breakfast,9:00 go to school"},
    {"thought":"i want to buy a cay"}
    ]
}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":profile},{"role": "system","content":Instructions}]
    reply = json_request(messages, 2000)
    character.personality = reply["personality"]
    character.mental_state = reply[ "mental_state"]
    character.short_term_memory = reply["short_term_memory"]
    character.long_term_memory=reply["long_term_memory"]

def next(character:Character,environment:Environment):
    profile=f"""
"Here is your character data:

Your basic information: name:{character.name},gender:{character.gender},age:{character.age}

Your current position:{character.position}

Your personality:{character.personality}

Your current mental state:{character.mental_state}

Your current physical condition:{character.physical_conditions}

Your external external conditions(such as injuries):{character.external_conditions} 

Memory details:

long_term_memory:{character.long_term_memory}

life_memory:{character.life_memory}

short_term_memory:{character.short_term_memory}

temp_memory:{character.temp_memory} (memories about what you just done.)

today_log:{character.today_log}

environment details:
{environment}
objects in environment:
{character.item(environment)}

"""

    instructions ="""
***Do the following step by step:***

1.base on all data,especially temp_memory,respose next thing you want to do.
2.select a target (object or person in environment) and what you want to do with it.
3.make some memories about your decision,and your thought.


Response Format:
Use JSON with keys: "target"(you can only select objects in environment),"do"(what you are going to do in brief),"memory"(what you are going to do in details)

Example of a valid JSON response:
```json
{
  "target":"table",
  "do":"study",
  "memory":[{"decision"},{"thought"}]
}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":profile},{"role": "system","content":instructions}]
    reply = json_request(messages, 2000)
    print(reply)
    breakpoint()
    character.temp_memory = reply["memory"]
    character.doing = reply["do"]
    item = reply["target"]
    
    role_action(character,environment,reply["target"],reply["do"])
    

    for obj in environment.objects:
        if item == obj.name:
            character.location = obj.location
            character.position = obj.name


   

def perception(character:Character,environment:Environment,change):
    profile=f"""
"Here is your character data:

Your basic information: name:{character.name},gender:{character.gender},age:{character.age}

Your current position:{character.position}

Your personality:{character.personality}

Your current mental state:{character.mental_state}

Your current physical condition:{character.physical_conditions}

Your external external conditions(such as injuries):{character.external_conditions} 

Memory details:

long_term_memory:{character.long_term_memory}

life_memory:{character.life_memory}

short_term_memory:{character.short_term_memory}

today_log:{character.today_log}

temp_memory:{character.temp_memory} (memories about right now.)

what you are doing right now:{character.doing}

environment details:
{environment}
objects in environment:
{character.item(environment)}

environment change:
{change}
"""

    instructions ="""
***Do the following step by step:***

1.according to the environment change,continue what you are doing or do next thing.
2.add the change,your thought,decision,etc about the change into "change".
3.if you want to do next thing,response "next"

Response Format:
Use JSON with keys:"do"(options:"continue" or "next"),"change"

Example of a valid JSON response:
```json
{
  "do":"stop",
  "change":{"change","thought","decision"}
}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":profile},{"role": "system","content":instructions}]
    reply = json_request(messages, 2000)
    print(reply)
    breakpoint()
    temp = character.temp_memory
    temp.append(reply["change"])
    character.temp_memory = temp

    if reply["do"] == "next":
        
        temp_sum(character,environment)
        character.temp_memory = [reply["change"]]
        next(character,environment)

def temp_sum(character:Character,environment:Environment):
    
    profile=f"""
"Here is your character data:

Memory details:

short_term_memory:{character.short_term_memory}

temp_memory:{character.temp_memory}

"""

    Instructions ="""
1.You can modify or leave unchanged any data returned.
2.Feel free to add or remove json data from both short-term memory and temp_memory.
3.memory should be clear and concise.
4.every memory you generate according to the data,DO NOT fabricated any memories on your own.

***Do the following step by step:***


1.if there is some thing need to be remembered in temp_memory,Summarize it into short_term_memory,
however do not remember unimportant memories.
2.Summarize relative short_term_memory.
3.sum up temp_memory into one paragraph in "temp_sum"
4.delete unimportant memories or memories that you already done in short_term_memory.

Response Format:
Use JSON with keys: "short_term_memory","temp_sum"

Example of a valid JSON response:
```json
{
    "short_term_memory":
    [
    {"thought":"i want to buy a cay"},
    {"plan": "Meet friends after school on Friday"}
    ]
    "temp_sum":""
}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":profile},{"role": "system","content":Instructions}]
    reply = json_request(messages, 2000)
    character.short_term_memory = reply["short_term_memory"]
    today = character.today_log
    today.append({environment.time:reply["temp_sum"]})
    character.today_log = today

system_prompt={"role": "system","content":"you are a system of a game. Please generate responses based on data and instruction"}
def role_action(character:Character,environment:Environment,target,action):
    data=f"""
"Here is data of the game:

request character:{character}

environment details:
{environment}

objects in environment (perspective of character):
{character.item(environment)}

request details:

target:{target}

action:{action}
"""
    functions = """
    function you have:
    {"function":"go","parameter":"table"}(object),
    {"function":"sleep"}
    {"function":"leave"}
"""
    instructions ="""

Instructions:
only do what character request.

***Do the following step by step:***


1.select a function to use.
2.after select,generate a suitable response telling the character the action is completed.
3.response start with You.
4.response what the character is doing now.

Response Format:
Use JSON with keys: "function","response","doing"

Example of a valid JSON response:
```json
{
    "function":{"function":"sleep"},
    "response":"You get out of bed",
    "doing":"standing by the bed"
}'''
    
    
"""
    messages = [system_prompt,{"role": "system","content":data},{"role": "system","content":functions},{"role": "system","content":instructions}]
    
    reply = json_request(messages, 2000)
    character.doing = reply["doing"]
    print(reply)
    perception(character,environment,reply["response"])