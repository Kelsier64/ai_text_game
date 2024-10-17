import math
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Tuple
import asyncio
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
import os,json
import prompt
load_dotenv()
API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
deployment_name = "gpt4o"

client = AsyncAzureOpenAI(
  api_key = API_KEY,  
  api_version = "2024-09-01-preview",
  azure_endpoint = RESOURCE_ENDPOINT
)

async def json_request(messages):
    response = await client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)



class Position:
    """Class to handle coordinates and calculations."""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance_to(self, other: 'Position') -> float:
        """Calculate the distance between two positions."""
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def angle_to(self, other: 'Position') -> float:
        """Calculate the angle between two positions."""
        return math.degrees(math.atan2(other.y - self.y, other.x - self.x))

    def __str__(self):
        return f"Position(x={self.x}, y={self.y})"


class TimeManager:
    """Class to handle time globally or per character/environment."""
    
    def __init__(self,time: datetime):
        self.current_time = time

    def get_time(self) -> str:
        return self.current_time.strftime("%H:%M")

    def get_date(self) -> str:
        return self.current_time.strftime("%m/%d %A")


class Describable(ABC):
    """Abstract class for objects that have a name and description."""
    
    @abstractmethod
    def get_description(self) -> str:
        pass


class WorldObject(Describable):
    """Base class for objects in the environment."""
    
    def __init__(self, name: str, position: Position, description: str):
        self.name = name
        self.position = position
        self.description = description
    
    def get_description(self) -> str:
        return f"{self.name}: {self.description}"


class Item(WorldObject):
    """Items that characters can interact with."""

    def __init__(self, name: str, position: Position, description: str):
        super().__init__(name, position, description)


class Gate(WorldObject):
    """Represents a gate that connects two environments."""
    
    def __init__(self, name: str, position: Position, description: str, connections: Tuple['Environment', 'Environment']):
        super().__init__(name, position, description)
        self.connections = connections

    def traverse(self, current_environment: 'Environment') -> 'Environment':
        """Move between two environments."""
        if current_environment == self.connections[0]:
            return self.connections[1]
        else:
            return self.connections[0]

    def get_description(self) -> str:
        return (f"{self.name}: {self.description}, connects "
                f"{self.connections[0].name} and {self.connections[1].name}")


class Environment(Describable):
    """Represents the environment in which characters and objects exist."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.weather = "Clear"
        self.temperature = 25
        self.objects: List[WorldObject] = []
        self.characters: List['Character'] = []
        self.event_temp = []

    def add_character(self, character: 'Character'):
        """Add character to the environment and update character's environment."""
        if character not in self.characters:
            self.characters.append(character)
            character.environment = self

    def remove_character(self, character: 'Character'):
        """Remove character from the environment."""
        if character in self.characters:
            self.characters.remove(character)

    async def item_interaction(self,character:'Character',request):
        data=f"""
"Here is data of the game:
environment details:
{self.get_description()}
objects in environment (perspective of character):
{character.get_objects_in_view()}
people in this environment (perspective of character):
{character.get_characters_in_view()}
request character:{character.get_description()}
request details:
target:{request[0]}
want to do:{request[1]}
action:{request[2]}
"""
        functions = """
    function you have:
    {"function":"goto"}(ex:"doing":"study"),
    {"function":"sleep"},
    {"function":"enter"}(ex:"message":"you enter the living room","doing":"stand by the door"),
    {"function":"pass"}
"""         
        messages = [{"role": "system","content":prompt.system},{"role": "system","content":data},{"role": "system","content":functions},{"role": "system","content":prompt.item_instruction}]
        response = await json_request(messages)
        return response
       

    def get_description(self) -> str:
        return (f"Environment: {self.name}, Description: {self.description}, "
                f"Weather: {self.weather}, Temperature: {self.temperature}°C, Date:{time.get_date()}, Time:{time.get_time()}")

