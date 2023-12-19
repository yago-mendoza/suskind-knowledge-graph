import os
import openai
from skcomponents import *
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

MODELS = {
    1 : 'gpt-3.5-turbo-16k',
    2 : 'gpt-3.5-turbo-1106',
    3 : 'babbage-002',
    4 : 'davinci-002'
}

model_of_choice = 5
max_tokens = 3
    
class Suskind_LLM_Implementation:

    def __init__ (self):
        self.llm = OpenAI(model_name=MODELS[model_of_choice], temperature=0, max_tokens=max_tokens)
        self.prompt = PromptTemplate(
            input_variables=['w1','w2','property'],
            template = 'Rate {property} between "{w1}" and "{w2}". 1-10.',
        )

    def rate (self, w1, w2, property):
        return self.llm(self.prompt.format(w1=w1, w2=w2, property=property))


LLM = Suskind_LLM_Implementation()

for mssg in mssgs:
    print(LLM.llm(mssg[0]).strip(), mssg[1])

for s1, s2 in synonyms:
    rate = LLM.rate(s1, s2, 'synonimicity')
    print(s1, s2, rate.strip())




