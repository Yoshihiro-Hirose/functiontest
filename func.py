import openai
import json

def get_current_weather(location, unit="fahrenheit"):
    weather_info = {
        "location": location,
        "temperature": "30",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

functions=[
    {
        "name": "get_current_weather",
        "description": "指定した場所の現在の天気を取得する。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "都市名や地名、県名など",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]

model_name = "gpt-3.5-turbo-0613"

question = "東京都港区の天気を教えてください。"

response = openai.ChatCompletion.create(
    model=model_name,
    messages=[
        {"role": "user", "content": question},
    ],
    functions=functions,
    function_call="auto",
)
message = response["choices"][0]["message"]

function_name = message["function_call"]["name"]

arguments = json.loads(message["function_call"]["arguments"])
function_response = get_current_weather(
    location=arguments.get("location"),
    unit=arguments.get("unit"),
)

second_response = openai.ChatCompletion.create(
    model=model_name,
    messages=[
        {"role": "user", "content": question},
        message,
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
        },
    ],
)

print(second_response.choices[0]["message"]["content"].strip())
