# from urllib import request
from flask import Flask, request, jsonify
from flask_cors import CORS
from predictions import SalaryPrediction as sp
import json
import pandas as pd
import secrets
from dotenv import load_dotenv
import openai
import os


app = Flask(__name__)
CORS(app)

# Load .env file
load_dotenv()

# Load OpenAI API Key
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_nonce():
    return secrets.token_hex(16)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, PATCH, DELETE"
    return response

# @app.after_request
# def add_csp_header(response):
#     nonce = generate_nonce()
#     # response.headers["Content-Security-Policy"] = f"default-src 'self' http://go-motors.com:81; script-src 'nonce-{nonce}'"
#     response.headers["Content-Security-Policy"] = f"default-src 'self' https://go-motors.com:8443; script-src 'nonce-{nonce}'"
#     return response

# Store data into a python list for simplicity 

@app.get("/prediction")
def get_predictions():

    # data = request.get_json()

    puesto_pes = request.args.get('puesto_pes')
    escolaridad = request.args.get('escolaridad')
    tipo_puesto = request.args.get('tipo_puesto')
    subtipo_puesto = request.args.get('subtipo_puesto')
    nivel_jerarquico = request.args.get('nivel_jerarquico')
    subnivel_jerarquico = request.args.get('subnivel_jerarquico')
    sector_economico = request.args.get('sector_economico')
    exp_years = request.args.get('exp_years')
    edad_years = request.args.get('edad_years')


    respuesta = {
        'puesto_pes' : puesto_pes,
        'escolaridad' : escolaridad,
        'tipo_puesto' : tipo_puesto,
        'subtipo_puesto' : subtipo_puesto,
        'nivel_jerarquico' : nivel_jerarquico,
        'subnivel_jerarquico' : subnivel_jerarquico,
        'sector_economico' : sector_economico,
        'exp_years' : exp_years,
        'edad_years' : edad_years
    }

    # respuesta_json = json.dumps(respuesta)
    # respuesta_json = jsonify(respuesta)
    try:
        df = sp.getSalaryPrediction(respuesta) # Esto me retorna la predicción
        # records = df.to_json(orient='records')
        single_record = json.loads(df)[0]
        respuesta_json = json.dumps(single_record)
        return respuesta_json, 200

    except Exception as e:  # Catching all exceptions (not always recommended for all use cases)
        print(f"An error occurred: {e}")
        error = {'error': str(e)}  # Convert the error to string to ensure it's serializable
        return jsonify(error), 500
    

# Open AI EndPoint
@app.route("/puesto-pes-description")
# def get_completion(model="gpt-3.5-turbo"):
def get_completion(model="gpt-3.5-turbo-16k"):
    try:
        # job_title = request.form["job"]
        job_title = request.args.get('puesto_pes')
        messages = [{"role": "user", "content": gen_prompt(job_title)}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.5, # this is the degree of randomness of the model's output
        )
        
        # respuesta_json = json.dumps(response)
        result=response.choices[0].message.content
        # Save the JSON data to a file
        # with open("response_output.json", "w") as file:
        #     file.write(respuesta_json)

        return result, 200
    except Exception as e:
        print(f"An error occurred: {e}")
        error = {'error': str(e)}  # Convert the error to string to ensure it's serializable
        return jsonify(error), 500


def gen_prompt(text):
    prompt = f"""
    The output must be in spanish. The output must be HTML. The input could be in spanish or english.\
    If input is in english, translate it to spanish and then continue.\
    All labels MUST be type <p> <strong> no exception.\
    Start with a job description not using ```{text}``` in the description,  and label it as "Objetivo", with at least 50 words.\
    Continue with 8 to 10 key responsabilities and tasks for the position, and label it as "Responsabilidades Claves y Funciones"\
    using infinitive verbs and ellaborate on your answers for each key responsability.
    Each key point should be a bullet point and at least 20 words. \ 
    At the end, add the source of the information with italic font as "Fuente: OpenAI"
    ```{text}```
    """
    return prompt

if __name__ == "__main__":
        app.run(host='0.0.0.0', port='5000')


