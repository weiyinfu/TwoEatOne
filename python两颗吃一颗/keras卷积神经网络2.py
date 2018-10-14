import keras
from keras.layers import *

x_input = Input((4, 4, 1))
x_flat = Flatten()(x_input)

"""
统计每个棋子的活动能力,使用2*2卷积核
因为需要统计权值,所以多来几层
"""
free_space = Conv2D(2, (2, 2), padding='SAME', activation='sigmoid')(x_input)
free_space = Conv2D(2, (2, 2), padding='VALID')(free_space)

"""
吃子观,2*3和3*2的卷积核
"""
eat1 = Conv2D(2, (2, 3), padding='VALID', activation='sigmoid')(x_input)
eat2 = Conv2D(2, (3, 2), padding='VALID', activation='sigmoid')(x_input)

m = Concatenate()([Flatten()(i) for i in (eat1, eat2, free_space)] + [x_flat])
"""
手写resnet
"""
m = Dense(300, activation='relu')(Concatenate()([m, x_flat]))
m = Dense(16, activation='relu')(Concatenate()([m, x_flat]))
logits = Dense(3, activation='softmax')(m)
m = keras.models.Model(inputs=x_input, outputs=logits)
m.compile(keras.optimizers.RMSprop(0.01), "categorical_crossentropy", metrics=['accuracy'])

import data

x, y = data.get_data(True, True)
x = x.reshape(-1, 4, 4, 1)
batch_size = 120
m.fit(x, y, batch_size=batch_size, epochs=1000)
