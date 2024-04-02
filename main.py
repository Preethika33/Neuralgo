import os
import librosa
import numpy as np
import requests

import os
from lyzr import VoiceBot
vb = VoiceBot(api_key="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")



def transcript():
    for i in os.listdir("Call Data Sample"):
        path = os.path.join("Call Data Sample", i)
        print(f"Processing {i}")
        transcript = vb.transcribe(path)

        with open(f"Output/{i[:-4]}.txt", "w", encoding="utf8") as f:
            f.write(transcript)
        return transcript
    
print(transcript)

def calculate_silence_ratio(audio_file):
    audio, sr = librosa.load(audio_file, sr=None)

    energy = librosa.feature.rms(y=audio)

    energy_db = librosa.amplitude_to_db(energy)

    silence_threshold_db = -60

    silent_segments = np.where(energy_db < silence_threshold_db, 1, 0)

    total_silence_duration = np.sum(silent_segments) / sr

    total_duration = librosa.get_duration(y=audio, sr=sr)
    
    silence_ratio = total_silence_duration / total_duration

    return silence_ratio

total_duration = 0
count = 0
def calculate_AHT(audio_file):
    global total_duration, count

    audio, sr = librosa.load(audio_file, sr=None)
    
    duration = librosa.get_duration(y=audio, sr=sr)

    total_duration += duration
    count += 1
    return total_duration/count

API_KEY = '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'
API_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
def fcr(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(API_KEY)
    }
    data = {
        'model': 'gpt-3.5-turbo',  
        'messages': [{'role': 'user', 'content': message}],
    }
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return 'Error: {}'.format(response.text)


def error_data(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(API_KEY)
    }
    data = {
        'model': 'gpt-3.5-turbo',  
        'messages': [{'role': 'user', 'content': message}],
    }
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return 'Error: {}'.format(response.text)


def csat(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(API_KEY)
    }
    data = {
        'model': 'gpt-3.5-turbo',  
        'messages': [{'role': 'user', 'content': message}],
    }
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return 'Error: {}'.format(response.text)
    
def call_transfer(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(API_KEY)
    }
    data = {
        'model': 'gpt-3.5-turbo',  
        'messages': [{'role': 'user', 'content': message}],
    }
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return 'Error: {}'.format(response.text)

    
def recallll(audio_dir):
    res = ""

    for audio_file in os.listdir(audio_dir):
        audio_path = os.path.join(audio_dir, audio_file)
        print(f"Processing {audio_file}")

        audio_txt = transcript()

        fcr_prompt = f"""
        First Call Resolution (FCR): Indicates the percentage of calls resolved on the first 
        interaction, showcasing the agent's ability to solve issues efficiently without follow up.
        in a folder the audio which was discussed by problem we want to find whether the problem is solved or not .
        {audio_txt}
        give output in single word.
        """
        response = fcr(fcr_prompt)
        res += " FCR: {}".format(response)

        error_data_prompt = f"""
        Error Rate: The frequency of errors made by agents during calls, such as providing 
        incorrect information or failing to follow proper protocols
        ---------------------------------
        {audio_txt}
        ---------------------------------
        calculate the error where the sentence that should be corrected while talking and find how many times it should be corrected.
        And give just  single numbers how many times it should be corrected.
        just give sigle number .not a sentences.
        """
        response = error_data(error_data_prompt)
        res += " Error_data: {}".format(response)

        csat_prompt = f"""
        Customer Satisfaction Score (CSAT): A metric derived from customer feedback 
        post-call, reflecting the customer's satisfaction with the service received.
        rate a scale from 1 to 5 due to the customers satisfactions in decimal numbers. 
        The given document can be in other languages. Manage accordingly.
        ---------------------------------
        {audio_txt}
        ---------------------------------
        give the output in a single number.
        """
        response = csat(csat_prompt)
        res += " csat: {}".format(response)

        call_transfer_prompt = f"""
        Call Transfer Rate: Measures how often calls are transferred to another agent or 
        department, which can indicate the need for better first-contact resolution or agent 
        training.
        ---------------------------------
        {audio_txt}
        ---------------------------------
        check if the call is transfered or not . in the above sentence
        If transfered means give 1 and not transfered means give 0.
        just give sigle number .not a sentences.
        """
        response = call_transfer(call_transfer_prompt)
        res += " Call_transfer: {}".format(response)
        
        ratio = calculate_silence_ratio(audio_path)
        AHT = calculate_AHT(audio_path)

        res += f" Silence Ratio: {ratio}"
        res += f" AHT: {AHT}"

        res += "\n"

    return res
