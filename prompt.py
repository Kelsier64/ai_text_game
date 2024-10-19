perception_sys="Forget all previous settings.select the next thing you want to do based on your character data following"

system="you are a system of a game. Please generate responses based on the following data and instruction"


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
5.Create a message.it is your murmur; however, it can also be left blank.
6.if you want to keep what you are doing attentively for a while,leave "yes" in key "attentively"(this only works on object)

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
  "keep":"yes"
}'''
Example of a valid JSON response for person:
```json
{
  "target":"Jack",
  "do":"talk",
  "action":"walk toward Jack",
  "memory":"",
  "message":"hi Jack."
  "keep":"no" (target is person,always "keep":"no")
}'''
"""

item = """
Instructions:
only do what character request.
***Do the following step by step:***
1.base on data,select an appropriate function to use.if no suitable function,respond with "execute":{"function":"pass"}
2.whether you pass the function or not,generate a message telling the requester that his action has been completed (in the first-person perspective).
3.ganerate the "event" to tell eneryone in this environment what happened(in third-person perspective).
4.update what the requester is doing now in brief(in third-person perspective).
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

role = """
Instructions:
only do what character request.
***Do the following step by step:***
1.base on data,generate a message for target to tell him what happened,conbine requester"s action,message,and other details in target's perspective(do not edit the message).
2.update what the requester is doing in very brief(in third-person perspective).
3.ganerate the "event" to tell eneryone in this environment what happened,conbine requester"s action,message,and other details but in third-person perspective(do not edit the message).
Response Format:
Use JSON with keys:"message","doing","event"
Example of a valid JSON response:
```json
{
    "message":"Evan said to me:'good morning'",
    "event":"Evan said to Jack:'good morning",
    "doing":"talking to Jack"
}'''
"""