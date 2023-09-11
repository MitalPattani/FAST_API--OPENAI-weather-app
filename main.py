import pandas as pd
from fastapi import FastAPI, Query
import crud.openai_suggestions as crud
import os

app = FastAPI()


## Get API to call the LLM Chatbot

@app.get("/weather/{Location}")
async def get_weather_city(Location: str):
    
    response = await crud.generate_LLM_response(Location)
    return response