class Character(Describable):
    """Represents a character with attributes like personality, memory, etc."""
    
    def __init__(self, name: str, age: int, gender: str, environment: Environment, position: Position,location:str, personality: str, mental_state: str,short_term_memory:List[str],long_term_memory:List[str],life_memory:List[str]):
        self.name = name
        self.age = age
        self.gender = gender
        self.environment = environment
        self.position = position
        self.location = location
        self.hunger = 100
        self.concertration = 0
        self.facial_expression = "neutral"
        self.doing = "idle"
        self.personality = personality
        self.mental_state = mental_state
        self.long_term_memory =  long_term_memory
        self.short_term_memory = short_term_memory
        self.life_memory = life_memory
        self.today_log: List[str] = []
        self.temp_memory: List[str] = []
        self.environment.add_character(self)
        self.event_temp = []
        self.status = False
    def move_to(self, new_position: Position):
        """Change character's position."""
        self.position = new_position

    def interact_with_item(self, item: Item):
        """Interact with an item in the environment."""
        self.doing = f"interacting with {item.name}"

    def go_through_gate(self, gate: Gate):
        """Move through a gate to a different environment."""
        self.environment.remove_character(self)
        self.environment = gate.traverse(self.environment)
        self.environment.add_character(self)

    def get_objects_in_view(self):
        """Return objects and their positions relative to a character's location."""
        objects_in_view = []
        for obj in self.environment.objects:
            angle = self.position.angle_to(obj.position)
            distance = self.position.distance_to(obj.position)
            objects_in_view.append({
                "object": obj.get_description(),
                "position": f"{int(angle)} degrees / {int(distance)} meters"
            })
        return objects_in_view

    def get_characters_in_view(self):
        """Return characters and their positions relative to a character's location."""
        characters_in_view = []
        for character in self.environment.characters:
            if character is not self:
                angle = self.position.angle_to(character.position)
                distance = self.position.distance_to(character.position)
                characters_in_view.append({
                    "character": character.name,
                    "action": character.doing,
                    "position": f"{int(angle)} degrees / {int(distance)} meters"
                })
        return characters_in_view
    
    def memory():
        pass
    def reflection():
        pass
    def interaction():
        pass
    async def perception(self,event):
        data = f"""
"Here is your character data:
Your basic information: name:{self.name},gender:{self.gender},age:{self.age}
Your current position:{self.location}
you are currently doing:{self.doing}
Your personality:{self.personality}
Your current mental state:{self.mental_state}
Your attention level:{self.concertration} 
You may miss environmental changes if their significance is lower than your attention level.
Memory details:
long_term_memory:{self.long_term_memory}
life_memory:{self.life_memory}
short_term_memory:{self.short_term_memory}
Environment:
- Description: {self.environment.get_description()}
- Objects: {self.get_objects_in_view()}
- People: {self.get_characters_in_view()}
"""
    
        now = f"""
    memories right now(temp_memory):{self.temp_memory}
    new event:{event}
"""

        messages = [{"role": "system","content":prompt.perception_sys},{"role": "system","content":data},{"role": "system","content":now},{"role": "system","content":prompt.perception}]
        response = await json_request(messages)
        return response
    
    def get_description(self) -> str:
        return (f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}, "
                f"Position: {self.position}, Doing: {self.doing}")

class sys:
    def __init__(self):
        pass
    async def run(self,env:Environment):
        tasks = []
        for role in env.characters:
            if role.status:
                tasks.append(role.perception(role.event_temp))
        re = await asyncio.gather(*tasks)
        print(re)

time = TimeManager(datetime(2024,10,12,8,0,0))

room = Environment(name="room",description="Alice's room")
living_room = Environment(name="living_room",description="living_room")


door = Gate("door", Position(10, 10), "The door between Alice's room and living_room.", (room, living_room ))

tv = Item(name="tv",position=Position(1,2),description="an old tv")
bed = Item(name="bed",position=Position(0,0),description="Alice's bed")
table = Item(name="table",position=Position(-1,2),description="Alice's table")
chair = Item(name="chair",position=Position(-1,3),description="Alice's chair")
microwave = Item(name="microwave",position=Position(5,2),description="")
fridge = Item(name="fridge",position=Position(5,3),description="")

room.objects=[tv,bed,table,chair,door]
living_room.objects=[microwave,fridge,door]

