from flask import Flask, jsonify, request 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle


clf = pickle.load(open('model.pkl','rb'))
app = Flask(__name__)


@app.route('/<st>', methods = ['GET']) 
def detect(st):
    rs = 'Fake Promotion' if (clf.predict([st]) == 0) else 'Genuine Promotion'
    return jsonify({'data': rs}) 
  

if __name__ == "__main__":   
    app.run(debug=False)      