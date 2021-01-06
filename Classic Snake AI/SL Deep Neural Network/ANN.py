import numpy as np 
import pandas as pd 
import tensorflow as tf 
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from sklearn.model_selection import train_test_split

#Importing Dataset
dataset = pd.read_csv("training_data.csv",header=None)
input_vals = dataset.iloc[:,:-1].values
outs = dataset.iloc[:,-1].values

in_train, in_test, out_train, out_test = train_test_split(input_vals,outs,test_size = 0.2, random_state = 0)

#Feature Scaling
sc = StandardScaler()
in_train=sc.fit_transform(in_train)
in_test = sc.transform(in_test)

#Fixing Output
lb = LabelBinarizer()
lb.fit(range(max(outs)+1))
outs = lb.transform(outs)
print(outs)
#Building the Neural Network

ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=8,activation="relu")) # First Hidden Layer
ann.add(tf.keras.layers.Dense(units=8,activation="relu")) # Second Hidden Layer
ann.add(tf.keras.layers.Dense(units=4,activation="softmax")) # Output Layer

ann.compile(optimizer = "adam", loss = "categorical_crossentropy", metrics = ["accuracy"])
ann.fit(in_train,out_train,batch_size = 32,epochs=1000)

print(ann.predict(sc.transform([[0,100,100,0,100,100,0.6,0.4,100,0.7,100,100,0.9998,100,100,0.2334,100,0.658,0.4,100,0,0,100,100]])))
