import pandas as pd
import numpy as np
import scipy.io.wavfile

num = 2000
path = input("Please enter the path of the audio file:")

sampFreq, sound = scipy.io.wavfile.read(path)
signal = sound
fft_spectrum = np.fft.rfft(signal)
freq = np.fft.rfftfreq(signal.size, d=1./sampFreq)
fft_spectrum_abs = np.abs(fft_spectrum)

x = np.column_stack((np.round(freq, 1), np.round(fft_spectrum_abs)))
data = np.array(sorted(x, key=lambda x: x[1], reverse=True)[:num])[:, 0]

tmpdf = pd.DataFrame(data.reshape(1,-1), columns=[f"x_{i}" for i in range(num)])
print(tmpdf)
