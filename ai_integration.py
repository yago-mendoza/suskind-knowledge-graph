import os
import openai
from skcomponents import *
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate



class PromptTemplate:
    def __init__(self, template):
        self.template = template

    def ask(self, *args):
        return self.template.format(*args)

class LLMBuilder:
    def __init__(self, max_tokens, temperature):
        self.model_name = 'gpt-3.5-turbo-16k'  # Default model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompt_template = None

    def set_model_name(self, model_name):
        self.model_name = model_name
        return self

    def build(self, prompt_template):
        self.prompt_template = prompt_template.replace("_", "{}")
        return Suskind_LLM_Implementation(self)


class Suskind_LLM_Implementation:
    def __init__(self, builder):
        self.llm = OpenAI(model_name=builder.model_name, temperature=builder.temperature, max_tokens=builder.max_tokens)
        self.prompt = PromptTemplate(builder.prompt_template)

    def send(self, *args):
        return self.llm(self.prompt.ask(*args)).strip()


MODELS = {
    1 : 'gpt-3.5-turbo-16k',
    2 : 'gpt-3.5-turbo-1106',
    3 : 'babbage-002',
    4 : 'davinci-002'
}

# Ejemplo de uso:
builder = LLMBuilder(max_tokens=3, temperature=0.5)
builder.set_model_name(MODELS[1])
LLM = builder.build('Rate _ between "_" and "_". 1-10.')

response = LLM.send('w1', 'w2', 'property')
print(response)



