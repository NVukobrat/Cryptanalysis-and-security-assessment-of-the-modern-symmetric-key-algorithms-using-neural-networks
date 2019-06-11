import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

from Configuration.Config.ModelsConfig import ANNConfig
from Models.Dataset.Read import read_cipher_key_group
from Models.Debug.TensorBoard import variable_summaries, write_summaries, save_model

# Dataset
ciphers, key_groups = read_cipher_key_group(
    ANNConfig.DATASET_PATH,
    additional_message='Reading Cipher dataset',
    max_size=30000,
)

# ######### CONFIGURATION ######### #

# TF + Docker
# config = tf.ConfigProto()
# config.intra_op_parallelism_threads = 2
# config.inter_op_parallelism_threads = 2
# tf.Session(config=config)

# Debug
host = "localhome:6007"

# Parameters
learning_rate = 0.001
num_steps = 1000
batch_size = 35
display_step = 1
save_model_step = 100

# TODO: BF Parameters?
# TODO: Use couple of cipher blocks instead of zero padding?
# TODO: Genetic algorithm for finding hyper-parameters.
# Architecture
n_hidden_1 = 2048
n_hidden_2 = 4096
n_hidden_3 = 1024
num_input = max([len(i) for i in ciphers])  # Defined by cipher max value - zero padding
num_classes = 2

# ######### CONFIGURATION ######### #

# ######### VARIABLES ######### #

