<<<<<<< HEAD
import os
from scipy.io import wavfile
from utility import pcm2float, float2pcm
import numpy as np

# %%
path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות מרחביים' \
       r'\FAST-RIR-main\CleanSpeech+RIR\RIRs_for_test'
'''
i = 0
for filename in os.listdir(path):
    os.rename(path + '\\' + filename, 'RIR-%d.wav' % i)
    i += 1
'''

for i in range(3):
    for j in range(50):
        print('CleanSpeech-%d_RIR-%d' % (i, j))


# %%
path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
       r'מרחביים\FAST-RIR-main\FAST-RIR-main - tom\data\RIRs'
output_path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
              r'מרחביים\FAST-RIR-main\FAST-RIR-main - tom\data\RIRs_cropped'

cnt = 11
for file in os.listdir(path):
    input_rate, input_sig = wavfile.read(path + '\\' + file)
    input_sig = pcm2float(input_sig, 'float32')
    input_sig = input_sig[:, 0]
    length = len(input_sig)
    if 15000 < length < 25000:
        RIR_original = input_sig[0:length:2]
        RIR_original = RIR_original[0:4096]
    elif length > 25000:
        RIR_original = input_sig[0:length:3]
        RIR_original = RIR_original[0:4096]
    else:
        RIR_original = input_sig[0:4096]
    print(cnt, length, '=>', len(RIR_original))
    cnt += 1

    wavfile.write(output_path + '\\' + file, input_rate, float2pcm(RIR_original, 'int16'))


cnt = 11
for file in os.listdir(output_path):
    input_rate, input_sig = wavfile.read(output_path + '\\' + file)
    input_sig = pcm2float(input_sig, 'float32')
    print(cnt, len(input_sig))
    cnt += 1
=======
import os
from scipy.io import wavfile
from utility import pcm2float, float2pcm
import numpy as np

# %%
path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות מרחביים' \
       r'\FAST-RIR-main\CleanSpeech+RIR\RIRs_for_test'
'''
i = 0
for filename in os.listdir(path):
    os.rename(path + '\\' + filename, 'RIR-%d.wav' % i)
    i += 1
'''

for i in range(3):
    for j in range(50):
        print('CleanSpeech-%d_RIR-%d' % (i, j))


# %%
path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
       r'מרחביים\FAST-RIR-main\FAST-RIR-main - tom\data\RIRs'
output_path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
              r'מרחביים\FAST-RIR-main\FAST-RIR-main - tom\data\RIRs_cropped'

cnt = 11
for file in os.listdir(path):
    input_rate, input_sig = wavfile.read(path + '\\' + file)
    input_sig = pcm2float(input_sig, 'float32')
    input_sig = input_sig[:, 0]
    length = len(input_sig)
    if 15000 < length < 25000:
        RIR_original = input_sig[0:length:2]
        RIR_original = RIR_original[0:4096]
    elif length > 25000:
        RIR_original = input_sig[0:length:3]
        RIR_original = RIR_original[0:4096]
    else:
        RIR_original = input_sig[0:4096]
    print(cnt, length, '=>', len(RIR_original))
    cnt += 1

    wavfile.write(output_path + '\\' + file, input_rate, float2pcm(RIR_original, 'int16'))


cnt = 11
for file in os.listdir(output_path):
    input_rate, input_sig = wavfile.read(output_path + '\\' + file)
    input_sig = pcm2float(input_sig, 'float32')
    print(cnt, len(input_sig))
    cnt += 1
>>>>>>> 0f8de6e6fdc9bfbddd2c211fd16cb0571793da57
