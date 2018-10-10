import data
from keras import *

a = models.Sequential()
a.add(layers.Dense(300, activation="relu"))
a.add(layers.Dense(300, activation="relu"))
a.add(layers.Dense(3, activation="softmax"))
a.compile(optimizers.Adam(0.2), losses.categorical_crossentropy, ['accuracy'])
x, y = data.get_data(True)
# x = x[:1000]
# y = y[:1000]
a.fit(x, y, batch_size=120, epochs=10000, verbose=1)
