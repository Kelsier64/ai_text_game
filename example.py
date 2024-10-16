import math
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict


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

    def update_characters(self):
        """Method to update the characters in the environment dynamically."""
        # Any additional logic to handle character updates in the environment.
        for character in self.characters:
            print(f"Character {character.name} is currently in {self.name}")

    def get_description(self) -> str:
        return (f"Environment: {self.name}, Description: {self.description}, "
                f"Weather: {self.weather}, Temperature: {self.temperature}°C")




class Character(Describable):
    """Represents a character with attributes like personality, memory, etc."""
    
    def __init__(self, name: str, age: int, gender: str, environment: Environment,
                 position: Position, personality: str, mental_state: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.environment = environment
        self.position = position
        self.hunger = 100
        self.facial_expression = "neutral"
        self.doing = "idle"
        self.personality = personality
        self.mental_state = mental_state
        self.long_term_memory: List[str] = []
        self.short_term_memory: List[str] = []
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
    def get_description(self) -> str:
        return (f"Character: {self.name}, Age: {self.age}, Gender: {self.gender}, "
                f"Position: {self.position}, Doing: {self.doing}")


# 創建時間管理器
time_manager = TimeManager()

# 創建兩個環境
env1 = Environment("Forest", "A dense forest with fog.")
env2 = Environment("Castle", "A large stone castle.")

# 創建一個門，連接兩個環境
gate = Gate("Main Gate", Position(50, 50), "The gate between forest and castle.", (env1, env2))

# 創建一個物品
sword = Item("Sword", Position(10, 10), "A sharp steel sword.")
env1.add_object(sword)

# 創建角色
character1 = Character("Aragorn", 35, "Male", env1, Position(0, 0), "Brave", "Calm", time_manager)
character2 = Character("haha", 35, "Male", env1, Position(-2, -1), "Brave", "Calm", time_manager)
# 角色與物品互動
breakpoint()
character1.interact_with_item(sword)

# 角色穿過門進入另一個環境
character1.go_through_gate(gate)

# 更新環境中的角色
env2.update_characters()

print(character1.get_description())
print(env2.get_description())

breakpoint()