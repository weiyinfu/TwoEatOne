import keras
from keras.layers import *

x_input = Input((4, 4, 1))

m44 = Conv2D(3, (4, 4), activation='relu', padding='SAME')(x_input)
m44 = Conv2D(3, (4, 4), activation='relu', padding='VALID')(m44)

m33 = Conv2D(3, (3, 3), activation='relu', padding='SAME')(x_input)
m33_pool = MaxPool2D()(m33)
m33 = Conv2D(3, (1, 1), activation='relu', padding='VALID')(m33_pool)
m33_pool = MaxPool2D()(m33)

m22 = Conv2D(3, (2, 2), activation='relu', padding='SAME')(x_input)
m22_pool = MaxPool2D()(m22)
m22 = Conv2D(3, (1, 1), activation='relu', padding='VALID')(m22_pool)
m22_pool = MaxPool2D()(m22)

m = concatenate([Flatten()(m33_pool), Flatten()(m22_pool), Flatten()(m44)])
m = BatchNormalization()(m)
m = Dense(100, activation='relu')(m)
m = BatchNormalization()(m)
m = Dense(100, activation='relu')(m)
m = BatchNormalization()(m)
logits = Dense(3, activation='softmax')(m)
m = keras.models.Model(inputs=x_input, outputs=logits)
m.compile(keras.optimizers.Adam(0.05), "categorical_crossentropy", metrics=['accuracy'])

import data

x, y = data.get_data(True, True)
x = x.reshape(-1, 4, 4, 1)
m.fit(x, y)
