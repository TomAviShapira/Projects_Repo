<<<<<<< HEAD
import matplotlib.pyplot as plt
from scipy.io import wavfile
from utility import pcm2float
import numpy as np

IR_file_name = 'RIR-net50_2.wav'
title = IR_file_name.split('.')[0]
IR_path = '..\\output\\RIRs\\' + title + '\\'

# =============================================================================
con_len = -1
IR_rate, IR_sig = wavfile.read(IR_path + IR_file_name)
IR_sig = pcm2float(IR_sig, 'float32')

fig = plt.figure(1)
plt.title(title + '     STFT Magnitude')
plt.specgram(IR_sig[:con_len, 0] / np.max(np.abs(IR_sig[:con_len, 0])), Fs=IR_rate)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar()
plt.show()
fig.savefig(IR_path + title + '-stft.png')
=======
import matplotlib.pyplot as plt
from scipy.io import wavfile
from utility import pcm2float
import numpy as np

IR_file_name = 'RIR-net50_2.wav'
title = IR_file_name.split('.')[0]
IR_path = '..\\output\\RIRs\\' + title + '\\'

# =============================================================================
con_len = -1
IR_rate, IR_sig = wavfile.read(IR_path + IR_file_name)
IR_sig = pcm2float(IR_sig, 'float32')

fig = plt.figure(1)
plt.title(title + '     STFT Magnitude')
plt.specgram(IR_sig[:con_len, 0] / np.max(np.abs(IR_sig[:con_len, 0])), Fs=IR_rate)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar()
plt.show()
fig.savefig(IR_path + title + '-stft.png')
>>>>>>> 0f8de6e6fdc9bfbddd2c211fd16cb0571793da57
