import tensorflow as tf# %%
target_height=254
target_width=254
path="anuj.jpeg"
image = tf.keras.preprocessing.image.load_img(path)
resized_image=tf.image.resize_with_pad(
    image, target_height, target_width, method=tf.image.ResizeMethod.BILINEAR,
    antialias=False
)

tf.keras.utils.save_img("resized_anuj",
resized_image, file_format="png")