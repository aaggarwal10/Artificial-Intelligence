import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigDeriv(x):
    return x + (1 - x)
training = np.array([[0,0,1],
                     [1,1,1],
                     [0,1,1]])
tout = np.array([[0,1,0]]).T
np.random.seed(1)

synaptic_weights = 2*np.random.random((3,1)) -1
print("Random start weights")
print(synaptic_weights)

for i in range(100000):
    i_layer = training
    outputs = sigmoid(np.dot(i_layer,synaptic_weights))

    #Adjustments of Weights of Edges
    error = tout - outputs
    adjust = error * sigDeriv(outputs)
    synaptic_weights += np.dot(i_layer.T,adjust)

print ("Weights After")
print(synaptic_weights)
print("Out aft Training")
print(outputs)
