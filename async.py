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
    
    def __init__(self):
        self.current_time = datetime.now()

    def update_time(self, new_time: datetime):
        self.current_time = new_time

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

    def add_object(self, obj: WorldObject):
        self.objects.append(obj)

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
target:{request["target"]}
want to do:{request["do"]}
action:{request["action"]}
"""
        functions = """
    function you have:
    {"function":"goto"}(ex:"doing":"study"),
    {"function":"sleep"},
    {"function":"enter"}(ex:"message":"you enter the living room","doing":"stand by the door"),
    {"function":"pass"}
"""         
        messages = [prompt.system,{"role": "system","content":data},{"role": "system","content":functions},{"role": "system","content":prompt.instruction}]
        response = await json_request(messages)
        return response
       

    def get_description(self) -> str:
        return (f"Environment: {self.name}, Description: {self.description}, "
                f"Weather: {self.weather}, Temperature: {self.temperature}°C")

class Character(Describable):
    """Represents a character with attributes like personality, memory, etc."""
    
    def __init__(self, name: str, age: int, gender: str, environment: Environment, position: Position, personality: str, mental_state: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.environment = environment
        self.position = position
        self.location = ""
        self.hunger = 100
        self.concertration = 0
        self.facial_expression = "neutral"
        self.doing = "idle"
        self.personality = personality
        self.mental_state = mental_state
        self.long_term_memory: List[str] = []
        self.short_term_memory: List[str] = []
        self.life_memory: List[str] = []
        self.temp_memory: List[str] = []
        self.environment.add_character(self)

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
Your current position:{self.position}
you are currently doing:{self.doing}
Your personality:{self.personality}
Your current mental state:{self.mental_state}
Your attention level:{self.concertration} 
You may miss environmental changes if their significance is lower than your attention level.
Memory details:
long_term_memory:{self.long_term_memory}
life_memory:{self.life_memory}
short_term_memory:{self.short_term_memory}
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



time_manager = TimeManager()

env1 = Environment("Forest", "A dense forest with fog.")
env2 = Environment("Castle", "A large stone castle.")


gate = Gate("Main Gate", Position(50, 50), "The gate between forest and castle.", (env1, env2))


sword = Item("Sword", Position(10, 10), "A sharp steel sword.")
env1.add_object(sword)


character1 = Character("Aragorn", 35, "Male", env1, Position(0, 0), "Brave", "Calm")
character2 = Character("haha", 35, "Male", env1, Position(-2, -1), "Brave", "Calm")


# re = asyncio.run(character1.perception("you woke up"))

asyncio.run(env1.item_interaction(character1,{"target":"","do":"","action":""}))



