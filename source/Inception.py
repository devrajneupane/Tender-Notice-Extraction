import tensorflow as tf
from tensorflow import keras


class InceptionUnit(keras.layers.Layer):
    def __init__(self, filters = [64, 96, 16, 128, 32, 32], strides=1, activation="relu", **kwargs):
        super().__init__(**kwargs)
        self.activation = keras.activations.get(activation)

        self.convo_1x1_zero = [ keras.layers.Conv2D(filters[0], 1, strides = strides, padding = "same", use_bias = False),
         keras.layers.BatchNormalization(),
         self.activation]

        self.convo_1x1_first =[ keras.layers.Conv2D(filters[1], 1, strides = strides, padding = "same", use_bias = False),
         keras.layers.BatchNormalization(),
         self.activation]

        self.convo_1x1_second = [ keras.layers.Conv2D(filters[2], 1, strides = strides, padding = "same", use_bias = False),
         keras.layers.BatchNormalization(),
         self.activation]

        self.max_pool_3x3_third = keras.layers.MaxPool2D(pool_size=3, strides=strides, padding = "same")

        self.convo_3x3_first2 = [ keras.layers.Conv2D(filters[3], 3, strides = strides, padding = "same", use_bias = False),
         keras.layers.BatchNormalization(),
         self.activation]

        self.convo_5x5_second2 = [ keras.layers.Conv2D(filters[4], 3, strides = strides, padding = "same", use_bias = False),
         keras.layers.BatchNormalization(),
         self.activation]

        self.convo_1x1_third2 = [ keras.layers.Conv2D(filters[5], 1, strides = strides, padding = "same", use_bias = False),
         keras.layers.BatchNormalization(),
         self.activation]

        # self.concat = keras.layers.Concatenate([self.convo_1x1_zero_at, self.convo_3x3_first2_at, self.convo_5x5_second2_at, self.convo_1x1_third2_at])
        self.concat = keras.layers.Concatenate()


    def call(self, inputs):
        z0, z1, z2, z3 = inputs, inputs, inputs, inputs
        for layer in self.convo_1x1_zero:
            z0 = layer(z0)

        for layer in self.convo_1x1_first:
            z1 = layer(z1)

        for layer in self.convo_1x1_second:
            z2 = layer(z2)

        z3 = self.max_pool_3x3_third(z3)

        for layer in self.convo_3x3_first2:
            z1 = layer(z1)
        
        for layer in self.convo_5x5_second2:
            z2 = layer(z2)

        for layer in self.convo_1x1_third2:
            z3 = layer(z3)

        return self.concat([z0, z1, z2, z3])

    
    def build_graph(self, dim = (224, 224, 64), to_file="Inception.png", **kwargs):
        x = keras.layers.Input(shape=(dim))
        model = keras.Model(inputs=[x], outputs=self.call(x))
        keras.utils.plot_model(model, to_file=to_file, **kwargs)

if __name__ == "__main__":
    inception = InceptionUnit()
    inception.build_graph(to_file="D:\Programming\Python\Tender-Notice-Extraction\img\Inception.png")
