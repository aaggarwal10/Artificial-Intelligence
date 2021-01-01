import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

training = np.array([[0,0,1],
                     [1,1,1],
                     [0,1,1]]).T
np.random.seed(1)

synaptic_weights = 2*random.random((3,1)) -1
print("Random start weights")
print(synaptic_weights)
for i in range(1):
    i_layer = training_inputs
    outputs = sigmoid(np.dot(i_layer,synaptic_weights))
print("Out aft Training")
print(outputs)
