import pandas as pd 
import pickle
from flask import Flask, render_template, request
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from playsound import playsound


app=Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
trip = pd.read_csv('tripadvisor_hotel_reviews.csv')
tokenizer = Tokenizer()
tokenizer.fit_on_texts(trip['Review'])



@app.route('/')
def home():
    result = ''
    return render_template('index.html', **locals())



@app.route('/predict', methods=['POST', 'GET'])
def predict():
    comment = request.form['comment']

    # Tokenization
    comment = tokenizer.texts_to_sequences(comment)

    # padding
    comment = pad_sequences(comment,maxlen=100,padding='post')

    # prediction
    review_predict = (model.predict(comment)>0.5).astype('int')

    if review_predict[0] == 1:
        result = "It's a negative review"
        playsound('0.mp3')
    else:
        result = "It's a positive review"
        playsound('1.mp3')

    return render_template('index.html', **locals())

if __name__ == '__main__':
    app.run()