This is a simple OPENAI chat bot that suggests the following 

- output = 
     {Location: City
        weather_summary: a funny weather weather_summary
        activity recommendation: activity recommendation as per weather
        outfit recommendation: Outfit recommendation as per weather}

- Model = chatgpt 3.5 - Turbo

- Input = City
- max_token = 100


- Add weatherAPI Key and openAI key to .env file

- Install requirements file
     --pip install -r requirements.txt

To start the codebase please run the following command
     --uvicorn main:app


API Url = http://127.0.0.1:8000/weather/{City}

