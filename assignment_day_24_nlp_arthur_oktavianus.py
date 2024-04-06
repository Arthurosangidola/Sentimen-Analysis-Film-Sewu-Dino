# -*- coding: utf-8 -*-
"""Assignment_Day 24_NLP_Arthur Oktavianus.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b7Lr-t_864GupjVzU3sYfYGXndBrbgAX

# Crawl Data Twitter

Twitter Auth Token
"""

#@title Twitter Auth Token

twitter_auth_token = ('insert your token')

# Import required Python package
!pip install pandas

# Install Node.js (because tweet-harvest built using Node.js)
!sudo apt-get update
!sudo apt-get install -y ca-certificates curl gnupg
!sudo mkdir -p /etc/apt/keyrings
!curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

!NODE_MAJOR=20 && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list

!sudo apt-get update
!sudo apt-get install nodejs -y

!node -v

"""# Masukan topik yang ingin di crawling"""

# Crawl Data

filename = 'Sewu_Dino.csv'
search_keyword = 'Sewu Dino lang:id'
limit = 500

!npx --yes tweet-harvest@2.6.0 -o "{filename}" -s "{search_keyword}" -l {limit} --token {twitter_auth_token}

"""# Rubah kedalam bentuk data frame"""

import pandas as pd

# Specify the path to your CSV file
file_path = f"tweets-data/{filename}"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('/content/tweets-data/Sewu_Dino.csv')

# Display the DataFrame
display(df)

"""# Cek Jumlah Tweet yang didapatkan"""

# Cek jumlah data yang didapatkan

num_tweets = len(df)
print(f"Jumlah tweet dalam dataframe adalah {num_tweets}.")

"""# NLP

# Library
"""

!pip install sastrawi -q

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import requests

"""# Load Dataset"""

data = pd.read_csv('/content/Sewu_Dino.csv')
data.head()

data=data.loc[:,['id_str','full_text']]

data=data[['id_str','full_text']]
data.head()

data.rename(columns={'id_str':'Id'},inplace=True)

data['Id'] = range(1, len(data) + 1)

data.rename(columns={'full_text': 'Text Tweet'}, inplace=True)

data.head()

"""# Text Processing
Langkah-langkah yang digunakan dalam melakukan text preprocessing adalah sebagai berikut:
- Cleaning text
- Lowercase
- Remove stopwords
- Stemming / Lemmatization
- Tokenization

## Cleaning Text and Lower Case
"""

def cleaning_text(text):
    # remove url
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text = url_pattern.sub(r'', text)

    # remove hashtags
    # only removing the hash # sign from the word
    text = re.sub(r'#', '', text)

    # remove mention handle user (@)
    text = re.sub(r'@[\w]*', ' ', text)

    # remove emojis
    emoji_pattern = re.compile(
        '['
        '\U0001F600-\U0001F64F'  # emoticons
        '\U0001F300-\U0001F5FF'  # symbols & pictographs
        '\U0001F680-\U0001F6FF'  # transport & map symbols
        '\U0001F700-\U0001F77F'  # alchemical symbols
        '\U0001F780-\U0001F7FF'  # Geometric Shapes Extended
        '\U0001F800-\U0001F8FF'  # Supplemental Arrows-C
        '\U0001F900-\U0001F9FF'  # Supplemental Symbols and Pictographs
        '\U0001FA00-\U0001FA6F'  # Chess Symbols
        '\U0001FA70-\U0001FAFF'  # Symbols and Pictographs Extended-A
        '\U00002702-\U000027B0'  # Dingbats
        '\U000024C2-\U0001F251'
        ']+',
        flags=re.UNICODE
    )
    text = emoji_pattern.sub(r'', text)

    # remove punctuation
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in text.lower():
        if x in punctuations:
            text = text.replace(x, " ")

    # remove extra whitespace
    text = ' '.join(text.split())

    # lowercase
    text = text.lower()
    return text

"""## Remove Stopword"""

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

