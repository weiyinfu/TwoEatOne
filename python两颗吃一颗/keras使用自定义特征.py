from keras import *

import data
import feature_extrator

a = models.Sequential()
a.add(layers.Dense(20, activation="relu"))
a.add(layers.Dense(3, activation="softmax"))
a.compile(optimizers.Adam(0.1), losses.categorical_crossentropy, ['accuracy'])
x, y = data.get_data(True, True)
x = feature_extrator.extract(x)
a.fit(x, y, batch_size=120, epochs=10000, verbose=1)
