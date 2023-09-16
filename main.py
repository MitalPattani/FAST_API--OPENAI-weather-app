import pandas as pd
from fastapi import FastAPI, Query
# import crud.openai_suggestions as crud_openai
import crud.langchain_implement as crud_langchain
import os

app = FastAPI()


# ## Get API to call the LLM Chatbot

# @app.get("/weather/{Location}")
# async def get_weather_city(Location: str):
    
#     response = await crud_openai.generate_LLM_response(Location)
#     return response




## Get API to call langchain LLM Chatbot


@app.get("/weather/{Location}")
async def get_weather_city(Location: str):
    
    response = await crud_langchain.generate_LLM_response(Location)
    return response

