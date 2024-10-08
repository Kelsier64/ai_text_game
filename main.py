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
        self.external_conditions = []
        self.mood = "not set"
        self.long_term_memory = long_term_memory
        self.short_term_memory = short_term_memory
        self.temp_memory = []
    def update(self,name=None,age=None,gender=None, location=None,position=None, personality=None, mental_state=None, physical_conditions=None,long_term_memory=None,short_term_memory=None):
        for key,value in locals().items():
            if key != "self" and value is not None:
                setattr(self,key,value)

    def __str__(self):
        return f"Character(name={self.name}, age={self.age}, gender={self.gender}, position={self.position})"

sys_prompt={"role": "user","content":"Forget all previous settings. Below is your character information. Please generate responses based on your own character profile and instruction"}

def reflection(character):
    
    reflection_prompt =f"""
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

Your hunger level:{character.hunger} 
100 is exremely full(You feel like you can’t eat another bite, and you might even feel uncomfortable)
on the other hand,0 is exremely hungry(almost fainting)
however,40-60 is a confortable range
lower than 40 you feel a little hungry
lower than 20 you feel a very hungry


Your current mood:{character.mood}


Memory details:


long_term_memory:{character.long_term_memory}

short_term_memory:{character.short_term_memory}

temp_memory:{character.temp_memory}

"Importance" is the importance level of this memory
"""
    Instructions ="""
You are currently asleep, and your subconscious is processing your mind.
Instructions:

1.Adjust the "importance" level as needed


2.memory should be clear and concise

do:

1.Create a new schedule for tomorrow or leave it blank.
2.Summarize today’s short-term memory,making a new daily memory in a few paragraphs as clear as posable.


Response Format:
Use JSON with keys:"Summarized_short_term_memory","schedule"

Example of a valid JSON response:
```json
{
    "Summarized_short_term_memory":"Today I spent the day tending to the trees and wildlife. I checked the health of the forest, cleared some fallen branches, and helped a few animals find food. I also took time to patrol the area, ensuring everything is safe and sound."
    "schedule":"12:00 wake up 13:00 eat breakfast"
}'''
    
    
"""
    messages = [sys_prompt,{"role": "system","content":reflection_prompt},{"role": "system","content":Instructions}]
    reply = json_request(messages, 2000)
    print(reply)
    long_term_memory = character.long_term_memory
    long_term_memory.append({"2024/10/8":{reply["Summarized_short_term_memory"]}})
    print(long_term_memory)


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
    short_term_memory=[{"importance":70,"schedule":"12:00 wake up,13:00 Explore the northern part of the forest"},
    {"importance":30,"current_goal":"Find the lost artifact."},
    {"importance": 80, "reflections": "Today was a challenging day, but I feel accomplished."},
    {"importance": 60, "encounter": "I met a mysterious traveler who spoke of the artifact."},
    {"importance": 50, "lesson_learned": "I learned to be cautious of my surroundings."},
    {"importance": 70, "evening_activity": "I practiced my swordsmanship under the stars."},
    {"importance": 90, "emotions": "I felt a sense of hope when I found a clue about the artifact's location."},
    {"importance": 40, "social_interaction": "I shared a meal with Bob and discussed our plans."},
    {"importance": 50, "thoughts_before_sleep": "I hope tomorrow brings new opportunities and challenges."}]
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

