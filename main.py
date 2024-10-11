import os
import json
import openai
from openai import AzureOpenAI
import time
import role
from role import Character
from datetime import datetime
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
    
class Environment:
    def __init__(self,name,description,time:datetime):
        self.name = name
        self.description = description
        self.time = time.strftime("%H:%M")
        self.date = time.strftime("%m/%d %A")
        self.weather = ""
        self.temperature = 25
        self.objects = []
    def __str__(self):
        return f"environment:{self.name},description:{self.description},time:{self.time},date:{self.date}"

class Item:
    def __init__(self,name,location,description):
        self.name = name
        self.location = location
        self.description = description
    def __str__(self):
        return f"name:{self.name},description:{self.description}"



character1 = Character(
    name="Alice",
    age=25,
    gender="male",
    location=(0,0),
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
today_log = [
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


tv = Item(name="tv",location=(12,0),description="an old tv")
bed = Item(name="bed",location=(0,0),description="Alice's bed")
table = Item(name="table",location=(3,3),description="Alice's table")
chair = Item(name="chair",location=(3,4),description="Alice's chair")

room = Environment(name="room",description="Alice's room",time=datetime(2024,10,12,8,0,0))

room.objects = [tv,bed,table,chair]



role.short_sum(character1)

role.life_sum(character1)

role.long_update(character1)

role.reflection(character1)

role.perception(character1,room,"you wake up")

