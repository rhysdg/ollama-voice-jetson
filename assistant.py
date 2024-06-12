from piper.voice import PiperVoice
from sshkeyboard import listen_keyboard, stop_listening
import queue
import os
import sys
import json
import wave
import time
import requests
import soundfile
import alsaaudio
import yaml
import numpy as np
import whisper
import logging
import threading
import queue
import sounddevice as sd
import numpy as np

##otherwise pointer error
import torch
import pyaudio

from whisper.model import load_model, available_models
from whisper.audio import SAMPLE_RATE, N_FRAMES, HOP_LENGTH, pad_or_trim, log_mel_spectrogram
from whisper.decoding import DecodingOptions, DecodingResult
from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE, get_tokenizer
from whisper.utils import exact_div, format_timestamp, optional_int, optional_float, str2bool, write_txt, write_vtt, write_srt
from whisper.transcribe import transcribe



# Configure logging
logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s')


INPUT_DEFAULT_DURATION_SECONDS = 5
#INPUT_FORMAT = pyaudio.paInt16

#Respeaker mic array v2 only
INPUT_FORMAT = pyaudio.paInt16
INPUT_CHANNELS = 1
INPUT_RATE = 16000
INPUT_CHUNK = 16000*5
OLLAMA_REST_HEADERS = {'Content-Type': 'application/json'}
INPUT_CONFIG_PATH ="assistant.yaml"
##chane this to your own device
INPUT_DEVICE = 36

