import logging

import tensorflow as tf

from data import get_data

file_handler = logging.FileHandler("haha.log", "w", "utf8")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.INFO)
MODEL_PATH = "model/haha.ckpt"


def get_layer(input, input_cnt, output_cnt, use_activite=True):
    w = tf.Variable(tf.random_normal([input_cnt, output_cnt]) * 0.1)
    b = tf.Variable(tf.random_normal([output_cnt]))
    output = tf.matmul(input, w) + b
    if use_activite:
        output = tf.nn.sigmoid(output)
    return output


def build_net(a):
    x_input = tf.placeholder(tf.float32, (None, 16))
    y_input = tf.placeholder(tf.float32, (None, 3))
    nowlayer = x_input
    for i in range(1, len(a)):
        nowlayer = get_layer(nowlayer, a[i - 1], a[i], i != len(a) - 1)
    return x_input, y_input, nowlayer


x_input, y_input, y_output = build_net([16, 300, 3])
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_input, logits=y_output))
optimizer = tf.train.AdamOptimizer(learning_rate=0.1)
train_step = optimizer.minimize(loss)
accuracy = tf.reduce_sum(tf.cast(tf.equal(tf.argmax(y_output, axis=1), tf.argmax(y_input, axis=1)), tf.float32))
initializer = tf.global_variables_initializer()

x, y = get_data()
x = x[:10000]
y = y[:10000]
BATCHSIZE = 120


def get_batch():
    if not hasattr(get_batch, "last"):
        get_batch.last = -BATCHSIZE
    get_batch.last += BATCHSIZE
    if get_batch.last >= len(x):
        get_batch.last = 0
    beg = get_batch.last
    end = len(x) if beg + 2 * BATCHSIZE >= len(x) else beg + BATCHSIZE
    return x[beg:end], y[beg:end]


def train():
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(initializer)
        for epoch in range(10000):
            for step in range(len(x) // BATCHSIZE):
                x_sample, y_sample = get_batch()
                _, lo = sess.run([train_step, loss], feed_dict={
                    x_input: x_sample,
                    y_input: y_sample
                })
            if epoch % 10 == 0:
                acc_sum = 0
                for i in range(0, len(x), BATCHSIZE):
                    acc = sess.run(accuracy, feed_dict={
                        x_input: x[i:i + BATCHSIZE],
                        y_input: y[i:i + BATCHSIZE]
                    })
                    acc_sum += acc
                print(acc_sum / len(x))
                logging.info("{} {}".format(epoch, acc_sum / len(x)))
                if acc_sum == len(x):
                    saver.save(sess, MODEL_PATH)
                    break


def test():
    saver = tf.train.Saver()
    with tf.Session() as sess:
        # sess.run(initializer)
        saver.restore(sess, MODEL_PATH)
        acc_sum = 0
        for i in range(0, len(x), BATCHSIZE):
            acc = sess.run(accuracy, feed_dict={
                x_input: x[i:i + BATCHSIZE],
                y_input: y[i:i + BATCHSIZE]
            })
            acc_sum += acc
        print(acc_sum / len(x))
        if acc_sum == len(x):
            print("all right")


train()
# test()
