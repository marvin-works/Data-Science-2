
import tensorflow as tf

# node1 = tf.constant(3.0, tf.float32)
# node2 = tf.constant(4.0)

# print(node1.numpy())
# print(node2.numpy())

# a= tf.constant(5)
# b= tf.constant(2)
# c= tf.constant(3)

# d= tf.multiply(a, b)
# e= tf.add(c, b)
# f= tf.subtract(d, e)

# print(f.numpy())

a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)

adder_node = a+b