class Assistant:
    def __init__(self):

        self.config = self.init_config()   
        self.audio = pyaudio.PyAudio()

        ######piper setup - changing to a private setup method shortly
        
        voicedir = "./voices/" #Where onnx model files are stored on my machine
        model = voicedir+"en_GB-alba-medium-sim.onnx"
        self.voice = PiperVoice.load(model, use_cuda=False)
        self.tts_stream = sd.OutputStream(samplerate=self.voice.config.sample_rate, channels=1, dtype='int16')

        try:
            self.audio_stream = self.audio.open(format=INPUT_FORMAT,
                            channels=INPUT_CHANNELS,
                            rate=INPUT_RATE,
                            input=True,
                            start=False,
                            input_device_index=INPUT_DEVICE,
                            )
        except Exception as e:                                            
            logging.error(f"Error opening audio stream: {str(e)}")
            self.wait_exit()

        self.model = load_model('small.en')

        self.context = []
        self.frames = []
        self.released=False
        self.terminate=False

        ##adding as a covert model warmup - otherwsie first pass is slow
        self.ask_ollama('wake up mini bee', self.text_to_speech)
        
  

    def get_pressed(self, key):
        self.key = key
    
        if self.key == 'space':
            while not self.terminate:
                data = self.audio_stream.read(1024)
        
                self.frames.append(data)


    
    def get_release(self, key):

        if self.key == 'space':
           
            self.released = True
            self.terminate=True
        
            stop_listening()
            
         

    def wait_exit(self):
        while True:
            self.display_message(self.config.messages.noAudioInput)
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    self.shutdown()

    def shutdown(self):
        logging.info("Shutting down Assistant")
        self.audio.terminate()
        pygame.quit()
        sys.exit()

    def init_config(self):
        #logging.info("Initializing configuration")
        class Inst:
            pass

        with open('assistant.yaml', encoding='utf-8') as data:
            configYaml = yaml.safe_load(data)

        config = Inst()
        config.messages = Inst()
        config.messages.loadingModel = configYaml["messages"]["loadingModel"]
        config.messages.pressSpace = configYaml["messages"]["pressSpace"]
        config.messages.noAudioInput = configYaml["messages"]["noAudioInput"]

        config.conversation = Inst()
        config.conversation.greeting = configYaml["conversation"]["greeting"]

        config.ollama = Inst()
        config.ollama.url = configYaml["ollama"]["url"]
        config.ollama.model = configYaml["ollama"]["model"]

        config.whisperRecognition = Inst()
        config.whisperRecognition.modelPath = configYaml["whisperRecognition"]["modelPath"]
        config.whisperRecognition.lang = configYaml["whisperRecognition"]["lang"]

        return config



    def waveform_from_mic(self) -> np.ndarray:
  

        result = self.frames

        result = np.frombuffer(b''.join(result), np.int16).astype(np.float32) * (1 / 32768.0)
        

        return result

    def speech_to_text(self, 
                        waveform, 
                        temperature):
        logging.info("Converting speech to text")
        result_queue = queue.Queue()

        def transcribe_speech():
            try:
                logging.info("Starting transcription")
                transcript = transcribe(self.model, 
                                    waveform, 
                                    temperature=temperature, 
                                    **args)
                
                logging.info("Transcription completed")
                text = transcript["text"]
                print('\nMe:\n', text.strip())
                result_queue.put(text)
            except Exception as e:
                logging.error(f"An error occurred during transcription: {str(e)}")
                result_queue.put("") 

        transcription_thread = threading.Thread(target=transcribe_speech)
        transcription_thread.start()
        transcription_thread.join()

        return result_queue.get()

    def ask_ollama(self, prompt, responseCallback):
        logging.info(f"Asking OLLaMa with prompt: {prompt}")
        full_prompt = prompt if hasattr(self, "contextSent") else (prompt)
        self.contextSent = True
        jsonParam = {
            "model": self.config.ollama.model,
            "stream": True,
            "context": self.context,
            "prompt": full_prompt
        }
        
        try:
            with requests.Session() as s:
                response = s.post(self.config.ollama.url,
                                        json=jsonParam,
                                        headers=OLLAMA_REST_HEADERS,
                                        stream=True,
                                        timeout=30)  # Increase the timeout value
                response.raise_for_status()

                full_response = ""
                for line in response.iter_lines():
                    body = json.loads(line)
                    token = body.get('response', '')
                    full_response += token

                    if 'error' in body:
                        logging.error(f"Error from OLLaMa: {body['error']}")
                        responseCallback("Error: " + body['error'])
                        return

                    if body.get('done', False) and 'context' in body:
                        self.context = body['context']
                        break

                responseCallback(full_response.strip())

        except requests.exceptions.ReadTimeout as e:
            logging.error(f"ReadTimeout occurred while asking OLLaMa: {str(e)}")
            responseCallback("Sorry, the request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred while asking OLLaMa: {str(e)}")
            responseCallback("Sorry, an error occurred. Please try again.")


    def text_to_speech(self, text):


        def play_speech():
            try:
                self.tts_stream = sd.OutputStream(samplerate=self.voice.config.sample_rate, channels=1, dtype='int16')
                self.tts_stream.start()
                # Adjust the speech rate (optional)
                
                # Add a short delay before converting text to speech
                for audio_bytes in self.voice.synthesize_stream_raw(text):
                    int_data = np.frombuffer(audio_bytes, dtype=np.int16)
                    self.tts_stream.write(int_data)

                self.tts_stream.stop()
                self.tts_stream.close()
                print('\nAI:\n', text.strip())

                

            except Exception as e:
                logging.error(f"An error occurred during speech playback: {str(e)}")

        speech_thread = threading.Thread(target=play_speech)
        speech_thread.start()


    def main(self):
       

        while True:

            self.audio_stream = self.audio.open(format=INPUT_FORMAT,
                            channels=INPUT_CHANNELS,
                            rate=INPUT_RATE,
                            input=True,
                            start=True,
                            input_device_index=INPUT_DEVICE,
                            )
            
            
            listen_keyboard(on_press=self.get_pressed, 
                            on_release=self.get_release)


            self.audio_stream.stop_stream()
            self.audio_stream.close()


            if self.released:

                speech = self.waveform_from_mic()

                temperature = tuple(np.arange(0, 1.0 + 1e-6, 0.2))
                args = {"language": 'English',
                        "disable_cupy": False}
      
                result = transcribe(self.model, 
                                    speech, 
                                    temperature=temperature, 
                                    **args)
                
                print(result['text'])
                
                
                self.ask_ollama(result['text'], self.text_to_speech)
                
                self.frames = []
                self.release=False
                self.terminate=False
           
               


            elif ass.key == 'q':
                logging.info("Quit key pressed")
                ass.shutdown()


if __name__ == "__main__":

    logging.info("Starting Assistant")
 

    ass = Assistant()
    ass.main()