# CONSTRUCT STOPWORDS
rama_stopword = "https://raw.githubusercontent.com/ramaprakoso/analisis-sentimen/master/kamus/stopword.txt"
yutomo_stopword = "https://raw.githubusercontent.com/yasirutomo/python-sentianalysis-id/master/data/feature_list/stopwordsID.txt"
fpmipa_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/fpmipa-stopwords.txt"
sastrawi_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/sastrawi-stopwords.txt"
aliakbar_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/aliakbars-bilp.txt"
pebahasa_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/pebbie-pebahasa.txt"
elang_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-id.txt"
nltk_stopword = stopwords.words('indonesian')

# create path url for each stopword
path_stopwords = [rama_stopword, yutomo_stopword, fpmipa_stopword, sastrawi_stopword,
                  aliakbar_stopword, pebahasa_stopword, elang_stopword]

# combine stopwords
stopwords_l = nltk_stopword
for path in path_stopwords:
    response = requests.get(path)
    stopwords_l += response.text.split('\n')

custom_st = '''
yg yang dgn ane smpai bgt gua gwa si tu ama utk udh btw
ntar lol ttg emg aj aja tll sy sih kalo nya trsa mnrt nih
ma dr ajaa tp akan bs bikin kta pas pdahl bnyak guys abis tnx
bang banget nang mas amat bangettt tjoy hemm haha sllu hrs lanjut
bgtu sbnrnya trjadi bgtu pdhl sm plg skrg
'''

# create dictionary with unique stopword
st_words = set(stopwords_l)
custom_stopword = set(custom_st.split())

# result stopwords
stop_words = st_words | custom_stopword
print(f'Stopwords: {list(stop_words)[:5]}')

# remove stopwords
from nltk import word_tokenize, sent_tokenize

def remove_stopword(text, stop_words=stop_words):
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return ' '.join(filtered_sentence)

"""## Stemming / Lemmatization"""

# stemming and lemmatization
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def stemming_and_lemmatization(text):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(text)

"""##  Tokenization

"""

# tokenization
def tokenize(text):
    return word_tokenize(text)

"""# Implement in dataset"""

# pipeline preprocess
def preprocess(text):
    # cleaning text and lowercase
    output = cleaning_text(text)

    # remove stopwords
    output = remove_stopword(output)

    # # stemming and lemmatization
    # output = stemming_and_lemmatization(output)

    # # tokenization
    # output = tokenize(output)

    return output

# implement preprocessing
preprocessed_data = data.copy()
preprocessed_data['Text Tweet'] = data['Text Tweet'].map(preprocess)

preprocessed_data.tail()

preprocessed_data['Text Tweet'][0]

"""## Save to CSV"""

df = pd.DataFrame(preprocessed_data)
csv_file_path = 'use_preprocessed_data.csv'
df.to_csv(csv_file_path, sep=';', index=False, header=True)

print(f'Data has been saved to {csv_file_path}')

# load dataset into pandas
import pandas as pd
data_upd = pd.read_csv('/content/use_preprocessed_data_upd_sentiment.csv')
data_upd

"""#LSTM"""

import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense

# Assuming your data is in a CSV file
file_path = '/content/use_preprocessed_data_upd_sentiment.csv'
df = pd.read_csv(file_path)

# Assuming the 'Text Tweet' column contains the text data and 'Sentiment' contains labels
texts = df['Text Tweet'].tolist()
labels = df['Sentiment'].tolist()

# Tokenize the text data
max_words = 10000  # Adjust based on your dataset size
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

# Pad sequences to make them of equal length
max_sequence_length = 100  # Adjust based on your dataset and sequence length
data = pad_sequences(sequences, maxlen=max_sequence_length)

# Convert labels to one-hot encoding
labels = pd.get_dummies(labels)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Build the LSTM model
model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=100, input_length=max_sequence_length))
model.add(LSTM(units=64, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(units=len(labels.columns), activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.layers import Dropout


# Build the LSTM model with some modifications
model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=100, input_length=max_sequence_length))
model.add(LSTM(units=128, dropout=0.3, recurrent_dropout=0.3, return_sequences=True)) # Adding return_sequences=True
model.add(LSTM(units=64, dropout=0.2, recurrent_dropout=0.2, return_sequences=True)) # Adding return_sequences=True
model.add(LSTM(units=32, dropout=0.2, recurrent_dropout=0.2, return_sequences=False))
model.add(Dense(units=len(labels.columns), activation='softmax'))


# Add dropout layer to prevent overfitting
model.add(Dropout(0.5))

# Compile the model with a different optimizer and learning rate
optimizer = Adam(lr=0.0001)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Early stopping to prevent overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train the model with early stopping
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), callbacks=[early_stopping])

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

