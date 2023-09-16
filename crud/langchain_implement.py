
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

import os

from crud.weatherapi import get_weather_API, get_outfit_recomendation, get_activity_recomendation

from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import StructuredTool
from langchain.prompts import ChatPromptTemplate
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
import json
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

from langchain.schema import SystemMessage


# llm = OpenAI(openai_api_key=OPENAI_key)
load_dotenv('.\.env')

OPENAI_key = os.environ.get("OPENAI_key")

LLM_max_token = 100
LLM_top_p = 1.2
LLM_Model = os.environ.get("LLM_Model")



async def generate_LLM_response(Location):

    # llm_chain = LLMChain(llm=llm, prompt=prompt)

    llm = ChatOpenAI(openai_api_key=OPENAI_key,temperature=LLM_top_p, model=LLM_Model)


    template_string = """You are a sarcastic funny chatbot that give funny description based on the data from the tools.

        Take the Location below delimited by triple backticks and get the weather details from the weatherapi using the tool,

        location: ```{location}```

        Give the following results using weather data,
        name of the location
        Funny description of the current weather, 
        a creative activity recomendation, 
        a quirky outfit recommendation         

        Format the output as JSON with the following keys:
        location
        weather_summary
        activity_recommendation
        outfit_recommendation
        """


    prompt_template = ChatPromptTemplate.from_template(template=template_string)


    tools = [
        StructuredTool.from_function(
            name = "get_weather_API",
            func=get_weather_API,
            description="useful for weather forcasting"
        ),
        StructuredTool.from_function(
            name="get_activity_recomendation",
            func=get_activity_recomendation,
            description="useful to suggest activity based on given data"
        ),
        StructuredTool.from_function(
            name="get_outfit_recomendation",
            func=get_outfit_recomendation,
            description="useful to get the outfit based on given data"
        )
    ]

    ## Simple agent that generates results using the given functions
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)


    return agent.run(prompt_template.format_messages(location=Location))

