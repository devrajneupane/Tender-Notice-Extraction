import tensorflow as tf
from tensorflow import keras


class ResidualUnit(keras.layers.Layer):
    def __init__(self, filters, strides=1, activation="relu", **kwargs):
        super().__init__(**kwargs)
        self.activation = keras.activations.get(activation)
        self.main_layers =[
            keras.layers.Conv2D(filters, 3, strides = strides, padding = "same", use_bias = False),
            keras.layers.BatchNormalization(),
            self.activation,
            keras.layers.Conv2D(filters, 3, strides = 1, padding = "same", use_bias = False),
            keras.layers.BatchNormalization()
        ]
        self.skip_layers = []
        if strides > 1:
            self.skip_layers = [
                keras.layers.Conv2D(filters, 1, strides = strides, padding = "same", use_bias = False),
                keras.layers.BatchNormalization()
            ]

    def call(self, inputs):
        z = inputs
        for layer in self.main_layers:
            z = layer(z)
        skip_z = inputs
        for layer in self.skip_layers:
            skip_z = layer(skip_z)
        return self.activation(z + skip_z)

    def build_graph(self, dim = (224, 224, 64),
        to_file='ResNet.png',
        show_shapes=False,
        show_dtype=False,
        show_layer_names=True,
        rankdir='TB',
        expand_nested=False,
        dpi=96,
        layer_range=None,
        show_layer_activations=False):
        x = keras.layers.Input(shape=(dim))
        model = keras.Model(inputs=[x], outputs=self.call(x))
        keras.utils.plot_model(model,
            to_file=to_file,
            show_shapes=show_shapes,
            show_dtype=show_dtype,
            show_layer_names=show_layer_names,
            rankdir=rankdir,
            expand_nested=expand_nested,
            dpi=dpi,
            layer_range=layer_range,
            show_layer_activations=show_layer_activations)
        
if __name__ == "__main__":
    model = ResidualUnit(filters=64, strides=1, activation="relu")
    model.build_graph()

        
    

