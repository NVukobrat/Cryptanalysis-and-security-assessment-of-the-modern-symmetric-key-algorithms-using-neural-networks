import tensorflow as tf

from Configuration.Config.ModelsConfig import ANNConfig


def variable_summaries(var):
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar('stddev', stddev)
        tf.summary.scalar('max', tf.reduce_max(var))
        tf.summary.scalar('min', tf.reduce_min(var))
        tf.summary.histogram('histogram', var)


def write_summaries(sess):
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter(
        ANNConfig.LOG_DIR + 'train/',
        sess.graph
    )
    test_writer = tf.summary.FileWriter(
        ANNConfig.LOG_DIR + 'test/',
    )

    return merged, train_writer, test_writer


def save_model(sess, saver):
    saver.save(
        sess,
        ANNConfig.LOG_DIR,  # + "model/"
    )
