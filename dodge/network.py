import numpy as np

class Network() :
  def __init__(self) :
    self.fitness = 0 # 적합도
    hidden_layer1 = 8 # hidden layer 노드 갯수
    hidden_layer2 = 4 # hidden layer 노드 갯수
    self.W1 = np.random.randn(6, hidden_layer1)
    self.W2 = np.random.randn(hidden_layer1, hidden_layer2)
    self.W3 = np.random.randn(hidden_layer2, 8) # w 값들을 무작위로 지정
    
  def decisionOutput(self, inputs) : # 방향 결정 (아웃풋) [상, 하, 좌, 우, 대각 4개]
    net = np.matmul(inputs, self.W1)
    net = np.tanh(net)
    
    net = np.matmul(net, self.W2)
    net = np.tanh(net)

    net = np.matmul(net, self.W3)
    net = np.tanh(net)

    net = self.softmax(net) # 8 방향을 결정하기 위한 softmax
    return net

  def sigmoid(x):
    return 1 / (1 + np.exp(-x))

  def softmax(self, x) :
    return np.exp(x) / np.sum(np.exp(x), axis=0)
