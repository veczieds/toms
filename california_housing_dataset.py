# -*- coding: utf-8 -*-
"""california-housing-dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NtkeMxTzUJ9n9A9LwZCYqNq_KD-BshXp
"""

import numpy as np
import matplotlib.pyplot as plt
import sklearn.datasets

X, Y = sklearn.datasets.fetch_california_housing(return_X_y=True)
Y = np.expand_dims(Y, axis=1)

print(X.shape)
print(Y.shape)


class Variable:
    def __init__(self, value):
        self.value = value
        self.grad = np.zeros_like(value)


class LayerLinear:
    def __init__(self, in_features, out_features):
        self.W = Variable(
            value=np.zeros((out_features, in_features))
        )
        self.b = Variable(
            value=np.zeros((out_features,))
        )
        self.x = None
        self.output = None

    def forward(self, x):
        self.x = x
        self.output = Variable(
            np.matmul(self.W.value, x.value.transpose()).transpose() + self.b.value
        )
        return self.output

    def backward(self):
        self.b.grad = 1 * self.output.grad  # Linear(x, W, b) / db = 1

        self.W.grad = np.matmul(  # Linear(x, W, b) / dW = x
            np.expand_dims(self.output.grad, axis=2),
            np.expand_dims(self.x.value, axis=1)
        )

        self.x.grad = np.matmul(  # Linear(x, W, b) / dx = W
            self.W.value.transpose(),
            self.output.grad.transpose()
        ).transpose()


class LossMSE:
    def __init__(self):
        self.y = None
        self.y_prim = None

    def forward(self, y, y_prim):
        self.y = y
        self.y_prim = y_prim
        loss = np.mean((y.value - y_prim.value) ** 2)
        return loss

    def backward(self):
        self.y_prim.grad = -2 * (self.y.value - self.y_prim.value)


import pdb

model = [
    LayerLinear(in_features=8, out_features=64),  # input 8 ipashibas majam nahuj 4?
    LayerLinear(in_features=64, out_features=64),
    LayerLinear(in_features=64, out_features=1), # output majas cena 1 dimensija
]
loss_fn = LossMSE()
BATCH_SIZE = 16
LEARNING_RATE = 1e-4

iterations = []
losses_2 = []
iters = 0
for epoch in range(80):
    print("Epoch: ", epoch)
    losses = []
    for idx in range(0, len(X) - BATCH_SIZE, BATCH_SIZE):
        iters += 1
        x = X[idx:idx + BATCH_SIZE]
        y = Y[idx:idx + BATCH_SIZE]

        out = Variable(x)
        for layer in model:
            out = layer.forward(out)
        y_prim = out

        losses.append(loss_fn.forward(Variable(y), y_prim))

        loss_fn.backward()
        for layer in reversed(model):
            layer.backward()
            if isinstance(layer, LayerLinear):
                layer.W.value -= np.mean(layer.W.grad, axis=0) * LEARNING_RATE
                layer.b.value -= np.mean(layer.b.grad, axis=0) * LEARNING_RATE

        #print(f'loss: {np.mean(losses)}')
        iterations.append(iters)
        losses_2.append(np.mean(losses))


plt.plot(iterations, losses_2)
plt.title("Knax mega lox")
plt.show()

# $Linear(x, W, b) = W\cdot x + b$
#
# $y_1 \in Y$
#
# $x_1 \in X$
#
# $y_1' = Linear(x1,W,b)$
#
# $ L(y, y') = (y - y')^2 $
#
# $ L(y, y') \rightarrow 0 $
#
# $ L(y, Linear(x, W, b)) \rightarrow 0 $
#
# $ \frac{ \partial L(y, Linear(x, W, b)) }
# {\partial W } =... $
#
# $ W_{t+1} = W_{t} - \frac{ \partial L(y, Linear(x, W, b)) }{\partial W } \alpha $
#
# $ b_{t+1} = b_{t} - \frac{ \partial L(y, Linear(x, W, b)) }{\partial W } \alpha $
#
# $ \frac{Linear(x, W, b) }{\partial W } = \frac {Wx + b}{\partial W} = W^{1-1} x + 0 = W^0X + 0 = 1 x = x $
#
# $ \frac{Linear(x, W, b) }{\partial b } = \frac {Wx + b}{\partial b} = 1 $
#
# $ \frac{f(g(x))}{\partial g(x)} = \frac{f(g(x))}{\partial g(x)} \frac{g(x)}{\partial x} $
#
#
# $ \frac{L(y, y') }{\partial y'} = \frac{(y - y')^2}{\partial y'} = \frac{(y-y')}{\partial y'} \frac{(y-y')^2}{\partial (y-y')} = -2 (y-y') $
#
# $ \frac{ \partial L(y, Linear(x, W, b)) }
# {\partial W } = -2 (y-y') *x $
#
# $ \frac{ \partial L(y, Linear(x, W, b)) }
# {\partial W } = -2 (y-y') *1 $