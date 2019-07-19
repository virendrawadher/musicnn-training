import tensorflow as tf

def dense_cnns(front_end_output, is_training, num_filt):

    front_end_output = tf.expand_dims(front_end_output, 3)

    # conv layer 1 - adapting dimensions
    front_end_pad = tf.pad(front_end_output, [[0, 0], [3, 3], [0, 0], [0, 0]], "CONSTANT")
    conv1 = tf.layers.conv2d(inputs=front_end_pad,
                             filters=num_filt,
                             kernel_size=[7, front_end_pad.shape[2]],
                             padding="valid",
                             activation=tf.nn.relu)
    bn_conv1 = tf.layers.batch_normalization(conv1, training=is_training)
    bn_conv1_t = tf.transpose(bn_conv1, [0, 1, 3, 2])

    # conv layer 2 - residual connection
    bn_conv1_pad = tf.pad(bn_conv1_t, [[0, 0], [3, 3], [0, 0], [0, 0]], "CONSTANT")
    conv2 = tf.layers.conv2d(inputs=bn_conv1_pad,
                             filters=num_filt,
                             kernel_size=[7, bn_conv1_pad.shape[2]],
                             padding="valid",
                             activation=tf.nn.relu)
    bn_conv2 = tf.layers.batch_normalization(conv2, training=is_training)
    conv2 = tf.transpose(bn_conv2, [0, 1, 3, 2])
    res_conv2 = tf.add(conv2, bn_conv1_t)

    # conv layer 3 - residual connection
    bn_conv2_pad = tf.pad(res_conv2, [[0, 0], [3, 3], [0, 0], [0, 0]], "CONSTANT")
    conv3 = tf.layers.conv2d(inputs=bn_conv2_pad,
                             filters=num_filt,
                             kernel_size=[7, bn_conv2_pad.shape[2]],
                             padding="valid",
                             activation=tf.nn.relu)
    bn_conv3 = tf.layers.batch_normalization(conv3, training=is_training)
    conv3 = tf.transpose(bn_conv3, [0, 1, 3, 2])
    res_conv3 = tf.add(conv3, res_conv2)

    return [front_end_output, bn_conv1_t, res_conv2, res_conv3]

