import numpy as np 
import pandas as pd 
import tensorflow as tf 
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class NeuralNet:
    ann = None
    sc = None
    results = None
    def __init__(self):
        #Importing Dataset
        dataset = pd.read_csv("training_data.csv",header=None)
        input_vals = dataset.iloc[:,:-1].values
        outs = dataset.iloc[:,-1].values

        in_train, in_test, out_train, out_test = train_test_split(input_vals,outs,test_size = 0.2, random_state = 0)

        #Feature Scaling
        self.sc = StandardScaler()
        in_train=self.sc.fit_transform(in_train)
        in_test = self.sc.transform(in_test)

        #Fixing Output
        lb = LabelBinarizer()
        lb.fit(range(max(outs)+1))
        outs = lb.transform(outs)

        #Building the Neural Network
        nn = tf.keras.models.Sequential()
        nn.add(tf.keras.layers.Dense(units=8,activation="relu")) # First Hidden Layer
        nn.add(tf.keras.layers.Dense(units=8,activation="relu")) # Second Hidden Layer
        nn.add(tf.keras.layers.Dense(units=4,activation="softmax")) # Output Layer

        nn.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"]);
        self.results = nn.fit(in_train,out_train,validation_data=(in_test, out_test),epochs=10,verbose=0)

        self.ann = nn
        
    def predict(self,data):
        ourDirec = self.ann.predict(self.sc.transform(data)).tolist()[0]
        DirecLst = [[1,0],[0,-1],[-1,0],[0,1]]
        return DirecLst[ourDirec.index(max(ourDirec))]

data = [[0,100,100,0,100,100,0.6,0.4,100,0.7,100,100,0.9998,100,100,0.2334,100,0.658,0.4,100,0,0,100,100]]
myAnn = NeuralNet()

plt.plot((myAnn.results).history['loss'], label='loss')
plt.plot((myAnn.results).history['val_loss'], label='val_loss')
plt.legend()

plt.plot(myAnn.results.history['acc'], label='acc')
plt.plot(myAnn.results.history['val_acc'], label='val_acc')
plt.legend()
plt.show()
print(myAnn.predict(data))


