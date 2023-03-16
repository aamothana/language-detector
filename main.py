from language-classifier import identify_language
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

## Jokes: https://www.ducksters.com/jokes/silly.php
## Corpus: https://github.com/gunthercox/chatterbot-corpus/blob/master/chatterbot_corpus/data/english/conversations.yml

## ZackBOt
zackBot = ChatBot("Zack")
trainer = ListTrainer(zackBot)

## Sentiment Value Calculator 
sentiment_value_dictionary = {}
file = open("sentiment_values.csv")

for line in file:
    line_list = line.split(",")
    sentiment_value_dictionary[line_list[0]] = float(line_list[1].strip())
    
#Takes a String and returns the overall sentiment value of that String
def get_total_sentiment(user_input):
    score = 0
    # Split into a list
    user_input_list = user_input.split(" ")
    # Make each word lowercase
    for word in user_input_list:
        word = word.lower()
        #Check for puntuation
        if not word.isalpha():
            word = remove_punctuation(word)
        # Add the sentiment values
        if word in sentiment_value_dictionary:
            score += sentiment_value_dictionary[word]
    return score
    

#Takes a String and returns that String without any punctuation or non-alphanumeric characters
def remove_punctuation(word):
    new_word = ""
    for i in range(len(word)):
        if word[i].isalpha():
            new_word += word[i]
    return new_word
    
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
    
## hasbulla


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

## Corpus Trainer
#trainer = ChatterBotCorpusTrainer(zackBot)
# trainer.train("chatterbot.corpus.english.greetings")
# trainer.train("chatterbot.corpus.english.conversations")

# trainer.train("chatterbot.corpus.english.botprofile")
# trainer.train("chatterbot.corpus.english.money")

## Teaching
#zackBot.learn_response("Have a nice day!", "I'm done with this conversation")

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
    if response == "good response":
        zackBot.learn_response(user_response, zackBot_response)
        print("Thanks I'm Learning!")
    if identify_language(response, models, n_vals=range(1,4)) != 'english':
        print("Sorry, I don't speak that language!")

    
print("ight ill see ya")