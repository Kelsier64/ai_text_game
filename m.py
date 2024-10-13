import os
import json
import openai
from openai import AzureOpenAI
import time
import role
from role import Character,Environment,Item,Gate
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
microwave = Item(name="microwave",location=(5,5),description="")
fridge = Item(name="fridge",location=(5,6),description="")

room = Environment(name="room",description="Alice's room",t=datetime(2024,10,12,8,0,0))
living_room = Environment(name="living_room",description="living_room",t=datetime(2024,10,12,8,0,0))

door = Gate(name="door",location=(5,5),description="door of Alice's room",connection=[room,living_room])

room.objects = [tv,bed,table,chair,door]
living_room.objects = [tv,microwave,fridge,table,chair,door]

character1 = Character(
    name="Alice",
    age=25,
    gender="male",
    environment=room,
    location=(0,0),
    position="bed",
    personality="extrovert",
    mental_state="normal",
    
    long_term_memory=[{'relationship': {'Emily': 'my girlfriend'}}, {'environment': 'I live in NYC, kitchen is next to my room'}, {'thought_about_Emily': 'she is a nice person'}, {'routine': 'go to living room and make breakfast'}, {'reminder': 'Finish math homework by today'}, {'goal': 'Practice basketball for at least an hour'}, {'challenges': 'Balancing schoolwork and basketball practice'}, {'proud_of': 'Maintaining good grades while being active in sports'}, {'values': 'Hard work, dedication, and maintaining relationships'}, {'self': 'I am a dedicated and hardworking individual who values relationships and strives to balance academics and sports'}],
    life_memory=[{'yesterday': 'Today was productive and fulfilling. I woke up early, had a good breakfast, and went to school. I stayed focused during math and science classes, enjoyed lunch with friends, and worked well on the history group project. After school, I relaxed, did my homework, practiced basketball, and ended the day with a nice dinner and some video games.', '2days_ago': 'I went to school and had math and science classes in the morning. During lunch, I hung out with my friends, and in the afternoon, we had a group project in history. After school, I did some homework and practiced basketball.', '3days_ago': 'I spent most of the day studying for a big biology exam. I also had basketball practice after school, which was pretty tiring.', 'old_days': 'Routine school days with classes, homework, basketball practice, and hanging out with friends. Helped a friend with math, worked on an English essay, and played video games.'}],
    short_term_memory=[{'thought': 'Remember to ask the teacher about the project'}, {'task': 'Study for the biology test next week'}, {'idea': 'Start working on the English presentation'}, {'plan': 'Meet friends after school tomorrow'}, {'tip': 'Stay focused during class discussions'}, {'schedule': '7:00 wake up, 8:00 eat breakfast, 9:00 go to school, 15:00 practice basketball, 18:00 dinner, 19:00 finish math homework'}]

    
)
today_log1 = []
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

    long_term_memory=[{'relationship': {'Alice': 'my boyfriend'}}, {'environment': 'I live in Brooklyn, my favorite café is just around the corner'}, {'thought_about_Alice': 'he is so energetic and always brightens my day'}, {'values': 'honesty, compassion'}, {'beliefs': 'Love is about mutual respect and support'}, {'memory': 'I had a lovely dinner with Alice and ended the day with a peaceful walk together. Feeling happy and loved.'}, {'challenges': 'Balancing work and personal life can be tough, but I manage by staying organized and taking breaks when needed.'}, {'proud_of': 'Completing my presentation despite a busy day at work.'}, {'goal': 'Plan a weekend getaway with Alice.'}, {'self': 'I am a kind and empathetic person who values honesty and compassion. I believe in mutual respect and support in relationships. I strive to balance my work and personal life effectively.'}],
    life_memory=[{'yesterday': 'It was a wonderful day. I woke up excited to meet Alice later. Despite a busy day at work, I managed to stay focused and complete my presentation. I had a lovely dinner with Alice and ended the day with a peaceful walk together. Feeling happy and loved.', '2days_ago': 'I spent the evening with Alice, we went to the park and grabbed dinner at our favorite restaurant.', '3days_ago': 'I had a busy day at work, but Alice sent me a sweet message that made my day better.', 'old_days': "We've been together for almost two years now, sharing many memories—trips, dinners, late-night conversations. She's been a huge part of my life."}],
    short_term_memory=[{'reminder': "Buy Alice's favorite tea when I visit her today."}, {'task': 'Prepare the proposal for the meeting on Thursday.'}, {'idea': 'Plan a weekend getaway with Alice.'}, {'tip': 'Take a break when feeling overwhelmed at work.'}, {'schedule': '7:00 wake up, 8:00 eat breakfast, 9:00 go to work, 18:00 visit Alice, 20:00 relax at home'}]
)
today_log2 = []
character2.today_log = today_log2

room.roles = [character1,character2]

role.perception(character1,"you wake up")

