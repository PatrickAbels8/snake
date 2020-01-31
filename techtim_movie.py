import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# load data: 28x28 per img, norm 0-1
data = keras.datasets.imdb
(train_data, train_labels), (test_data, test_labels) = data.load_data(
	num_words = 10000)

# make data readable
word_index = data.get_word_index()
word_index = {k:(v+3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

reverse_word_index = dict([(value, key) for (key, value) 
	in word_index.items()])

# preprocessing
train_data = keras.preprocessing.sequence.pad_sequences(train_data,
	value=word_index["<PAD>"], padding="post", maxlen=250)
test_data = keras.preprocessing.sequence.pad_sequences(test_data,
	value=word_index["<PAD>"], padding="post", maxlen=250)

def decode_review(text):
	return " ".join([reverse_word_index.get(i, "?") for i in text])


# model
model = keras.Sequential([
	keras.layers.Embedding(10000, 16),
	keras.layers.GlobalAveragePooling1D(),
	keras.layers.Dense(16, activation="relu"),
	keras.layers.Dense(1, activation="sigmoid")
	])

model.summary()
model.compile(optimizer="adam", loss="binary_crossentropy",
	 metrics=["accuracy"])

x_val = train_data[:10000]
x_train = train_data[10000:]
y_val = train_labels[:10000]
y_train = train_labels[10000:]

fitmodel = model.fit(x_train, y_train, epochs=40, batch_size=512,
	validation_data=(x_val, y_val), verbose=1)
results = model.evaluate(test_data, test_labels)

# print(results)

# todo save model