character1 = Character(
    name="Alice",
    age=25,
    gender="male",
    environment=room,
    location="bed",
    position=Position(0,0),
    personality="extrovert",
    mental_state="normal",
    long_term_memory=[{'relationship': {'Emily': 'my girlfriend'}}, {'environment': 'I live in NYC, kitchen is next to my room'}, {'thought_about_Emily': 'she is a nice person'}, {'routine': 'go to living room and make breakfast'}, {'reminder': 'Finish math homework by today'}, {'goal': 'Practice basketball for at least an hour'}, {'challenges': 'Balancing schoolwork and basketball practice'}, {'proud_of': 'Maintaining good grades while being active in sports'}, {'values': 'Hard work, dedication, and maintaining relationships'}, {'self': 'I am a dedicated and hardworking individual who values relationships and strives to balance academics and sports'}],
    life_memory=[{'yesterday': 'Today was productive and fulfilling. I woke up early, had a good breakfast, and went to school. I stayed focused during math and science classes, enjoyed lunch with friends, and worked well on the history group project. After school, I relaxed, did my homework, practiced basketball, and ended the day with a nice dinner and some video games.', '2days_ago': 'I went to school and had math and science classes in the morning. During lunch, I hung out with my friends, and in the afternoon, we had a group project in history. After school, I did some homework and practiced basketball.', '3days_ago': 'I spent most of the day studying for a big biology exam. I also had basketball practice after school, which was pretty tiring.', 'old_days': 'Routine school days with classes, homework, basketball practice, and hanging out with friends. Helped a friend with math, worked on an English essay, and played video games.'}],
    short_term_memory=[{'thought': 'Remember to ask the teacher about the project'}, {'task': 'Study for the biology test next week'}, {'idea': 'Start working on the English presentation'}, {'plan': 'Meet friends after school tomorrow'}, {'tip': 'Stay focused during class discussions'}, {'schedule': '7:00 wake up, 8:00 eat breakfast, 9:00 go to school, 15:00 practice basketball, 18:00 dinner, 19:00 finish math homework'}]
    )


character2 = Character(
    name="Emily",
    age=24,
    gender="female",
    environment=room,
    location="bed",
    position=Position(0,0),
    personality="kind and empathetic",
    mental_state="content",

    long_term_memory=[{'relationship': {'Alice': 'my boyfriend'}}, {'environment': 'I live in Brooklyn, my favorite café is just around the corner'}, {'thought_about_Alice': 'he is so energetic and always brightens my day'}, {'values': 'honesty, compassion'}, {'beliefs': 'Love is about mutual respect and support'}, {'memory': 'I had a lovely dinner with Alice and ended the day with a peaceful walk together. Feeling happy and loved.'}, {'challenges': 'Balancing work and personal life can be tough, but I manage by staying organized and taking breaks when needed.'}, {'proud_of': 'Completing my presentation despite a busy day at work.'}, {'goal': 'Plan a weekend getaway with Alice.'}, {'self': 'I am a kind and empathetic person who values honesty and compassion. I believe in mutual respect and support in relationships. I strive to balance my work and personal life effectively.'}],
    life_memory=[{'yesterday': 'It was a wonderful day. I woke up excited to meet Alice later. Despite a busy day at work, I managed to stay focused and complete my presentation. I had a lovely dinner with Alice and ended the day with a peaceful walk together. Feeling happy and loved.', '2days_ago': 'I spent the evening with Alice, we went to the park and grabbed dinner at our favorite restaurant.', '3days_ago': 'I had a busy day at work, but Alice sent me a sweet message that made my day better.', 'old_days': "We've been together for almost two years now, sharing many memories—trips, dinners, late-night conversations. She's been a huge part of my life."}],
    short_term_memory=[{'reminder': "Buy Alice's favorite tea when I visit her today."}, {'task': 'Prepare the proposal for the meeting on Thursday.'}, {'idea': 'Plan a weekend getaway with Alice.'}, {'tip': 'Take a break when feeling overwhelmed at work.'}, {'schedule': '7:00 wake up, 8:00 eat breakfast, 9:00 go to work, 18:00 visit Alice, 20:00 relax at home'}]
)



async def main():
    system = sys()
    character1.status = True
    character1.event_temp.append("you woke up")
    character2.status = True
    character2.event_temp.append("you woke up")
    await system.run(room)


asyncio.run(main())


