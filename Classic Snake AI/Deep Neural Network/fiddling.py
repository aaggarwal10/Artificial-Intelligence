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

"""
Proto 1: Snake AI
-> Start with 8 Input Nodes for each direction from head including nodes.
-> For each direction encode 3 hidden layers that hold 3 different types of
   info:
       -> Distance to wall
       -> Distance to a Body Piece
           -> if not set to really high number
       -> Distance to Food (if any)
           -> if not set to really high number
-> Output Nodes: 4 Nodes representing Cardinal Direction snake takes.

This entire process was what Code Bullet used for his first Snake AI. I am
going to use it as a start point. Through other research I found that this AI
needs improvement through other heuristic searches and algorithms. (i.e. Monte
Carlo, DNQ algorithm, etc.)

"""
