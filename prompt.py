perception_sys="Forget all previous settings.select the next thing you want to do based on your character data following"

perception = """
Instructions:
1.generate every thing in first-person.

***Do the following step by step:***

1.base on all data,especially temp_memory and new event,select a target (object or person in environment) and decide what you want to do with it.
2.to do it,make an action.
3.If you and the selected object or person are not in the same position, your first action should be to walk toward them.
4.Make some memories about your decision, thoughts on the new event, etc.
5.Create a message. If the target is a person, the message will be said to them. If the target is an object, it’s your murmur; however, it can also be left blank.
6.If you’ve just ended a conversation, do not target the same person. Move on to something else.


Use JSON with keys: 
"target"(you can only select object or person in environment),"do"(what you are going to do in brief),"action","memory"(what you are going to do in details),"message"

Example of a valid JSON response for object:

if you want to continue what you are doing for a while,leave "continue" in key "action"(this only need to do on object)
```json
{
  "target":"table",
  "do":"study",
  "action":"continue",
  "memory":{"event":"","decision":"","thought":""},
  "message":""
  
}'''
Example of a valid JSON response for person:
```json
{
  "target":"Jack",
  "do":"talk",
  "action":"walk toward Jack",
  "memory":{"event":"","decision":"","thought":""},
  "message":"hi Jack."
}'''
"""