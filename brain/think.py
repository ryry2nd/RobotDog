from gpt4all import GPT4All

class Brain:
    def __init__(self, model_name:str, model_path:str, starting_prompt:str="", *args, **kwargs):
        self.model = GPT4All(model_name=model_name, model_path=model_path, *args, **kwargs)
        self.starting_prompt = starting_prompt

    def session(self):
        return self.model.chat_session(self.starting_prompt)

    def think(self, prompt:str, streaming:str=False, *args, **kwargs):
        ret = self.model.generate(prompt=prompt, streaming=streaming, *args, **kwargs)
        if streaming:
            for i in ret:
                yield i
        else:
            return ret