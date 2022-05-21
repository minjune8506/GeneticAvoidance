import numpy as np

class Network() :
  def __init__(self) :
    self.fitness = 0 # 적합도
    hidden_layer = 10 # hidden layer 노드 갯수
    self.W1 = np.random.randn(2, hidden_layer)
    self.W2 = np.random.randn(hidden_layer, hidden_layer)
    self.W3 = np.random.randn(hidden_layer, 5) # w 값들을 무작위로 지정
    
  def decisionOutput(self, inputs) : # 방향 결정 (아웃풋) [상, 하, 좌, 우, 가만히]
    net = np.matmul(inputs, self.W1)
    net = np.tanh(net)
    
    net = np.matmul(net, self.W2)
    net = np.tanh(net)

    net = np.matmul(net, self.W3)
    net = np.tanh(net)

    net = self.softmax(net) # 5 개의 방향 중 다중 분류를 위한, Softmax 적용
    return net

  def softmax(self, x) :
    return np.exp(x) / np.sum(np.exp(x), axis=0)
