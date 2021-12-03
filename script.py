import pandas as pd
import numpy as np
import tensorflow as tf
import youtube_dl
import librosa
import scipy.io.wavfile
import soundfile as sf
import os
import warnings
import joblib
warnings.filterwarnings("ignore")

# search music from youtube, download it and conert to wav
def download_youtube_audio(link, output_dir):
    ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav'
    }]
   }
    # current_list_of_files = os.listdir(output_dir)
    
    print('Downloading...')
    with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
        info = ydl.extract_info(link, download=True)
        # filename = ydl.prepare_filename(info)
    
    if 'entries' in info:
        info = info['entries'][0]
        
    title = info['title']
    print(f'Downloaded: {title}')
    
    # filename = list(set(os.listdir(output_dir))-set(current_list_of_files))[0]
    filename = ydl.prepare_filename(info).replace('webm', 'wav').replace('m4a', 'wav').replace('mp3', 'wav')
    #return f'{output_dir}/{filename}'
    return filename

# loading amplitude of frequency 0Hz - 11025Hz    
def load_fft_amplitude(path):
    y, signal = scipy.io.wavfile.read(path)
    if signal.ndim == 2 or y != 22050:
        print('Converting to mono / Resampling ...')
        y, sr = librosa.load(path, mono=True, sr=22050)
        sf.write('tmp/tmp.wav', y, sr)
        y, signal = scipy.io.wavfile.read('tmp/tmp.wav')
        os.remove('tmp/tmp.wav')
    
    print('Extracting data...')     
        
    fft_spectrum = np.fft.rfft(signal)
    freq = np.fft.rfftfreq(signal.size, d=1./y)
    fft_spectrum_abs = np.abs(fft_spectrum)
    
    data = np.column_stack((freq, np.round(fft_spectrum_abs)))
    tmpdf = pd.DataFrame(data, columns=['freq', 'amp'])
    tmpdf.loc[:, 'freq'] = np.round(tmpdf['freq'])
    
    df = pd.DataFrame(
                np.array(tmpdf.groupby('freq').max('amp')).reshape(1, -1),
                columns=[str(i) for i in range(0, 11025+1)],
            )
    
    x = np.array(df, dtype=np.float32)
    
    loaded_model = joblib.load(STANDLISER_PATH)
    x = loaded_model.transform(x)
    x = np.reshape(x, (x.shape[0], x.shape[1], 1))
    return x

# predict music genre
def get_prediction(x):
    print('Loading model...')
    interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_detais = interpreter.get_output_details()
    print('Finishing loaded model')
    
    interpreter.set_tensor(input_details[0]['index'], x)
    interpreter.invoke()
    result = interpreter.get_tensor(output_detais[0]['index'])
    return result


if __name__ == '__main__':
    TFLITE_MODEL_PATH = 'model2.tflite'
    STANDLISER_PATH = 'scaler.pkl'
    STORE_DIR = 'tmp'
    
    GENRES = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    
    print("AIST2010 Project - Music Genre Classification")
    print("Wan Yee Ki 1155143499")
    print("In this program, you may either provide a sound file / song name / song url for music genre classification", end="\n\n")
    print("Please choose one of the followings:")
    print("  1. Load .wav file")
    print("  2. Download .wav file from YouTube")
    
    choice_one = input("Your choice: ")
    print("")
    
    if choice_one == "1":
        print(f"Current directory: {os.getcwd()}")
        path = input("Please enter the path of the .wav file: ")
        try:
            x = load_fft_amplitude(path)
        except FileNotFoundError:
            print("**ERROR: File Not Found**")
            exit()
    elif choice_one == "2":
        songname = input("Please enter the name / url of the song: ")
        try:
            filename = download_youtube_audio(songname, STORE_DIR)
        except Exception as err:
            print(f"**ERROR: {err}")
            exit()
        print("")
        x = load_fft_amplitude(filename)
    
    print("")
    pred = get_prediction(x)
    print("")
    
    print(f'{"Music Genre":12}| {"Percentage"}')
    for i in range(10):
        print(f'{GENRES[i]:12}: {np.round(pred[0][i]*100, 3)}%')