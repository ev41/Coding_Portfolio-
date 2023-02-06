#tensorflow is a dope library for creating machine learning models
#keras is another machine learning library that has a lot of useful functions for preprocessing data. Useful functions such as feature normalization, standardization, etc etc.
#tensorflow also has in-house datasets which are suuuuuper useful and easily integrated into your code. Will definitely try using them in future ML projects. 

import tensorflow as tf
from tensorflow import keras



# import the CIFAR-10 dataset
(X_train, y_train), (X_test, y_test) = keras.datasets.cifar10.load_data()

# Normalize the data
#should I use the tf.keras.layers.normalization function instead? 

X_train = X_train / 255.0
X_test = X_test / 255.0

# Define the model
#
model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu',
                        input_shape=(32, 32, 3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10)

# Evaluate the model
test_loss, test_acc = model.evaluate(X_test,  y_test, verbose=2)
print('\nTest accuracy:', test_acc)
