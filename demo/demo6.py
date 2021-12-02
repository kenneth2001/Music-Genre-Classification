import tensorflow as tf
import numpy as np
import tensorflow.keras as keras

x = np.random.uniform(-100, 100, size=(1000, 2))
y = []

for i in x:
    if i[0] + i[1] > 0:
        y.append(0)
    else:
        y.append(1)

y = np.array(y)

model = tf.keras.models.Sequential()

model.add(
    tf.keras.layers.Dense(2, input_shape=(2,)))
model.add(
    tf.keras.layers.Dense(4, activation='relu'))
model.add(
    tf.keras.layers.Dense(4, activation='relu'))
model.add(
    tf.keras.layers.Dense(2, activation='softmax'))

optimiser = tf.keras.optimizers.Adam()
model.compile(
    optimizer=optimiser, 
    loss='sparse_categorical_crossentropy', 
    metrics=['accuracy'])

model.fit(x, y, epochs=10, batch_size=32)

ann_viz(model, title="My first neural network")