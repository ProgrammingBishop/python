import gym
import tensorflow as tf
import numpy      as np

num_inputs  = 4
num_hidden  = 4
num_outputs = 1

initializer = tf.layers.variance_scaling_initializer()

X = tf.placeholder( tf.float32, shape = [ None, num_inputs ] )