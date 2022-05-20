import numpy as np

class Network() :
  def __init__(self) :
    self.fitness = 0 # 적합도 초기화

    hidden_layer = 10 # hidden layer 값을 10으로 지정
    self.w1 = np.random.randn(4, hidden_layer)
    self.w2 = np.random.randn(hidden_layer, hidden_layer)
    self.w3 = np.random.randn(hidden_layer, 5) # w 값들을 무작위로 지정
    
  def decisionOutput(self, inputs) : # 방향 결정 (아웃풋) [상, 하, 좌, 우, 가만히]
    net = np.matmul(inputs, self.w1)
    net = np.tanh(net)
    
    net = np.matmul(net, self.w2)
    net = np.tanh(net)

    net = np.matmul(net, self.w3)
    net = np.tanh(net)

    net = self.softmax(net) # 8 개의 방향 중 다중 분류를 위한, Softmax 적용
    return net

  def softmax(self, x) :
    return np.exp(x) / np.sum(np.exp(x), axis=0)