# tf Graph input
X = tf.placeholder("float", [None, num_input])
Y = tf.placeholder("float", [None, num_classes])

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([num_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'h3': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3])),
    'out': tf.Variable(tf.random_normal([n_hidden_3, num_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'b3': tf.Variable(tf.random_normal([n_hidden_3])),
    'out': tf.Variable(tf.random_normal([num_classes]))
}

# Batch
processed_batches = 0


# ######### VARIABLES ######### #


def construct_neural_net(x):
    with tf.name_scope('weights'):
        variable_summaries(weights['h1'])
        variable_summaries(weights['h2'])
        variable_summaries(weights['h3'])
        variable_summaries(weights['out'])

    with tf.name_scope('biases'):
        variable_summaries(biases['b1'])
        variable_summaries(biases['b2'])
        variable_summaries(biases['b3'])
        variable_summaries(biases['out'])

    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    activations_1 = tf.nn.relu(layer_1)
    layer_2 = tf.add(tf.matmul(activations_1, weights['h2']), biases['b2'])
    activations_2 = tf.nn.relu(layer_2)
    layer_3 = tf.add(tf.matmul(activations_2, weights['h3']), biases['b3'])
    activations_3 = tf.nn.relu(layer_3)
    out_layer = tf.matmul(activations_3, weights['out']) + biases['out']

    with tf.name_scope('pre-activate'):
        variable_summaries(layer_1)
        variable_summaries(layer_2)
        variable_summaries(layer_3)
        variable_summaries(out_layer)

    with tf.name_scope('activations'):
        variable_summaries(activations_1)
        variable_summaries(activations_2)
        variable_summaries(activations_3)

    return out_layer


def define_prediction(logits):
    prediction = tf.nn.softmax(logits)

    with tf.name_scope('softmax'):
        variable_summaries(prediction)

    return prediction


def define_loss(logits):
    loss_op = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(
            logits=logits,
            labels=Y
        )
    )
    tf.summary.scalar('cross_entropy_loss', loss_op)

    return loss_op


def define_optimizer(loss_op):
    optimizer = tf.train.AdamOptimizer(
        learning_rate=learning_rate
    )
    train_op = optimizer.minimize(
        loss_op
    )

    return train_op


def define_evaluation(prediction):
    correct_pred = tf.equal(
        tf.argmax(prediction, 1),
        tf.argmax(Y, 1)
    )
    accuracy = tf.reduce_mean(
        tf.cast(
            correct_pred,
            tf.float32
        )
    )
    tf.summary.scalar('accuracy', accuracy)

    return accuracy


def train(sess, init, train_op, x_train, y_train, loss_op, accuracy, merged, train_writer):
    # Run the initializer
    sess.run(init)

    # Model saver
    saver = tf.train.Saver()
    for step in range(1, num_steps + 1):
        # Get next batch
        batch_x, batch_y = next_batch(
            x_train,
            y_train
        )
        global processed_batches
        processed_batches += batch_size

        # Run optimization op (backprop)
        summary, _ = sess.run(
            [merged, train_op],
            feed_dict={X: batch_x, Y: batch_y}
        )
        train_writer.add_summary(summary, step)

        # Save model
        if step % save_model_step == 0:
            save_model(sess, saver)

        # Log step
        log_training_progress(step, sess, loss_op, accuracy, batch_x, batch_y)

    print("Optimization Finished!")


def next_batch(x, y):
    batch_check(x, y)

    next_cipher_batch, next_key_group_batch = create_batch(
        x,
        y,
        training=True
    )

    next_cipher_batch = np.reshape(
        next_cipher_batch,
        (batch_size, num_input)
    )
    next_key_group_batch = np.reshape(
        next_key_group_batch, (
            batch_size, num_classes)
    )

    return next_cipher_batch, next_key_group_batch


def batch_check(x, y):
    global processed_batches
    if processed_batches >= len(y) - batch_size:
        processed_batches = 0
        print("WARNING: " + "Batch started with reading same data again")


def create_batch(x, y, training=True):
    next_cipher_batch = list()
    next_key_group_batch = list()

    if training:
        batch_range = [processed_batches, processed_batches + batch_size]
    else:
        batch_range = [0, len(y)]

    for i in range(batch_range[0], batch_range[1]):
        batch_cipher = process_cipher(x, i)
        next_cipher_batch.append(batch_cipher)

        batch_key_group = process_key_group(y, i)
        next_key_group_batch.append(batch_key_group)

    return next_cipher_batch, next_key_group_batch


def process_cipher(x, i):
    cipher = x[i]
    cipher = list(map(int, list(cipher)))
    cipher = np.reshape(cipher, (-1, np.shape(cipher)[0]))
    padded_cipher = np.zeros((1, num_input))
    padded_cipher[:np.shape(cipher)[0], :np.shape(cipher)[1]] = cipher

    return padded_cipher


def process_key_group(y, i):
    key_group = int(y[i])
    if key_group == 0:
        reverse_key_group = 1
    else:
        reverse_key_group = 0
    full_key_group = [np.reshape(key_group, (-1, 1)), reverse_key_group]

    return full_key_group


def log_training_progress(step, sess, loss_op, accuracy, batch_x, batch_y):
    if step % display_step == 0 or step == 1:
        # Calculate batch loss and accuracy
        loss, acc = sess.run(
            [loss_op, accuracy],
            feed_dict={X: batch_x, Y: batch_y}
        )
        print(
            "Step " + str(step) + ", Minibatch Loss= " +
            "{:.4f}".format(loss) + ", Training Accuracy= " +
            "{:.3f}".format(acc)
        )


def evaluate(sess, x_test, y_test, accuracy, merged, test_writer):
    # Reset batch counter
    global processed_batches
    processed_batches = 0

    # Determine number of steps
    global batch_size
    test_step_num = (int(len(x_test) / batch_size))
    if test_step_num > num_steps:
        test_step_num = num_steps

    # Calculate accuracy for test set
    for step in range(1, test_step_num + 1):
        # Get next batch
        batch_x, batch_y = next_batch(
            x_test,
            y_test
        )
        processed_batches += batch_size

        summary, acc = sess.run(
            [merged, accuracy],
            feed_dict={X: batch_x, Y: batch_y}
        )
        test_writer.add_summary(summary, step)

        # Log step
        log_testing_progress(step, acc)


def log_testing_progress(step, acc):
    if step % display_step == 0 or step == 1:
        print(
            "Step " + str(step) + ", Test Accuracy=" + "{:.3f}".format(acc)
        )


def summary(x_train, y_train, x_test, y_test):
    print()
    print("### Summary ###")
    print("Sizes:")
    print("Train X: " + str(len(x_train)))
    print("Train y: " + str(len(y_train)))
    print("Test X: " + str(len(x_test)))
    print("Test y: " + str(len(y_test)))


def next_test_batch(x, y):
    next_cipher_batch, next_key_group_batch = create_batch(
        x,
        y,
        training=False
    )

    next_cipher_batch = np.reshape(
        next_cipher_batch,
        (len(y), num_input)
    )

    next_key_group_batch = np.reshape(
        next_key_group_batch,
        (len(y), num_classes)
    )

    return next_cipher_batch, next_key_group_batch


def main():
    # Train-Test split
    x_train, x_test, y_train, y_test = train_test_split(ciphers, key_groups, test_size=0.1, random_state=0)

    # Construct model
    logits = construct_neural_net(X)
    prediction = define_prediction(logits)

    # Define loss
    loss_op = define_loss(logits)

    # Define optimizer
    train_op = define_optimizer(loss_op)

    # Evaluate model
    accuracy = define_evaluation(prediction)

    # Initialize the variables (i.e. assign their default value)
    init = tf.global_variables_initializer()

    # Start training
    with tf.Session() as sess:
        # Debug
        # sess = tf_debug.TensorBoardDebugWrapperSession(sess, host)

        # Summary
        merged, train_writer, test_writer = write_summaries(sess)

        # Train
        train(sess, init, train_op, x_train, y_train, loss_op, accuracy, merged, train_writer)

        # Evaluate model
        evaluate(sess, x_test, y_test, accuracy, merged, test_writer)

    # Summary
    summary(x_train, x_test, y_train, y_test)


if __name__ == '__main__':
    main()
