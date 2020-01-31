import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# load data: 28x28 per img, norm 0-1
data = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = data.load_data()
test_images = test_images/255.0
train_images = train_images/255.0

class_names = ['t-shirt', 'trouser', 'pullover', 'dress', 'coat',
			   'sandal', 'shirt', 'sneaker', 'bag', 'ankle boot', ]

# create model: input 1 entry per img, 128 hidden, 10 output
model = keras.Sequential([
	keras.layers.Flatten(input_shape=(28, 28)),
	keras.layers.Dense(128, activation="relu"),
	keras.layers.Dense(10, activation="softmax")
	])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
	metrics=["accuracy"])
model.fit(train_images, train_labels, epochs=2)

# predict
prediction = model.predict(test_images)
for i in range(5):
	plt.grid(False)
	plt.imshow(test_images[i])
	plt.xlabel("actual: " + class_names[test_labels[i]])
	plt.title("predict: " + class_names[np.argmax(prediction[i])])
	plt.show()

