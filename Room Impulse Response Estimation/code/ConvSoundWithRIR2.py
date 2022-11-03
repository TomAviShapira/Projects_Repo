<<<<<<< HEAD
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
from utility import pcm2float, float2pcm
import re

# =============================================================================
IR_path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
          r'מרחביים\FAST-RIR-main\CleanSpeech+RIR\RIRs_for_test_2'
IR_file_name = r'\RIR-0.wav'
IR_file_name2 = re.search(r'(RIR-\d)', IR_file_name).group(1)

sound_path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
             r'מרחביים\FAST-RIR-main\CleanSpeech+RIR\CleanSpeeches_for_test'
sound_file_name = r'\CleanSpeech-0.wav'
sound_file_name2 = re.search(r'(CleanSpeech-\d)', sound_file_name).group(1)

output_path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
              r'מרחביים\FAST-RIR-main\FAST-RIR-main - tom\data\input_wav_files_for_test_2\\'
# =============================================================================

for i in range(3):
    sound_file_name = re.sub(r'\d+', str(i), sound_file_name)
    sound_file_name2 = re.sub(r'\d+', str(i), sound_file_name2)
    input_rate, input_sig = wavfile.read(sound_path + sound_file_name)
    input_sig = pcm2float(input_sig, 'float32')
    for j in range(50):
        IR_file_name = re.sub(r'\d+', str(j), IR_file_name)
        IR_file_name2 = re.sub(r'\d+', str(j), IR_file_name2)
        IR_rate, IR_sig = wavfile.read(IR_path + IR_file_name)
        # IR_sig = pcm2float(IR_sig, 'float32')

        if input_rate != IR_rate:
            print("Size mismatch")
            sys.exit(-1)
        else:
            rate = input_rate
        con_len = -1

        out_0 = fftconvolve(input_sig[:con_len], IR_sig[:con_len])
        out_0 = out_0 / np.max(np.abs(out_0))
        out_0 = out_0[: rate * 3]  # 3 sec
        length = len(out_0)
        crop_length = 48000
        if length < crop_length:
            zeros = np.zeros(crop_length - length)
            out_0 = np.concatenate([out_0, zeros])
        else:
            out_0 = out_0[0:crop_length]
        wavfile.write(output_path + sound_file_name2 + '_' + IR_file_name2 + '.wav', rate, float2pcm(out_0, 'int16'))

        if not len(out_0) == crop_length:
            print("ERROR: out_0 length is" + len(out_0) + ". (should be %d)" % 48000)

print("ConvSoundWithRIR: DOME")
=======
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
from utility import pcm2float, float2pcm
import re

# =============================================================================
IR_path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
          r'מרחביים\FAST-RIR-main\CleanSpeech+RIR\RIRs_for_test_2'
IR_file_name = r'\RIR-0.wav'
IR_file_name2 = re.search(r'(RIR-\d)', IR_file_name).group(1)

sound_path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
             r'מרחביים\FAST-RIR-main\CleanSpeech+RIR\CleanSpeeches_for_test'
sound_file_name = r'\CleanSpeech-0.wav'
sound_file_name2 = re.search(r'(CleanSpeech-\d)', sound_file_name).group(1)

output_path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
              r'מרחביים\FAST-RIR-main\FAST-RIR-main - tom\data\input_wav_files_for_test_2\\'
# =============================================================================

for i in range(3):
    sound_file_name = re.sub(r'\d+', str(i), sound_file_name)
    sound_file_name2 = re.sub(r'\d+', str(i), sound_file_name2)
    input_rate, input_sig = wavfile.read(sound_path + sound_file_name)
    input_sig = pcm2float(input_sig, 'float32')
    for j in range(50):
        IR_file_name = re.sub(r'\d+', str(j), IR_file_name)
        IR_file_name2 = re.sub(r'\d+', str(j), IR_file_name2)
        IR_rate, IR_sig = wavfile.read(IR_path + IR_file_name)
        # IR_sig = pcm2float(IR_sig, 'float32')

        if input_rate != IR_rate:
            print("Size mismatch")
            sys.exit(-1)
        else:
            rate = input_rate
        con_len = -1

        out_0 = fftconvolve(input_sig[:con_len], IR_sig[:con_len])
        out_0 = out_0 / np.max(np.abs(out_0))
        out_0 = out_0[: rate * 3]  # 3 sec
        length = len(out_0)
        crop_length = 48000
        if length < crop_length:
            zeros = np.zeros(crop_length - length)
            out_0 = np.concatenate([out_0, zeros])
        else:
            out_0 = out_0[0:crop_length]
        wavfile.write(output_path + sound_file_name2 + '_' + IR_file_name2 + '.wav', rate, float2pcm(out_0, 'int16'))

        if not len(out_0) == crop_length:
            print("ERROR: out_0 length is" + len(out_0) + ". (should be %d)" % 48000)

print("ConvSoundWithRIR: DOME")
>>>>>>> 0f8de6e6fdc9bfbddd2c211fd16cb0571793da57
