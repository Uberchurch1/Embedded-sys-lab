from ollama import chat
from pydantic import BaseModel
from typing import List

class color(BaseModel):
    color1: str
    colpercent1: int

class colorList(BaseModel):
    colors: List[color]

response = chat(
    messages=[
        {
            'role': 'user',
            'content': 'List the names and percentages of colors of paint needed to make the color purple',
        }
    ],
    model='llama3.2',
    format=colorList.model_json_schema(),  # Expecting a list format
)

paint_colors = colorList.model_validate_json(response.message.content)

print(paint_colors)