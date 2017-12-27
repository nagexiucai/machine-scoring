#!/usr/bin/env python
#coding=utf-8

import tensorflow as tf
import numpy as np
from pprint import pprint

# verify installation
# hello = tf.constant('Hello, TensorFlow!')
# sess = tf.Session()
# print(sess.run(hello))

z = tf.zeros([3,4,5])
pprint(z)
