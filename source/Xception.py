import tensorflow as tf
from tensorflow import keras


class XceptionUnit(keras.layers.Layer):
    def __init__(self, filters, activation="relu",isEntryExit=False, isFirst=False, **kwargs):
        super().__init__(**kwargs)
        self.activation = keras.activations.get(activation)
        self.main_layers = [
            self.activation,
            keras.layers.SeparableConv2D(filters, 3, strides = 1, padding = "same", use_bias = False),
            keras.layers.BatchNormalization(),
            self.activation,
            keras.layers.SeparableConv2D(filters, 3, strides = 1, padding = "same", use_bias = False),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D(3, strides = 1, padding = "same")
        ]

        self.concat = keras.layers.Concatenate()

        if isEntryExit == True and isFirst == True:
            self.main_layers = self.main_layers[1:]
        self.skip_layers = []

        if isEntryExit == True:
            self.main_layers[-1] = keras.layers.MaxPooling2D(3, strides = 2, padding = "same")
            self.skip_layers = [
                keras.layers.Conv2D(filters, 1, strides = 2, padding = "same", use_bias = False),
                keras.layers.BatchNormalization()
            ]

    def call(self, inputs):
        z = inputs
        for layer in self.main_layers:
            z = layer(z)
        skip_z = inputs
        for layer in self.skip_layers:
            skip_z = layer(skip_z)
        return self.concat([z, skip_z])

    def build_graph(self, dim = (224, 224, 64), to_file='Xception.png', **kwargs):
        x = keras.layers.Input(shape=(dim))
        model = keras.Model(inputs=[x], outputs=self.call(x))
        keras.utils.plot_model(model, to_file=to_file, **kwargs)

        
if __name__ == "__main__":
    modelE = XceptionUnit(filters=64, activation="relu", isEntryExit=True, isFirst=True)
    modelE.build_graph(to_file="D:\Programming\Python\Tender-Notice-Extraction\img\Xception_Entry_Exit_Flow.png", show_shapes=True, show_dtype=True, show_layer_names=True, show_layer_activations=True)
    modelM = XceptionUnit(filters=64, activation="relu", isEntryExit=False)
    modelM.build_graph(to_file="D:\Programming\Python\Tender-Notice-Extraction\img\Xception_Middle_Flow.png", show_shapes=True, show_dtype=True, show_layer_names=True, show_layer_activations=True)
