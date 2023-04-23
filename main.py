import webbrowser

import openai
import gradio as gr
import logging

import config as cf


openai.api_key = cf.key

# set up logging configuration
logging.basicConfig(level=logging.INFO)


def chat_completion(words, content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": words},
        ]
    )
    text = response.choices[0].message.content
    return text


def handle_input(audio):
    print(audio)

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    words = transcript['text'].split(maxsplit=1)

    logging.info('Instrucción: ' + words[0])

    logging.info('Propmpt: ' + words[1])

    if 'Dime' in words[0].capitalize():
        return chat_completion(words[1], "Eres un chatbot")
    elif 'Dibuja' in words[0].capitalize():
        response = openai.Image.create(
            prompt=words[1],
            n=1,
            size="1024x1024"
        )
        url = response['data'][0]['url']
        webbrowser.open(url)
        return 'Opening URL -> ' + url
    elif 'Traduce' in words[0].capitalize():
        split = transcript['text'].split(maxsplit=3)
        logging.info('Idioma: ' + split[2])
        return chat_completion(split[3], "Eres traductor, así que traduce esto al " + split[2])


ui = gr.Interface(fn=handle_input, inputs=gr.Image(), outputs=gr.outputs.Textbox())
ui.launch()
