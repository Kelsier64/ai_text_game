perception_sys="Forget all previous settings.you are a character in a life simulator,select the next thing you want to do based on your character data and instruction following"

temp_sum_sys="Forget all previous settings.you are a character in a life simulator,update your memory based on your character data and instruction following"

system="""you are a system of a life simulator game. Please generate responsesbased on the following data and instructions.
parameter explanation:
position,absolute position.
description,include description of character or object's position,appearance or character's facial expression and what he doing now,etc.
"""

perception = """
Instructions:
1.generate every thing in first-person.
***Do the following step by step:***
base on all data,react to the new event.
first,select a target (object or person in environment)

if you selected an object:
1.decide what you want to do to it.
2.to do it,make an action.
3.If you and the selected object are not in the same position, your first action should be walk toward it.
4.Make some memories about your decision, thoughts, etc on the new event.
5.the message,it is your murmur,no one can hear,it only say to yourself; however,it can also be left blank.
6.if you want to keep doing it for a while,set a clock for it,output how many minutes you want to set;however,for immediate actions(walking or speaking,etc),do not set a clock,output 0.
if you selected a person:
1.the temp_memory is the previous conversation just now.
2.you only can do interactional action,you CAN NOT go anywhere.
3.If you and the selected person are not in the same position, your first action should be to walk toward him.
4.Make some memories about your decision, thoughts, etc on the new event.
5.Create a message.the message will be said to them; however, it can also be left blank.
6.DO NOT repeat the new event or temp_memory
***
DO NOT always continue the conversation.select an object instead of a person to end the conversation and do next thing.
***

Use JSON with keys: 
"target"(you can only select object or person in environment),"do"(what you are going to do in brief),"action","memory","message","keep"
Example of a valid JSON response for object:

```json
{
  "target":"table",
  "do":"study",
  "action":"sit down and study",
  "memory":"",
  "message":"",
  "clock":60
}'''
Example of a valid JSON response for person:
```json
{
  "target":"Jack",
  "do":"talk",
  "action":"walk toward Jack",
  "memory":"",
  "message":"hi Jack."
  "clock":0 (target is person,always "clock":0)
}'''
"""
temp_sum="""
***Do the following step by step:***
1.base on temp memory,sum up what have you done in detail.
2.temp memory will be cleared,so remember some thing important,update it into short_term_memory.
3.update memory in short_term_memory if need,or there is something need to be remembered.
Response Format:
Use JSON with keys:"done","short_term_memory"

Example of a valid JSON response:
```json
{
    "done":"sum up what have you done",
    "short_term_memory":[{json},{json},{json}]
}'''
"""

item = """
Instructions:
only do what character request.
***Do the following step by step:***
1.base on data,select an appropriate function to use.if no suitable function,respond with "execute":{"function":"pass"}
2.whether you pass the function or not,generate a message telling the requester that his action has been completed (in the first-person perspective).
3.ganerate the "event" to tell eneryone in this environment what happened(in third-person perspective).
4.update what the requester is doing now in brief(in third-person perspective,only action no name of requester).
Response Format:
Use JSON with keys: "execute","message","event","doing"
Example of a valid JSON response:
```json
{
    "execute":{"function":"goto"},
    "message":"you walk to the table and sit down",
    "event":"",
    "doing":"study"
}'''
"""

object_update = """
Instructions:
***Do the following step by step:***
1.base on instruction,update the data of the target.
2.add or subtract the data,do not replace it.
Response Format:
Use JSON with keys:"absolute_position","description","informations","functions"
Example of a valid JSON response:
```json
{
    "absolute_position":"(x,y)"
    "description":""
    "informations":""
    "functions":""
}'''
"""
character_update = """
Instructions:
***Do the following step by step:***
1.base on instruction,update the data of the target.
2.add or subtract the data,do not replace it.
Response Format:
Use JSON with keys:"absolute_position","description","inventory","environment"
Example of a valid JSON response:
```json
{
    "absolute_position":"(x,y)"
    "description":""
    "inventory":""
    "environment":""
}'''
"""
target = """
1. Based on the user's action and the target's function, **select the objects or characters that need to be updated**.
2. For each selected object or character, **generate commands to instruct the system on how to update** the data in detail. Ensure you:
   - Use `description_now` to correctly identify the target,give me the description now and DO NOT modify it.
   - If modifying an object,instruct updating its position,description,which include description of position and appearance,etc.
   - If modifying a character,instruct updating its position,environment,item_list,and description,which include description of position, appearance, facial expression, and current action,etc.

3. **Generate a message for the user in first-person perspective**, confirming their action is completed.
4. **Generate an "event" in third-person perspective**, detailing what occurred for all others in the environment.

**Response Format:**
Respond in JSON format with keys: `"objects"`, `"characters"`, `"message"`, and `"event"`. Here’s a template to follow:

```json
{
    "objects": [
        {"name": "object_name", "description_now": "object_description_now", "instruction": "object_update_instruction"},
        {"name": "object_name", "description_now": "object_description_now", "instruction": "object_update_instruction"}
        ...
    ],
    "characters": [
        {"name": "character_name", "description_now": "character_description_now", "instruction": "character_update_instruction"},
        {"name": "character_name", "description_now": "character_description_now", "instruction": "character_update_instruction"}
        ...
    ],
    "message": "User's confirmation message here",
    "event": "Event message for others here"
}
"""


role = """
Instructions:
only do what character request.
***Do the following step by step:***
1.Based on the provided data, generate a message from the target's perspective that tells them what happened, describing the requester's behavior and what he said. (Do not edit the words the requester said; just add some description before it)
2.Update what the requester is doing in very brief terms (in third-person perspective).
3.ganerate the "event" to inform everyone in the environment what happened,describing the requester's behavior and what he said(Do not edit the words the requester said; just add some description before it)
Response Format:s
Use JSON with keys:"message","doing","event"
Example of a valid JSON response:
```json
{
    "message":"Evan smiled and said to me:'good morning'",
    "event":"Evan smiled and says to Jack:'good morning",
    "doing":"talking to Jack"
}'''
"""