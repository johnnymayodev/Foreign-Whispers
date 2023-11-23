import os
import shutil
import time
import pickle

import pyttsx3 #9.0.1
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 0.7)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 

if os.path.exists("audio"):
    shutil.rmtree("audio")
os.mkdir("audio")

# def main(dictionary, language):
#     text = dictionary_to_text(dictionary)



#     start_time = time.time()
    


#     end_time = time.time()
#     print("Time taken: ", round(end_time - start_time, 2))

# def dictionary_to_text(dictionary):

#     pause = " . . . . " # 1 second pause
#     text = dictionary[0]['text'] 

#     for i in range(1, len(dictionary)):
#         gap = dictionary[i]['start'] - dictionary[i-1]['end']
#         text += pause * gap
#         text += dictionary[i]['text']

#     return text 

if __name__ == "__main__":

    myDict = {
        0: {
            'start': 0,
            'end': 7,
            'text': 'Bill Gates helped usher in the digital revolution at Microsoft and has spent the decade since'
        },
        1: {
            'start': 8,
            'end': 12,
            'text': "exploring and investing in innovative solutions to some of the world's toughest problems",
        },
        2: {
            'start': 13,
            'end': 18,
            'text': ' global poverty, disease, and the coronavirus pandemic, which he spent nearly $2 billion',
        },
    }

    language = "en"

    # main(myDict, language)

    