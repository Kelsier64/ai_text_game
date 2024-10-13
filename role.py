import os
import json
import openai
from openai import AzureOpenAI
import time
from datetime import datetime
import math
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
deployment_name = "gpt4o"

client = AzureOpenAI(
  api_key = API_KEY,  
  api_version = "2024-09-01-preview",
  azure_endpoint = RESOURCE_ENDPOINT
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
    def __init__(self,name,description,t:datetime):
        self.name = name
        self.description = description
        self.time = t.strftime("%H:%M")
        self.date = t.strftime("%m/%d %A")
        self.weather = ""
        self.temperature = 25
        self.objects = []
        self.roles = []

    def __str__(self):
        return f"environment:{self.name},doing:{self.description},time:{self.time},date:{self.date}"

class Item:
    def __init__(self,name,location,description):
        self.name = name
        self.location = location
        self.description = description
    def __str__(self):
        return f"name:{self.name},description:{self.description}"

class Gate:
    def __init__(self,name,location,description,connection):
        self.name = name
        self.location = location
        self.description = description
        self.connection = connection
    def __str__(self):
        return f"name:{self.name},description:{self.description},connection:{self.connection[0].name} and {self.connection[1].name}"

class Character:
    def __init__(self, name, age, gender,environment:Environment, location,position, personality, mental_state,long_term_memory,life_memory,short_term_memory):
        self.name = name
        self.age = age
        self.gender = gender
        self.environment=environment

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

    def go(self,item):
        self.position = item.name
        self.location = item.location
    def enter(self,target):
        if self.environment == target.connection[0]:
            self.environment = target.connection[1]
        elif self.environment == target.connection[1]:
            self.environment = target.connection[0]
            
    def objects(self):
        objects = []
        for item in self.environment.objects:
            angle, distance = position(self.location,item.location)
            objects.append({"object":item.__str__(),"position":f"{int(angle)}degrees/{int(distance)}metters"})
        return objects
    
    def people(self):
        people = []
        for person in self.environment.roles:
            angle, distance = position(self.location,person.location)
            people.append({"name":person.name,"description":person.doing,"position":f"{int(angle)}degrees/{int(distance)}metters"})
        return people

    def __str__(self):
        return f"{self.name},position:{self.position},doing:{self.doing}"

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

perception_prompt={"role": "system","content":"Forget all previous settings.select the next thing you want to do based on your character data following"}

def perception(character:Character,change):
    profile=f"""
Here is your character's data:

Basic Information:
- Name: {character.name}
- Gender: {character.gender}
- Age: {character.age}

Current Status:
- Position: {character.position}
- Activity: {character.doing}

Personality and State:
- Personality: {character.personality}
- Mental State: {character.mental_state}
- Physical Condition: {character.physical_conditions}
- External Conditions (e.g., injuries): {character.external_conditions}

Memory Details:
- Long-term Memory: {character.long_term_memory}
- Life Memory: {character.life_memory}
- Short-term Memory: {character.short_term_memory}
- Today's Log: {character.today_log}

Environment:
- Description: {character.environment}
- Objects: {character.objects()}
- People: {character.people()}
"""
    
    now = f"""
    memories right now(temp_memory):{character.temp_memory}
    new event:{change}
"""
    instructions ="""
Instructions:
1.generate every thing in first-person.

***Do the following step by step:***

1.base on all data,especially temp_memory and new event,select a target (object or person in environment) and decide what you want to do with it.
2.to do it,make an action.
3.If you and the selected object or person are not in the same position, your first action should be to walk toward them.
4.Make some memories about your decision, thoughts on the new event, etc.
5.Create a message. If the target is a person, the message will be said to them. If the target is an object, it’s your murmur; however, it can also be left blank.
6.If you’ve just ended a conversation, do not target the same person. Move on to something else.


Use JSON with keys: 
"target"(you can only select object or person in environment),"do"(what you are going to do in brief),"action","memory"(what you are going to do in details),"message"

Example of a valid JSON response for object:

if you want to continue what you are doing for a while,leave "continue" in key "action"(this only need to do on object)
```json
{
  "target":"table",
  "do":"study",
  "action":"continue",
  "memory":{"event":"","decision":"","thought":""},
  "message":""
  
}'''
Example of a valid JSON response for person:
```json
{
  "target":"Jack",
  "do":"talk",
  "action":"walk toward Jack",
  "memory":{"event":"","decision":"","thought":""},
  "message":"hi Jack."
}'''
"""

    messages = [perception_prompt,{"role": "system","content":profile},{"role": "system","content":now},{"role": "system","content":instructions}]
    reply = json_request(messages, 2000)
    reply["memory"]["event"] = change
    character.temp_memory.append(reply["memory"])
    character.temp_memory.append({"I_say":reply["message"]})

    for item in character.environment.objects:
        if item.name == reply["target"]: 
            if reply["action"] == "continue":
                temp_sum(character)
                character.temp_memory = [reply["memory"],{"I_say":reply["message"]}]
            else:
                item_interaction(character,reply["target"],reply["do"],reply["action"])

    for role in character.environment.roles:
        if role.name == reply["target"]:
            role_interaction(character,reply["target"],reply["message"],reply["do"],reply["action"])

def temp_sum(character:Character):
    
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
    character.today_log.append({character.environment.time:reply["temp_sum"]})

system_prompt={"role": "system","content":"you are a system of a game. Please generate responses based on data and instruction"}

def item_interaction(character:Character,target,do,action):

    for i in character.environment.objects:
        if i.name == target:
            target = i
            
    data=f"""
"Here is data of the game:

environment details:
{character.environment}

objects in environment (perspective of character):
{character.objects()}

people in this environment (perspective of character):
{character.people()}

request character:{character}

request details:

target:{target}

want to do:{do}

action:{action}
"""
    
    functions = """
    function you have:
    {"function":"goto"}(ex:"doing":"study"),
    {"function":"sleep"},
    {"function":"enter"}(ex:"message":"you enter the living room","doing":"stand by the door"),
    {"function":"pass"}
   
"""
    instructions ="""
Instructions:
only do what character request.

***Do the following step by step:***

1.base on data,select an appropriate function to use.if no suitable function,respond with "execute":{"function":"pass"}
2.whether you pass the function or not,generate a message telling the requester that his action has been completed (in the first-person perspective).
3.update what the requester is doing now in brief(in third-person perspective).

Response Format:
Use JSON with keys: "execute","message","doing"

Example of a valid JSON response:
```json
{
    "execute":{"function":"go"},
    "message":"you walk to the table and sit down",
    "doing":"study"
}'''
    
    
"""
    messages = [system_prompt,{"role": "system","content":data},{"role": "system","content":functions},{"role": "system","content":instructions}]
    reply = json_request(messages, 2000)
    if reply["execute"]["function"] == "goto":
        character.go(target)

    if reply["execute"]["function"] == "enter":
        character.go(target)
        character.enter(target)
                
    character.doing = reply["doing"]
    print(action+"/"+character.__str__()+","+character.environment.name)
    print(reply)
    breakpoint()
    perception(character,reply["message"])

def role_interaction(character:Character,target,message,do,action):

    data=f"""
"Here is data of the game:

environment details:
{character.environment}

objects in environment (perspective of character):
{character.objects()}

people in this environment (perspective of character):
{character.people()}

request character:{character}

request details:

target:{target}

want to do:{do}

message:{message}

action:{action}
"""
    
    instructions ="""
Instructions:
only do what character request.

***Do the following step by step:***

1.base on data,generate a message for target,conbine requester"s action,message,and other details.
2.update what they are doing in very brief(in third-person perspective).

Response Format:
Use JSON with keys:"target","message","requester_doing","target_doing"

Example of a valid JSON response:
```json
{
    "target":"Jack",
    "message":"Evan woke me up and said:'good morning'",
    "requester_doing":"talking to Jack",
    "target_doing":"talking to Evan"
}'''
    
    
"""
    messages = [system_prompt,{"role": "system","content":data},{"role": "system","content":instructions}]
    reply = json_request(messages, 2000)
    character.doing = reply["requester_doing"]
    print(character.__str__()+","+character.environment.name+":"+message)
    breakpoint()
    for person in character.environment.roles:
        if person.name == reply["target"]:
            person.doing=reply["target_doing"]
            interaction(person,reply["message"],character)

interaction_prompt={"role": "system","content":"Forget all previous settings.generate dialogue based on your character data following"}

def interaction(character:Character,change,target):
    profile=f"""
Here is your character's data:

Basic Information:
- Name: {character.name}
- Gender: {character.gender}
- Age: {character.age}

Current Status:
- Position: {character.position}
- Activity: {character.doing}

Personality and State:
- Personality: {character.personality}
- Mental State: {character.mental_state}
- Physical Condition: {character.physical_conditions}
- External Conditions (e.g., injuries): {character.external_conditions}

Memory Details:
- Long-term Memory: {character.long_term_memory}
- Life Memory: {character.life_memory}
- Short-term Memory: {character.short_term_memory}
- Today's Log: {character.today_log}

Environment:
- Description: {character.environment}
- Objects: {character.objects()}
- People: {character.people()}
"""

    conversation = f"""
Interaction Details:
- You are NOW interacting with: {target.name}
- Memory of Previous Interaction (chat history): {character.temp_memory}
- New Interaction Details: {change}
"""


    instructions = """
Instructions:
1.generate every memories in the first-person.

***Do the following step by step:***
1.Generate the words you want to say and actions towards the one you are interacting with, based on your data, especially chat history.
2.You can only perform interactive actions; you CANNOT walk or move away.However, leave "next" in the key "interaction" to end the conversation in order to perform another action.
3.Do not repeat the conversation; end it to do something else.
4.make some memories about your thought,etc.

Use JSON with keys: "interaction","message","memory"

Example of a valid JSON response:
```json
{
  "interaction":"walk toward Jack",
  "message":"hi Jack.",
  "memory":{"thought":""}
}'''

(leave "next" in key "interaction" to end the conversation to do another thing.)
```json
{
  "interaction":"next",
  "message":"bye Jack.",
  "memory":{"thought":""}
}'''

"""

    messages = [interaction_prompt,{"role": "system","content":profile},{"role": "system","content":conversation},{"role": "system","content":instructions}]
    reply = json_request(messages, 2000)
    reply["memory"]["event"] = change
    character.temp_memory.append(reply["memory"])
    character.temp_memory.append({"I_said":reply["message"]})

    if reply["interaction"] == "next":

        perception(character,"you end the conversation to do next thing")
        perception(target,f"{reply["message"]} and {character.name} end the conversation")
    else:
        for role in character.environment.roles:
            if role.name == target.name:
                role_interaction(character,target.name,reply["message"],"interaction",reply["interaction"])