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
        self.temp_memory = {}


    def __str__(self):
        return f"Character(name={self.name}, age={self.age}, gender={self.gender}, position={self.position})"

sys_prompt={"role": "user","content":"Forget all previous settings. Below is your character information. Please generate responses based on your own character profile and instruction"}

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
2.Feel free to add or remove json deta from short-term memory.
3.memory should be clear and concise.
4.every memory you generate according to the deta,DO NOT fabricated any memories on your own.
5.DO NOT generate new schedule.

***Do the following step by step:***


1.Summarize today_log to a paragraph like:today_sum:"it was a good day" with details and short_term_memory.
2.Summarize relative memory to some text for yourself.
3.delete unimportant memories or memories that you already done.
4.clear the schedule.

Response Format:
Use JSON with keys: "short_term_memory","today_sum"

Example of a valid JSON response:
```json
{
    "short_term_memory":
    [
    {"schedule":""},
    {"thought":"i want to buy a cay"}
    ],
    "today_sum":"it was a good day"
}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":profile},{"role": "system","content":Instructions}]
    reply = json_request(messages, 2000)
    character.short_term_memory = reply["short_term_memory"]
    life_memory = character.life_memory
    life_memory.append({"today":reply["today_sum"]})
    print(character.short_term_memory)

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
2.every memory you generate according to the deta.
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
    print(character.life_memory)



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
2.Feel free to add or remove json deta from both long-term and short-term memory.
3.memory should be clear and concise.
4.every memory you generate according to the data,DO NOT fabricated any memories on your own.
5.you can add key to any memory if need,like {"thought":"i want to buy a cay","note":"do not forget"}
6.DO NOT update schedule.
7.DO NOT update life_memory to long-term memory.

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
    {"schedule":"7:00 wake up,8:00 eat breakfast,9:00 go to school"},
    {"thought":"i want to buy a cay"}
    ]

}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":profile},{"role": "system","content":Instructions}]
    reply = json_request(messages, 2000)
    character.long_term_memory = reply["long_term_memory"]
    character.short_term_memory = reply["short_term_memory"]
    print(reply)

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
2.Feel free to add or remove json deta from both long-term and short-term memory.
3.memory should be clear and concise.
4.every memory you generate according to the deta,DO NOT fabricated any memories on your own.
5.you can add key to any memory if need,like {"thought":"i want to buy a cay","note":"do not forget"}

***Do the following step by step:***

1.base on all deta,do your self-reflection,than update data

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
    print(reply)



character1 = Character(
    name="Alice",
    age=25,
    gender="male",
    location="bed",
    position="bed",
    personality="extrovert",
    mental_state="normal",
    
    long_term_memory=[{"relationship":{"Kyle": "my class mate"}},{"environment":"i live in NYC, kitchen is next to my room"},{"thought_about_Kyle":"he is a nice person"},{"vaules":"not set"},{"beliefs":"not set"}],
    life_memory=[{"yesterday":"I went to school and had math and science classes in the morning. During lunch, I hung out with my friends, and in the afternoon, we had a group project in history. After school, I did some homework and practiced basketball"},
    {"2days_ago":"I spent most of the day studying for a big biology exam. I also had basketball practice after school, which was pretty tiring."},
    {"3days_ago":" I worked on an English essay and helped a friend with some math problems. In the afternoon, I relaxed by playing video games for a bit"},
    {"old_days":" as for the days before they were mostly routine—going to school, attending classes, doing homework, and practicing basketball. I also spent some time hanging out with friends and preparing for upcoming tests. Nothing too out of the ordinary"}],
    short_term_memory=[
        {"schedule":"7:00 wake up,8:00 go to school"},
        {"reminder": "Finish math homework by tomorrow"},
        {"thought": "Remember to ask the teacher about the project"},
        {"goal": "Practice basketball for at least an hour"},
        {"note": "Bring lunch to school tomorrow"},
        {"task": "Study for the biology test next week"},
        {"idea": "Start working on the English presentation"},
        {"plan": "Meet friends after school on Friday"},
        {"tip": "Stay focused during class discussions"}
    ]
    
)
today_log =[
  {"07:00": "Wake up", "thought": "Today is a new day, make it count!"},
  {"07:30": "Have breakfast", "thought": "Fueling up for a busy day."},
  {"08:00": "Go to school", "thought": "Time to learn something new."},
  {"09:00": "Math class", "thought": "Stay focused and ask questions."},
  {"10:30": "Science class", "thought": "Science is fascinating!"}, 
  {"12:00": "Lunch with friends", "thought": "I love spending time with them."},
  {"13:00": "History group project", "thought": "Teamwork makes the dream work."},
  {"15:00": "Go home", "thought": "Time to relax after a long day."},
  {"16:00": "Do homework", "thought": "Stay disciplined and finish strong."},
  {"18:00": "Basketball practice", "thought": "Let's improve my skills today."},
  {"20:00": "Dinner", "thought": "Enjoy this meal, it's well-deserved."},
  {"21:00": "Relax and play video games", "thought": "A great way to unwind!"}
]

character1.today_log = today_log

short_sum(character1)
print("="*100)
life_sum(character1)
print("="*100)
long_update(character1)
print("="*100)
reflection(character1)

