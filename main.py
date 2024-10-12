import os
import json
import openai
from openai import AzureOpenAI
import time
import role
from role import Character,Environment,Item
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
    



tv = Item(name="tv",location=(12,0),description="an old tv")
bed = Item(name="bed",location=(0,0),description="Alice's bed")
table = Item(name="table",location=(3,3),description="Alice's table")
chair = Item(name="chair",location=(3,4),description="Alice's chair")

room = Environment(name="room",description="Alice's room",t=datetime(2024,10,12,8,0,0))

room.objects = [tv,bed,table,chair]


character1 = Character(
    name="Alice",
    age=25,
    gender="male",
    environment=room,
    location=(0,0),
    position="bed",
    personality="extrovert",
    mental_state="normal",
    
    long_term_memory=[{"relationship":{"Emily": "my girlfriend"}},{"environment":"i live in NYC, kitchen is next to my room"},{"thought_about_Emily":"she is a nice person"},{"vaules":"not set"},{"beliefs":"not set"}],
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
today_log1 = [
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
character1.today_log = today_log1

character2 = Character(
    name="Emily",
    age=24,
    gender="female",
    environment=room,
    location=(0,0),
    position="bed",
    personality="kind and empathetic",
    mental_state="content",

    long_term_memory=[{"relationship":{"Alice": "my boyfriend"}},{"environment":"I live in Brooklyn, my favorite café is just around the corner"},{"thought_about_Alice":"he is so energetic and always brightens my day"},{"values":"honesty, compassion"},{"beliefs":"Love is about mutual respect and support"}],
    life_memory=[
        {"yesterday":"I spent the evening with Alice, we went to the park and grabbed dinner at our favorite restaurant."},
        {"2days_ago":"I had a busy day at work, but Alice sent me a sweet message that made my day better."},
        {"3days_ago":"I helped Alice with her project and afterward, we watched a movie together."},
        {"old_days":"We've been together for almost two years now, and we've shared so many memories—trips, dinners, late-night conversations. She's been a huge part of my life."}
    ],
    short_term_memory=[
        {"schedule":"8:00 wake up, 9:00 go to work"},
        {"reminder": "Buy Alice's favorite tea when I visit her tomorrow."},
        {"thought": "I wonder how Alice's day is going."},
        {"goal": "Finish my presentation and surprise Alice with dinner tonight."},
        {"note": "Call mom to check in."},
        {"task": "Prepare the proposal for the meeting on Thursday."},
        {"idea": "Plan a weekend getaway with Alice."},
        {"plan": "Finish work early and spend the evening with Alice."},
        {"tip": "Take a break when feeling overwhelmed at work."}
    ]
)
today_log2 = [
  {"08:00": "Wake up", "thought": "A new day, excited to meet Alice later."},
  {"09:00": "Go to work", "thought": "Busy day ahead, but I'll get through it."},
  {"12:00": "Lunch break", "thought": "I should call Alice to check in."},
  {"15:00": "Work on presentation", "thought": "I need to focus, almost done."},
  {"18:00": "Leave work", "thought": "Can't wait to see Alice tonight."},
  {"19:00": "Dinner with Alice", "thought": "Spending time with her always feels right."},
  {"21:00": "Go for a walk", "thought": "Walking hand in hand, it’s the perfect way to end the day."},
  {"22:00": "Go to bed", "thought": "Feeling happy and loved."}
]
character2.today_log = today_log2

room.roles = [character1,character2]

role.short_sum(character1)
role.life_sum(character1)
role.long_update(character1)
role.reflection(character1)

role.short_sum(character2)
role.life_sum(character2)
role.long_update(character2)
role.reflection(character2)

role.perception(character1,"you wake up")

