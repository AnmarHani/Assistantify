import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import requests
import os
import pygame
import uuid
import matplotlib.pyplot as plt
import pandas as pd

from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def setup_openai_client():

    return openai.OpenAI(api_key=OPENAI_API_KEY)

def transcribe_audio(client, audio_path):

    with open(audio_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

def fetch_ai_response(client, input_text, session_state):
    if 'chat_history' not in session_state:
        session_state['chat_history'] = [{
            "role": "system", 
            "content": "You are now connected to Assistantify. How can I assist you today?"
        }]
    session_state['chat_history'].append({
        "role": "user", 
        "content": input_text
    })



    messages = [{"role": msg["role"], "content": msg["content"]} for msg in session_state['chat_history']]
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
    assistant_response = response.choices[0].message.content
    session_state['chat_history'].append({
        "role": "assistant", 
        "content": assistant_response
    })
    return assistant_response

def text_to_audio(client, text, audio_path):
    """Converts text to audio using OpenAI's TTS and automatically plays it using pygame."""
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=text)
    response.stream_to_file(audio_path)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def authenticate(url, data):
    
    response = requests.post(url, json=data)
    return response.json() if response.status_code == 200 else None

def show_login_form():
  
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        token = authenticate("http://localhost:8000/login", {"username": username, "password": password})
        if token:
            st.session_state['token'] = token['access_token']
            st.session_state['page'] = 'audio'  # Default to audio on login
            st.rerun()
        else:
            st.sidebar.error("Incorrect username or password")

def main_app():
    choice = st.sidebar.radio("Choose an interaction type:", ['Audio Interaction', 'Chat Interaction', 'Food Info', 'Weather'])
    if choice == 'Audio Interaction':
        audio_interaction()
    elif choice == 'Chat Interaction':
        chat_interaction()
    elif choice == 'Food Info':
        show_food_info()
    elif choice == 'Weather':
        weather_info()


def audio_interaction():
    
    recorded_audio = audio_recorder()
    if recorded_audio:
        audio_file = f"audio_{uuid.uuid4()}.mp3"
        with open(audio_file, "wb") as f:
            f.write(recorded_audio)
        transcribed_text = transcribe_audio(setup_openai_client(), audio_file)
        st.write("Transcribed text:", transcribed_text)
        ai_response = fetch_ai_response(setup_openai_client(), transcribed_text, st.session_state)
        response_audio_file = f"response_audio_{uuid.uuid4()}.mp3"
        text_to_audio(setup_openai_client(), ai_response, response_audio_file)

def chat_interaction():
  """Handles the chat interaction part of the application."""
  with st.container():
    user_input = st.text_input("You:", key="user_input")
    send_button = st.button('Send')

  if send_button:
    if 'chat_history' not in st.session_state:
      st.session_state['chat_history'] = []

   
    if user_input.strip():
      # Fetch the response only once
      ai_response = fetch_ai_response(setup_openai_client(), user_input, st.session_state)


      if len(st.session_state['chat_history']) == 0 or ai_response != st.session_state['chat_history'][-1]['content']:
 
        st.session_state['chat_history'].append({
          "role": "assistant",
          "content": ai_response
        })

  if 'chat_history' in st.session_state:
    for message in st.session_state['chat_history']:
      st.write(f"{message['role']}: {message['content']}", key=f"message-{message['role']}-{message['content']}")






def calculate_goodness(nutrition_info):
    health_labels = set(nutrition_info.get("healthLabels", []))
    # List of labels considered 'good'
    good_labels = {"VEGAN", "VEGETARIAN", "PESCATARIAN", "PALEO", "DAIRY_FREE", "GLUTEN_FREE"}
    relevant_labels = health_labels.intersection(good_labels)
    # For a more meaningful percentage, consider the proportion of good labels found to all good labels possible
    if good_labels:
        goodness_percentage = (len(relevant_labels) / len(good_labels)) * 100
    else:
        goodness_percentage = 0
    return goodness_percentage

