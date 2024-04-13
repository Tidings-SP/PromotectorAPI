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



@app.route('/detect', methods = ['GET']) 
def detect():
    url = request.args.get('url')
    is_eng_param = request.args.get('isEng')
    is_eng = is_eng_param.lower() in ['true', '1', 't', 'y', 'yes'] if is_eng_param else True
    data = extract_text_from_video(url, is_eng)
    rs = 'Fake Promotion' if (clf.predict([data]) == 0) else 'Genuine Promotion'
    return jsonify({'data': data,
                    'prediction' : rs,
                    }) 
  


def extract_text_from_video(url, isEng = True):
    video = mp.VideoFileClip(url)
    audio_file = video.audio 
    audio_file.write_audiofile("2.wav")
    r = sr.Recognizer() 
    trans = GoogleTranslator()
    # print(type(audio_file))
    # Specify the language code for Tamil
    r.lang = "ta-IN"

    with sr.AudioFile("/opt/render/project/src/2.wav") as source:
        # Listen for the data (load audio to memory)
        audio_data = r.record(source)
    try:
        # Recognize the audio and specify English as the language
        if(isEng):
            text = r.recognize_google(audio_data) 
        else:
            text = r.recognize_google(audio_data, language='ta-IN') 
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Could not understand audio")
        print("You said: " + text)
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    trans_text = GoogleTranslator(source='auto', target='en').translate(text)

    print(trans_text)
    return trans_text




if __name__ == "__main__":   
    app.run(debug=False)      