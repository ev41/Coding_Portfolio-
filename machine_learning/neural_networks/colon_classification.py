#Import required libraries
#We're using the tensorflow library which allows us to build and train our machine learning model
#importing the tensorflow datasets library allows us to load datasets from their public collection

import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras




# Load the dataset
# to load the dataset with tensorflow, you have to use the tfds.load() method

#the with_true=True argument is used to retrieve info about the dataset (i.e. the number of 
    #classes and the shape of the data,
  
#the as_supervised=True arg is used to indicate that the dataset is a supervised learning 
    #dataset, which means that it has both the input data and output data for our model

#riffing off the previous point, you need to split/partition the data, so you can train
    #and validate your dataset. This is what the split= argument is for.
  
(train_dataset, test_dataset), dataset_info = tfds.load('colorectal_histology',
                                                        split=[
                                                            'train[:80%]', 'train[80%:90%]'],
                                                        with_info=True,
                                                        as_supervised=True)



# Preprocess the data
#this makes our data useable by converting it into a format that can be 
    #utilized/processed by the neural network model.
  
#We're formating the shape of the images, as well as dividing pixel values by 255 
    #so we can feed values 0-1 through the model. This is called normalization. 
    #this is how we ensure that the input data is within a standard range.
  
  
def preprocess(image, label):
    image = tf.cast(image, tf.float32)
    image = tf.image.resize(image, (96, 96))
    image /= 255
    return image, label

  
  
  
#Alrighty. Here we're implementing the map() method to apply the preprocess()
    #function to the training and testing datasets. The batch() method is used to create
    #batches of data, which is just a way to make processing efficient. 
train_dataset = train_dataset.map(preprocess).batch(32)
test_dataset = test_dataset.map(preprocess).batch(32)






# Build the model
#The Sequential model is from the Keras library. This model consists of three layers:
    # a Flatten layer (flattens iput data into a 1-dimensional array
    # a Dense (fully connected) later with 128 units
    # and another Dense layer with 10 units
    #Truthfully, a lot of this Keras stuff is kinda hazey for me, so I just followed the necessary
        #syntax within the documentation.
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(96, 96, 3)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])






# Compile the model. The optimizer is a parameter that influences the models weights and learning rate. 
    #Adam is a powerful and efficient option.
  
#loss is a parameter... ok, in short, loss calculates the neural network gradients, which adapts node weights, which (hopefully) 
    #increases the model's accuracy. This particular argument loss = "sparse_cate...entropy" is used for multi-class classification problems.
  
#metric should be self-explanatory.
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])





# This is what we use the train the model
#We're using 10 epochs, which basically means there are 10 iterations, or rounds of analysis
    #over the training dataset before we start testing the model. 
model.fit(train_dataset, epochs=10)





#so here what we're doing is evaluating the model on the test dataset using the evaluate() method
    #then we're storing the results in test_loss and test_acc.
    #the verbose=2 arg is used so we can reduce the amount of output displayed (easier on the eyes)

#Annnnd then! We print the accuracy, which gives us a good idea of how well the model actually 
    #classifies the images in the test dataset. Pretty cool stuff!
test_loss, test_acc = model.evaluate(test_dataset, verbose=2)
print('\nTest accuracy:', test_acc)



#NOTE TO SELF: the model actally didn't do toooooooo well. Only 42% accuracy. Perhaps I should
    #try cleaing the dataset?
  
