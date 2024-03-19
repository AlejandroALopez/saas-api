import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import asyncio

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Plan Builder tests
system_prompt = "You are a plan builder that creates a list of tasks for a given goal and \
    max number of weeks. Always provide your result in JSON format."

goal = "Learn Python fundamentals"
max_weeks = 4

user_prompt = f"Goal: {goal}\nMax weeks: {max_weeks}"

# Function to get an array of tasks
functions = [
    {
        "name": "write_task",
        "description": "Shows the title, week number, and description of a task",
        "parameters": {
            "type": "object",
            "properties": {
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the task"
                            },
                            "week": {
                                "type": "number",
                                "description": "Week number of the task"
                            },
                        },
                        "required": ["title", "description", "week"]
                    }
                }
            },
            "required": ["tasks"]
        }
    }
]

# Creates a plan
# - Input: goal <string>, max_weeks <number>
# - Output: { "tasks": [ array of tasks ] }
async def make_plan(): 
    # invoke GPT API
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        functions=functions,
        function_call="auto",
        max_tokens=1000,
    )

    await asyncio.sleep(5) # tweek this

    json_object = json.loads(completion.choices[0].message.function_call.arguments)
    return json_object