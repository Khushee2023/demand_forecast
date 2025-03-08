#routes.py
from flask import Blueprint, request, jsonify
import requests
from model1 import predict as predict_price
from model2 import predict as predict_demand
from model3 import predict as predict_production

api_blueprint = Blueprint('api', __name__)

OPENWEATHER_API_KEY = 'f8eecee3f82a3ee3e9f0e4123b8c7bd7'

@api_blueprint.route('/predict', methods=['POST'])
def predict():
    data = request.json
    location = data['location']
    timestamp = data['timestamp']

    weather_data = fetch_weather_data(location, timestamp)

    features = extract_features(weather_data)

    demand = predict_demand(features)
    production = predict_production(features)
    price = predict_price(features)

    surplus = production - demand
    calculated_price = demand / 300

    return jsonify({
        'energy_demand': demand,
        'energy_produced': production,
        'surplus': surplus,
        'price': calculated_price
    })

def fetch_weather_data(location, timestamp):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={OPENWEATHER_API_KEY}'
    response = requests.get(url)
    data = response.json()
    # Extract necessary fields from the API response
    return data

def extract_features(weather_data):
    # Extract and transform weather features based on API response
    features = [
        weather_data['temperature'],
        weather_data['feels_like'],
        weather_data['humidity'],
        weather_data['pressure'],
        weather_data['wind_speed'],
        weather_data['wind_direction'],
        weather_data['cloud_coverage'],
        weather_data['precipitation']
    ]
    return features
