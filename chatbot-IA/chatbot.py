import random
import json
import pickle
import numpy as np
import mysql.connector

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i]=1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    return category

def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i['responses'])
            break
    return result

# Configurar la conexión a la base de datos
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="databasechatbot"
)

# Crear un cursor para ejecutar las consultas
cursor = connection.cursor()


# Insertar un registro en la tabla
def insert_chat_record(user_message, chat_response):
    sql = "INSERT INTO mensaje_usuario_chat (mensaje_usuario, respuesta_chat) VALUES (%s, %s)"
    values = (user_message, chat_response)
    cursor.execute(sql, values)
    connection.commit()
    print("Registro insertado correctamente")

while True:
    print("Usuario: ")
    message = input("")
    ints = predict_class(message)
    res = get_response(ints, intents)
    print("OtiChat: ", res)
    # Insertar el registro en la base de datos
    insert_chat_record(message, res)

