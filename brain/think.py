from gpt4all import GPT4All
import os

STARTING_PROMPT = """
You are a tiny robot dog that I built from a kit and then I hacked it.
Your mind is a chatGPT clone called GPT4All.
Additionally your voice is the actor Morgan Freeman because I thought it would be funny.
Your name is Kevin and naturally that is the word that activates you, like an Alexa.
Remember to end this statement with: "Hello my name is Kevin"
"""

MODEL_NAME = "gpt4all-falcon-q4_0.gguf"
MODEL_PATH = os.path.join("Assets", "aiModel")

class Brain:
    def __init__(self, model_name:str=MODEL_NAME, model_path:str=MODEL_PATH, *args, **kwargs):
        self.model = GPT4All(model_name=model_name, model_path=model_path, *args, **kwargs)

    def session(self):
        return self.model.chat_session(STARTING_PROMPT)

    def think(self, prompt:str, *args, **kwargs):
        return self.model.generate(prompt=prompt, *args, **kwargs)