# Save the model to a file
model.save('lstm_sentiment_model.h5')

# Optionally, save the tokenizer as well for later use during inference
import pickle

# Optionally, save the tokenizer as well for later use during inference
with open('tokenizer.pkl', 'wb') as tokenizer_file:
    pickle.dump(tokenizer, tokenizer_file)

from keras.models import load_model
import pickle

# Load the model
loaded_model = load_model('lstm_sentiment_model.h5')

# Load the tokenizer
with open('tokenizer.pkl', 'rb') as tokenizer_file:
    loaded_tokenizer = pickle.load(tokenizer_file)

# New sentence for testing
test_sentence = 'filmya biasa saja'
new_sentence = preprocess(test_sentence)
# Tokenize and pad the new sentence
new_sequence = loaded_tokenizer.texts_to_sequences([new_sentence])
new_data = pad_sequences(new_sequence, maxlen=max_sequence_length)

# Predict sentiment for the new sentence
predictions = loaded_model.predict(new_data)

# Get the predicted sentiment label
predicted_sentiment_label = labels.columns[predictions.argmax(axis=1)[0]]
print(f"preprocessing: {new_sentence}")
print(f"new_sequence: {new_sequence}")
print(f"new_data: {new_data}")
print(f"Predicted Sentiment: {predicted_sentiment_label}")

"""# LSTM Update Sample"""

import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense

# Assuming your data is in a CSV file
file_path = '/content/Sewu_Dino_upd.csv'
df2 = pd.read_csv(file_path)

# Assuming the 'Text Tweet' column contains the text data and 'Sentiment' contains labels
texts = df2['Text Tweet'].tolist()
labels = df2['Sentiment'].tolist()

# Tokenize the text data
max_words = 10000  # Adjust based on your dataset size
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

# Pad sequences to make them of equal length
max_sequence_length = 100  # Adjust based on your dataset and sequence length
data = pad_sequences(sequences, maxlen=max_sequence_length)

# Convert labels to one-hot encoding
labels = pd.get_dummies(labels)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Build the LSTM model
model2 = Sequential()
model2.add(Embedding(input_dim=max_words, output_dim=100, input_length=max_sequence_length))
model2.add(LSTM(units=64, dropout=0.2, recurrent_dropout=0.2))
model2.add(Dense(units=len(labels.columns), activation='softmax'))

model2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model2.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

# Save the model to a file
model2.save('lstm_sentiment_model_new.h5')

# Optionally, save the tokenizer as well for later use during inference
import pickle

with open('new_tokenizer.pkl', 'wb') as tokenizer_file:
    pickle.dump(tokenizer, tokenizer_file)

"""# Hyperparameter tuning"""

# Save the model to a file with a different name
model.save('tuned_lstm_sentiment_model.h5')

# Optionally, save the tokenizer as well for later use during inference
import pickle

with open('tuned_tokenizer.pkl', 'wb') as tokenizer_file:
    pickle.dump(tokenizer, tokenizer_file)

"""# Test kembali dengan sentence yang sama dengan model sebelumnya"""

from keras.models import load_model
import pickle

# Load the model
loaded_model = load_model('lstm_sentiment_model_new.h5')

# Load the tokenizer
with open('new_tokenizer.pkl', 'rb') as tokenizer_file:
    loaded_tokenizer = pickle.load(tokenizer_file)

# New sentence for testing
test_sentence2 = 'film nya jelek sekali'
new_sentence2 = preprocess(test_sentence2)
# Tokenize and pad the new sentence
new_sequence2 = loaded_tokenizer.texts_to_sequences([new_sentence2])
new_data2 = pad_sequences(new_sequence, maxlen=max_sequence_length)

# Predict sentiment for the new sentence
predictions = loaded_model.predict(new_data2)

# Get the predicted sentiment label
predicted_sentiment_label = labels.columns[predictions.argmax(axis=1)[0]]
print(f"preprocessing: {new_sentence2}")
print(f"new_sequence: {new_sequence2}")
print(f"new_data: {new_data2}")
print(f"Predicted Sentiment: {predicted_sentiment_label}")

