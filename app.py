from flask import Flask, jsonify, request 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import moviepy.editor as mp
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pickle


clf = pickle.load(open('model.pkl','rb'))
app = Flask(__name__)
@app.route('/') 
def index():
    return "<center><h1>To use the API put / followed by your text on the root url!</h1></center>"



@app.route('/<st>', methods = ['GET']) 
def detect(st):
    rs = extract_text_from_video()
    # rs = 'Fake Promotion' if (clf.predict([st]) == 0) else 'Genuine Promotion'
    return jsonify({'data': rs}) 
  


def extract_text_from_video():
    video = mp.VideoFileClip("https://firebasestorage.googleapis.com/v0/b/promodetector-7ddb1.appspot.com/o/1.mp4?alt=media&token=6ca8d382-fc9a-4482-a1cb-0d5b32e51472")
    audio_file = video.audio 
    audio_file.write_audiofile("1.wav")
    isEng = False
    r = sr.Recognizer() 
    trans = GoogleTranslator()

    # Specify the language code for Tamil
    r.lang = "ta-IN"

    with sr.AudioFile('1.wav') as source:
        # Listen for the data (load audio to memory)
        audio_data = r.record(source)
    try:
        # Recognize the audio and specify English as the language
        text = r.recognize_google(audio_data, language='ta-IN')  # Specify English language
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    trans_text = GoogleTranslator(source='auto', target='en').translate(text)

    print(trans_text)
    return trans_text




# if __name__ == "__main__":   
#     app.run(debug=False)      