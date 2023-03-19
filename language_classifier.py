import collections
import typing
import math

import nltk
nltk.download('udhr')
from nltk.corpus import udhr

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

languages = ['english', 'german', 'dutch', 'french', 'italian', 'spanish']
language_ids = ['English-Latin1', 'German_Deutsch-Latin1', 'Dutch_Nederlands-Latin1', 'French_Francais-Latin1', 'Italian_Italiano-Latin1', 'Spanish_Espanol-Latin1']# I chose the above sample of languages as they all use similar characters. 

### Optional: If you want to add more languages:

# First use this function to find the language file id
def retrieve_fileid_by_first_letter(fileids, letter):
    return [id for id in fileids if id.lower().startswith(letter.lower())]

# Example usage

# Then copy-paste the language name and language id into the relevant list:
languages += []
language_ids += []

def extract_xgrams(text:str, n_vals: typing.List[int]) -> typing.List[str]:

    xgrams = []

    for n in n_vals:
        if n < len(text):
            for i in range(len(text) - n + 1) :
                ng = text[i:i+n]
                xgrams.append(ng)
    return xgrams

def build_model(text:str, n_vals: typing.List[int]) -> typing.Dict[str, int]:

    model = collections.Counter(extract_xgrams(text, n_vals))
    num_ngrams = sum(model.values())

    for ng in model:
        model[ng] = model[ng] / num_ngrams
    return model

raw_texts = {language: udhr.raw(language_id) for language, language_id in zip(languages, language_ids)}

# Build a model of each language
models = {language: build_model(text=raw_texts[language], n_vals=range(1,4)) for language in languages}

def calculate_cosine(a: typing.Dict[str, float], b: typing.Dict[str, float]) -> float:
    """
    Calculate the cosine between two numeric vectors
    Params:
        a, b: two dictionaries containing items and their corresponding numeric values
        (e.g. ngrams and their corresponding probabilities)
    """
    numerator = sum([a[k]*b[k] for k in a if k in b])
    denominator = (math.sqrt(sum([a[k]**2 for k in a])) * math.sqrt(sum([b[k]**2 for k in b])))
    return numerator / denominator

def identify_language(
    text: str,
    language_models: typing.Dict[str, typing.Dict[str, float]],
    n_vals: typing.List[int]
    ) -> str:
    """
    Given a text and a dictionary of language models, return the language model 
    whose ngram probabilities best match those of the test text
    Params:
        text: the text whose language we want to identify
        language_models: a Dict of Dicts, where each key is a language name and 
        each value is a dictionary of ngram: probability pairs
        n_vals: a list of n_gram sizes to extract to build a model of the test 
        text; ideally reflect the n_gram sizes used in 'language_models'
    """
    text_model = build_model(text, n_vals)
    language = ""
    max_c = 0
    for m in language_models:
        c = calculate_cosine(language_models[m], text_model)
        # The following line is just for demonstration, and can be deleted
        if c > max_c:
            max_c = c
            language = m
    return language

## ZackBOt
zackBot = ChatBot("Zack")
trainer = ListTrainer(zackBot)
    
## Greetingsgreet
greetings = ["YO",
            "*smacks you on your back*", 
            "*shoots you*", 
            "Hi",
            "Oh lordy lord!",
            "LMAO",
            "dud",
            "AUUUGHHHHHH",
            "I got options bro",
            "Yo can we finish this"
            ]
## Jokes
jokes = ["Wanna hear a joke?"
        "I was wondering why the ball was getting bigger and bigger. Then it hit me.",
        "Why did the chicken cross the road?",
        "Guess what? Chicken butt",
        "What goes up and down but does not move?",
        "Stairs",
        "Where should a 500 pound alien go?",
        "On a diet",
        "What did one toilet say to the other?",
        "You look a bit flushed.",
        "Why did the picture go to jail?",
        "Because it was framed.",
        "What did one wall say to the other wall?",
        "I'll meet you at the corner.",
        "What did the paper say to the pencil?",
        "Write on!",
        "What do you call a boy named Lee that no one talks to?",
        "Lonely"]

## Makeing fun of ali
ali_insults = ["Why you stuttering", 
            "I dont even play this and I can still beat you, you are bad!!!!!!",
            "You're trash",
            "Play chess rn",
            "Can you give me a charger",
            "Didn't you stutter?",
            "man you so stupid",
            "Why you stutter on that word?",
            "Yo you are so trash bro"]
    

## Videogames
videogames = ["Yesterday I was playing games last night and I went crazy!!!!!",
              "Yo I am cracked at snake",
             "1v1 me right now and I'll beat you",
             "My KD is 5.0"]

## Insults/Comebacks
insults = ["man you so stupid",
         "Why you stutter on that word?",
         "Yo you are so trash bro",
         ]

## Training the ZackBot
trainer.train(greetings)
trainer.train(jokes)
trainer.train(ali_insults)
trainer.train(videogames)         
trainer.train(insults)

## Starting the conversation

print("Hello! Welcome to ZackBot")
print("To exit, please type exit")
print()
print("--------------------------------------------------")
print()
print("Hey")


## Conversation
while True:
    response = input().lower()
    if "exit" in response or "bye" in response:
        break
    elif identify_language(response, models, n_vals=range(1,4)) != 'english':
        print("Sorry, I don't speak that language!")
    else:
        zackBot_response = zackBot.get_response(response)
        print(zackBot_response)
    user_response = response

    
print("ight ill see ya")
