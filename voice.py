import array
import numpy as np
import pyaudio
import wave
from Python_Extension import *

rate = 16000
record_seconds = 1.024
chunk = 1024

NN = Neural_Networks("model.txt")
SP = Speech_Processing()
SP.Load_Parameter("param.txt")


if __name__ == "__main__":
    while (True):
        buffer = []
        frame = []
        
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=rate,
                            input_device_index=2,
                            frames_per_buffer=chunk,
                            input=True)

        for i in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            buffer.append(data)

            if i == 0:
                frame = np.fromstring(data, dtype=np.int16)
            else:
                frame = np.append(frame, np.fromstring(data, dtype=np.int16))

        stream.stop_stream()
        stream.close()
        audio.terminate()

        frame = np.array(frame / 32768, dtype=np.float32)
        MFCC = SP.Calculate_MFCC(frame, frame.shape[0], 400, 160, 13, 26, rate)

        output = np.zeros(100, dtype=np.float32)
        NN.Test(MFCC, output, int(MFCC.shape[0] / (3 * 13)))
        print(0.5 * (output[0] + output[output.shape[0] - 1]))

'''
wav = wave.open("file.wav", 'wb')
wav.setnchannels(1)
wav.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wav.setframerate(rate)
wav.writeframes(b''.join(buffer))
wav.close()
'''
