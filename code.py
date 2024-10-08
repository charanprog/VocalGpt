!pip install -q git+https://github.com/openai/whisper.git
!pip install -q gradio
!pip install -q openai
!pip install -q gTTS
import whisper
import gradio as gr
import time
import warnings
import json
import openai
import os
from gtts import gTTS
import subprocess

command = "ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 10 -q:a 9 -acodec libmp3lame Temp.mp3"

warnings.filterwarnings("ignore")
openai.api_key = "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"
model = whisper.load_model("base")
model.device
subprocess.run(command, shell=True)
def chatgpt_api(input_text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": input_text},]

    if input_text:
        messages.append(
            {"role": "user", "content": input_text},
        )
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat_completion.choices[0].message.content
    return reply

def transcribe(audio):

    language = 'en'

    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)

    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    result_text = result.text

    out_result = chatgpt_api(result_text)

    audioobj = gTTS(text = out_result,
                    lang = language,
                    slow = False)

    audioobj.save("Temp.mp3")

    return [result_text, out_result, "Temp.mp3"]

output_1 = gr.Textbox(label="My Input")
output_2 = gr.Textbox(label="Output")
output_3 = gr.Audio("Temp.mp3")

gr.Interface(
    title = 'MyChatBot',
    fn=transcribe,
    inputs=[
        gr.inputs.Audio(source="microphone", type="filepath")
    ],

    outputs=[
        output_1,  output_2, output_3
    ],
    ).launch(share =True ,debug = True )
