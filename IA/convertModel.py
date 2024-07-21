import os
#Désactiver les optimisations oneDNN
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

#Convert Keras model to tensorflow lite
import tensorflow as tf

# Charger le modèle Keras
model = tf.keras.models.load_model("C:\\Users\\nehem\\Documents\\Projet\\Trad-glasses\\IA\\YSML.h5")

# Convertir le modèle en TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Enregistrer le modèle TensorFlow Lite
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
