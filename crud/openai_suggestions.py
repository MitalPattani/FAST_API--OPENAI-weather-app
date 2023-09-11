import os
import openai
import json
from dotenv import load_dotenv
from crud.weatherapi import get_weather_city

load_dotenv('.\.env')

OPENAI_key = os.environ.get("OPENAI_key")



openai.api_key=OPENAI_key


LLM_context = "You are a funny chatbot. Always respond in less than 100 words. \
      Always get the lastest weather parameters using the available function call."

LLM_max_token = 100

LLM_top_p = 0.9

LLM_Model = "gpt-3.5-turbo"

## Define OPENAI function
functions = [
        {
            "name": "get_weather_city",
            "description": "Get the weather parameters in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location e.g. San Francisco",
                    },
                    
                },
                "required": ["location"],
            },
        }
    ]

## Define Basic system character 
messages=[
    {
      "role": "system",
      "content": LLM_context
    }
]

## Generate response using basic OPENAI
async def generate_LLM_response(Location):
    messages.append(
    {"role": "user", "content":Location})

    completion = openai.ChatCompletion.create(
                model=LLM_Model,
                messages=messages,
                functions=functions,
                function_call="auto",
                top_p = LLM_top_p,
                max_tokens=LLM_max_token
                )
    response_message = completion["choices"][0]["message"]

    available_functions = {
        "get_weather_city":get_weather_city,
    }

    if "function_call" in response_message:
        func_name = response_message["function_call"]["name"]
        func_args = json.loads(response_message["function_call"]["arguments"])  

        function_to_call = available_functions[func_name]


        function_response = function_to_call(location= func_args.get("location"))
        messages.append(response_message)
        messages.append(
            {
                "role":"function",
                "name":func_name,
                "content": function_response
            }
        )

        second_response = openai.ChatCompletion.create(
                            model=LLM_Model,
                            messages=messages,
                            max_tokens=LLM_max_token,
                            top_p = LLM_top_p)
        
        ## Summary response
        messages_summ = messages+ [{"role": "user", "content":"Give a funny and informative summary of the weather"}]
        
        summary_response = openai.ChatCompletion.create(
                            model=LLM_Model,
                            messages=messages_summ,
                            max_tokens=LLM_max_token,
                            top_p = LLM_top_p)

        ## outfit recommendation response
        messages_summ = messages+ [{"role": "user", "content":"Give outfit recommendation based on weather!"}]
        
        outfit_response = openai.ChatCompletion.create(
                            model=LLM_Model,
                            messages=messages_summ,
                            max_tokens=LLM_max_token,
                            top_p = LLM_top_p)


        ## activity recommendation response
        messages_summ = messages+ [{"role": "user", "content":"Give activity recommendation based on weather!"}]
        
        activity_response = openai.ChatCompletion.create(
                            model=LLM_Model,
                            messages=messages_summ,
                            max_tokens=LLM_max_token,
                            top_p = LLM_top_p)


        suggestion = {}
        suggestion["city"] =  func_args.get("location")
        suggestion["weather_summary"] = summary_response['choices'][0]["message"]["content"]
        suggestion["activity_recommendation"] = activity_response['choices'][0]["message"]["content"]
        suggestion["outfit_recommendation"] = outfit_response['choices'][0]["message"]["content"]

        return suggestion
    else:
        return "No Such City!"