def display_nutrition_info(nutrition_info):
    st.subheader("Nutrition Information")
    st.write("Calories:", nutrition_info.get("calories", "Not available"))
    st.write("Total Weight:", nutrition_info.get("totalWeight", "Not available"))
    
    # Displaying diet labels
    diet_labels = ", ".join(nutrition_info.get("dietLabels", []))
    st.write("Diet Labels:", diet_labels if diet_labels else "No diet labels available")
    
    # Displaying health labels
    health_labels = ", ".join(nutrition_info.get("healthLabels", []))
    st.write("Health Labels:", health_labels if health_labels else "No health labels available")
    
    # Displaying ingredient details
    ingredients = nutrition_info.get("ingredients", [])
    if ingredients:
        st.subheader("Ingredients Detail")
        for idx, ingredient in enumerate(ingredients, 1):
            st.markdown(f"**Ingredient {idx}**")
            st.write("Food ID:", ingredient.get("foodId", "Not specified"))
            st.write("Quantity:", ingredient.get("quantity", "Not specified"))
            st.write("Measure:", ingredient.get("measure", {}).get("label", "Not specified"))
            st.write("Weight (g):", ingredient.get("weight", "Not specified"))
            st.write("Food:", ingredient.get("food", {}).get("label", "Not specified"))
            st.write("Food Category:", ingredient.get("foodCategory", "Not specified"))
    else:
        st.write("No detailed ingredient information available.")

    # Handling cautions
    cautions = ", ".join(nutrition_info.get("cautions", []))
    st.write("Cautions:", cautions if cautions else "No specific cautions")



def show_food_info():
    st.title("Food Nutrition Analyzer")
    food_name = st.text_input("Enter the food you want to analyze:")
    food_weight = st.number_input("Enter the weight in grams (g):", min_value=0, format='%d')
    analyze_button = st.button("Analyze")

    if analyze_button and food_name and food_weight > 0:
        # Combine the food name and weight
        food_query = f"{food_weight}g {food_name}"
        nutrition_info = get_nutrition_info(food_query)

        # Check for allergies
        check_allergy_response = check_allergies(food_name)
        if check_allergy_response['message'].startswith("Alert"):
            alert_message = "Alert: You cannot eat this food. You have allergies from it."
            st.error(alert_message)
            # Using existing text_to_audio function to alert the user
            response_audio_file = f"alert_{uuid.uuid4()}.mp3"
            text_to_audio(setup_openai_client(), alert_message, response_audio_file)

        if nutrition_info:
            display_nutrition_info(nutrition_info)
            goodness_percentage = calculate_goodness(nutrition_info)
            st.subheader("Goodness Percentage")
            st.write(f"The food is {goodness_percentage:.2f}% good.")

            # Display the pie chart
            chart_data = pd.Series([goodness_percentage, 100-goodness_percentage], index=["Good", "Not Good"])
            st.pyplot(chart_data.plot.pie(autopct='%.1f%%', startangle=90, colors=['green', 'red'], labels=["Good", "Not Good"]).get_figure())

def check_allergies(food_name):
    url = "http://localhost:8000/check_allergies"
    headers = {
        "Authorization": f"Bearer {st.session_state['token']}",
        "Content-Type": "application/json"
    }
    payload = {"food": food_name}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to check allergies: {response.status_code} {response.text}")
        return None
    
def get_nutrition_info(food_query):
    url = "https://api.edamam.com/api/nutrition-data"
    app_id = "2ec85e11"
    app_key = "e95f3d98d3286ca952b533180c077030"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "ingr": food_query
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def fetch_weather_info(location):
    api_key = "59daf3b3bfd9e552fe741ed78a3714bd"  # Your API key (Be cautious with it)
    base_url = "http://api.weatherstack.com/current"
    params = {
        'access_key': api_key,
        'query': location,
        'units': 'm'  # Metric units
    }
    response = requests.get(base_url, params=params)
    return response.json()

def weather_info():
    st.subheader("Weather Information")
    location = st.text_input("Enter the location for weather information:", "New York")
    if st.button("Get Weather"):
        weather_data = fetch_weather_info(location)
        if 'current' in weather_data:
            current_weather = weather_data['current']
            weather_details = f"Current temperature in {location} is {current_weather['temperature']}°C, " \
                              f"with {current_weather['weather_descriptions'][0]}. " \
                              f"Humidity is at {current_weather['humidity']}%."
            st.write(weather_details)
            
            # Using text_to_audio to announce weather
            response_audio_file = f"weather_{uuid.uuid4()}.mp3"
            text_to_audio(setup_openai_client(), weather_details, response_audio_file)
        else:
            st.error("Failed to retrieve weather data.")

def main():

    st.title("Welcome to Assistantify")
    if 'token' not in st.session_state:
        show_login_form()
    else:
        main_app()


if __name__ == "__main__":
    main()
