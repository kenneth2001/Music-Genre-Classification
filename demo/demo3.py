import pandas as pd
import numpy as np
import librosa

path = input("Please enter the path of the audio file:")
print("")

df = pd.DataFrame(columns=['chroma_stft_mean',
                            'chroma_stft_var',
                            'rms_mean',
                            'rms_var',
                            'spectral_centroid_mean',
                            'spectral_centroid_var',
                            'spectral_bandwidth_mean',
                            'spectral_bandwidth_var',
                            'rolloff_mean',
                            'rolloff_var',
                            'zero_crossing_rate_mean',
                            'zero_crossing_rate_var',
                            'tempo'] + [f"mfcc{i}" for i in range(1, 21)], index=None)

y, sr = librosa.load(path)
mfcc = librosa.feature.mfcc(y, sr)
data = [[np.mean(librosa.feature.chroma_stft(y, sr)),
        np.var(librosa.feature.chroma_stft(y, sr)),
        np.mean(librosa.feature.rms(y)),
        np.var(librosa.feature.rms(y)),
        np.mean(librosa.feature.spectral_centroid(y, sr)),
        np.var(librosa.feature.spectral_centroid(y, sr)),
        np.mean(librosa.feature.spectral_bandwidth(y, sr)),
        np.var(librosa.feature.spectral_bandwidth(y, sr)),
        np.mean(librosa.feature.spectral_rolloff(y, sr)),
        np.var(librosa.feature.spectral_rolloff(y, sr)),
        np.mean(librosa.feature.zero_crossing_rate(y)),
        np.var(librosa.feature.zero_crossing_rate(y)),
        librosa.beat.tempo(y)[0]] + [np.mean(mfcc[i]) for i in range(20)]]

tmpdf = pd.DataFrame(data, columns=df.columns)

print(tmpdf.iloc[0])
