import scipy.io.wavfile
import pandas as pd
import numpy as np

path = input("Please enter the path of the audio file:")
print('')

y, signal = scipy.io.wavfile.read(path)
fft_spectrum = np.fft.rfft(signal)
freq = np.fft.rfftfreq(signal.size, d=1./y)
fft_spectrum_abs = np.abs(fft_spectrum)

data = np.column_stack((freq, np.round(fft_spectrum_abs)))
tmpdf = pd.DataFrame(data, columns=['freq', 'amp'])
tmpdf.loc[:, 'freq'] = np.round(tmpdf['freq'])


df = pd.DataFrame(
        np.array(tmpdf.groupby('freq').max('amp')).reshape(1, -1),
        columns=[str(i) for i in range(0, 11025+1)])

print(df.iloc[0])
