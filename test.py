#!/usr/bin/env python
#coding=utf-8

import core

from tensorflow.contrib.learn.python.learn.datasets.mnist import load_mnist
load_mnist()

x_data = core.np.float32(core.np.random.rand(2, 100))
y_data = core.np.dot([0.100, 0.200], x_data) + 0.300

b = core.tf.Variable(core.tf.zeros([1]))
w = core.tf.Variable(core.tf.random_uniform([1, 2], -1.0, 1.0))
y = core.tf.matmul(w, x_data) + b

loss = core.tf.reduce_mean(core.tf.square(y - y_data))
optimazer = core.tf.train.GradientDescentOptimizer(0.5)
train = optimazer.minimize(loss)

init = core.tf.initialize_all_variables()
sess = core.tf.Session()
sess.run(init)

for step in range(0, 201):
    sess.run(train)
    if step%20 == 0:
        print(step, sess.run(w), sess.run(b))
