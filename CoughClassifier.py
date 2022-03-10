import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import layers
import tensorflow as tf
from sklearn.metrics import confusion_matrix
from tensorflow import keras
from keras.preprocessing import image
from tensorflow.keras.models import load_model

from os import path
                                                                       
dst = "coughtest.wav"
dim=(150,150)
model = load_model('cough2.h5')
def Classifier(file):
  import librosa
  samples, sample_rate = librosa.load(dst, sr=None)
  sgram = librosa.stft(samples)
  sgram_mag, _ = librosa.magphase(sgram)
  mel_scale_sgram = librosa.feature.melspectrogram(S=sgram_mag, sr=sample_rate)
  mel_sgram = librosa.amplitude_to_db(mel_scale_sgram, ref=np.min)
  print(mel_sgram.shape)
  import cv2
  mel_sgram = cv2.resize(mel_sgram, dim, interpolation = cv2.INTER_AREA)
  img2 = np.zeros((150,150,3))
  img2[:,:,0] = mel_sgram
  img2[:,:,1] = mel_sgram
  img2[:,:,2] = mel_sgram

 
  img_array = keras.preprocessing.image.img_to_array(img2)
  img_array = tf.expand_dims(img_array, 0) # Create a batch

  predictions = model.predict(img_array)
  score = tf.nn.softmax(predictions[0])

  print(
      "This image most likely belongs to {} with a {:.2f} percent confidence."
      .format(np.argmax(score), 100 * np.max(score))
  )

  if np.argmax(score)== 1:
    print("You might have covid. We recommend you to get tested")
    return 1
  else:
      print("You still might have covid but I clear you")
      return 0
if __name__=='__main__' :
  Classifier(dst)
