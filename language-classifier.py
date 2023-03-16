import typing
import math
import pip
import nltk
from nltk.corpus import udhr

languages = ['english', 'german', 'dutch', 'french', 'italian', 'spanish']
language_ids = ['English-Latin1', 'German_Deutsch-Latin1', 'Dutch_Nederlands-Latin1', 'French_Francais-Latin1', 'Italian_Italiano-Latin1', 'Spanish_Espanol-Latin1']# I chose the above sample of languages as they all use similar characters. 

### Optional: If you want to add more languages:

# First use this function to find the language file id
def retrieve_fileid_by_first_letter(fileids, letter):
    return [id for id in fileids if id.lower().startswith(letter.lower())]

# Example usage
print(f"Fileids beginning with 'R': {retrieve_fileid_by_first_letter(udhr.fileids(), letter='R')}")

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
print(raw_texts['english'][:1000]) # Just print the first 1000 characters

# Build a model of each language
models = {language: build_model(text=raw_texts[language], n_vals=range(1,4)) for language in languages}
print(models['german'])

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
        print(f'Language: {m}; similarity with test text: {c}')
        if c > max_c:
            max_c = c
            language = m
    return language

print(f"Test text: {text}")
print(f"Identified language: {identify_language(text, models, n_vals=range(1,4))}")

# Prints
# Test text: i was taught that the way of progress was neither swift nor easy.
# Language: english; similarity with test text: 0.7812347488239613
# Language: german; similarity with test text: 0.6638235631734796
# Language: dutch; similarity with test text: 0.6495872103674768
# Language: french; similarity with test text: 0.7073331083503462
# Language: italian; similarity with test text: 0.6635204671187273
# Language: spanish; similarity with test text: 0.6811923819801172
# Identified language: english
