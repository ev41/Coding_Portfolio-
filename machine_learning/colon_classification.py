# Import required libraries
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras

# Load the dataset
(train_dataset, test_dataset), dataset_info = tfds.load('colorectal_histology',
                                                        split=[
                                                            'train[:80%]', 'train[80%:90%]'],
                                                        with_info=True,
                                                        as_supervised=True)



# Preprocess the data
#this makes our data useable by converting it into a format that can be utilized/processed by the neural network model.
#We're formating the shape of the images, as well as dividing pixel values by 255 so we can feed values 0-1 through the model. 
def preprocess(image, label):
    image = tf.cast(image, tf.float32)
    image = tf.image.resize(image, (96, 96))
    image /= 255
    return image, label


train_dataset = train_dataset.map(preprocess).batch(32)
test_dataset = test_dataset.map(preprocess).batch(32)

# Build the model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(96, 96, 3)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# Compile the model. The optimizer is a parameter that influences the models weights and learning rate. Adam is a powerful and efficient option.
#loss is a parameter... ok, in short, loss calculates the neural network gradients, which adapts node weights, which (hopefully) increases the model's accuracy.
#metric should be self-explanatory.
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])



# This is what we use the train the model
model.fit(train_dataset, epochs=10)



# Annnnnnnnnnnd that's all folks. Now we run this bad boy
test_loss, test_acc = model.evaluate(test_dataset, verbose=2)
print('\nTest accuracy:', test_acc)
