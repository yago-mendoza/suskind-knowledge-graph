import os
import openai
from skcomponents import *
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# os.environ['OPENAI_API_KEY'] =
# openai.api_key = 
# G = Graph('data.txt')

model_of_choice = 1

# hey, so, i just discovered, hyperonyms and hyponyms are useles, are basically synoynms jeje
# 

MODELS = {
    1 : 'gpt-3.5-turbo-16k',
    2 : 'gpt-3.5-turbo-1106',
    3 : 'babbage-002',
    4 : 'davinci-002'
}

# synonyms : put to 0, 1 or 2
# semantic : 

# QUOTES, REPLICAS, SLANG
# Sinónimos y semánticos no recíprocos. Limpiar.

# OBJETIVOS
# - Conseguir poner synset1 -> synset0, synset1, synset2, hyperonyms, hyponyms
# - Conseguir poner semset1 -> semset0, semset1, semset2, hyperonyms, hyponyms, antonyms

# STEPS (syns)

# "Rate 'habitual' synonym 'fijo' [1-10] just number.
# "Is 'godzilla' a 'monstruo' just [Y/N]"

# Is very similar "Abominable monstruo de las nieves" and "Monstruo"?
# Is "Mueble" >concept, = or < than "Silla"? Return just symb.
# Rate poetry on 'alfilerazo luminoso' [1-10] just number

# Concepts related to 'word'
# Concepts related to 'word definition'
# What word is
# Has 'banco' multiple meanings
# Has White House multiple meanings?
# Persona - armazón de huesos, buen samaritano, gloria pasada
# Bebida - sidra caliente, té helado, caldo, ginebra, leche

# synset-0 [opt]: This set includes synonyms that have a broader meaning than the target word. They encompass the essence of the target word but in a wider context.
# - persona : ser vivo, sujeto, organismo vivo
# - copioso : infinito
# synset-1 [opt]: These are words that can be used interchangeably with the target word. They are almost identical in meaning.
# - persona : ciudadano de a pie, individuo
# synset-2 [opt]: This set includes synonyms that are similar to the target word but are more specific and often used in particular contexts.
# - persona : hablante, transeúnte, viandante
# - cincelado por los ángeles : de torneados músculos
# - latido : acelerados latidos del corazón

# semset-0
# This set includes hyperonyms, which are words with a broader category that phyisically or conceptually encompasses in a space the given word. This shouldn’t be confused with the ‘set’ field.
# - n : ‘n’ representing a component (wheel(car),
# - n : ‘n’ representing a subdivision (San Francisco(EEUU),
# - n : ‘n’ representing a content (leche(biberón),
# - v : ‘n’ that come before (muerte inminente(aferrarse a la vida),
# - n : ‘v’ that come before (apuñalar(herida),
# semset-1
# These are words that are directly related to the target word, but NOT synonyms. They could be any type of word (noun, verb, adjective, etc.) that has an immediate connection.
# - n : intrinsic ‘j’ (navideño, frivolo, maleducado instead of Navidad, frivolidad, mala educación)
# Note 1. Navideño instead of Navidad. Frivolo instead of Frivolidad. Maleducado instead of Mala educación.
# Note 2. Evitar rangos enteros de sinónimos. Solo los más ad hoc.
# Note 3. Remember that if they are not intrinsic, we can make up new nodes.
# - j : ‘n’ that is the root(algodón(algodonoso),
# - v : ‘n’ to which is intrinsic (perro(ladrar), 
# - v : ‘n’ which is intrinsic to the action (determinación(avanzar sin Volver la vista),
# - v : ‘v’ simultaneous occur (acompañar en el sentimiento – estar de luto)
# semset-2
# This set consists of meronyms, which are words that denote a part of, or a member of, the thing that the target word represents.
# - EEUU : San Francisco
# - wheel : tire, rubber
# - hacer sitio : abrir camino
# - v : ‘v’ that come after


# connotations = ["Positive", "Negative", "Neutral", "Ambiguous", "Variable"]
# frequencies = ["Very High", "High", "Medium", "Low", "Very Low"]
# registers = ["Formal", "Informal", "Technical", "Poetic", "Colloquial", "Academic", "Archaic", "Creative", "Professional", "Historical", "Universal", "Specialized", "Youthful", "Business", "Idiomatic"]

















# synonyms = []
# syns_nodeset = G.filter_synset1('>',20)
# for _ in range(10):
#     n = syns_nodeset.random()
#     synonyms.append((n.name, n.get_neighbors('synset1').random().name))
    

# class Suskind_LLM_Implementation:

#     def __init__ (self):
#         self.llm = OpenAI(model_name=MODELS[model_of_choice], temperature=0, max_tokens=3)
#         self.prompt = PromptTemplate(
#             input_variables=['w1','w2','property'],
#             template = 'Rate {property} between "{w1}" and "{w2}". 1-10.',
#         )

#     def rate (self, w1, w2, property):
#         return self.llm(self.prompt.format(w1=w1, w2=w2, property=property))


# LLM = Suskind_LLM_Implementation()

# for mssg in mssgs:
#     print(LLM.llm(mssg[0]).strip(), mssg[1])

# for s1, s2 in synonyms:
#     rate = LLM.rate(s1, s2, 'synonimicity')
#     print(s1, s2, rate.strip())




