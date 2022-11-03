from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import torch.utils.data as data
# from PIL import Image
import soundfile as sf
import PIL
import os
import os.path
import pickle
import random
import numpy as np
import re
import pandas as pd
from scipy import signal
from scipy.io import wavfile
from utility import pcm2float, float2pcm

from miscc.config import cfg


class TextDataset(data.Dataset):
    def __init__(self, data_dir, rirsize=4096):  # , transform=None, target_transform=None):

        # self.transform = transformeasydict
        # self.target_transform = target_transform
        self.rirsize = rirsize
        self.data = []
        self.data_dir = data_dir
        self.bbox = None

        split_dir = os.path.join(data_dir)

        self.filenames = self.load_filenames(split_dir)
        self.inputWAV = self.load_inputWAVs(split_dir)

    def get_RIR(self, RIR_path):
        wav, fs = sf.read(RIR_path)  # Image.open(RIR_path).convert('RGB')
        length = wav.size
        # crop_length = int((16384*(80))/(64))
        crop_length = 4096  # int(16384)
        if length < crop_length:
            zeros = np.zeros(crop_length - length)
            RIR_original = np.concatenate([wav, zeros])
        else:
            RIR_original = wav[0:crop_length]

        # resample_length = int((self.rirsize*(80))/(64))
        resample_length = int(self.rirsize)
        if resample_length == 16384:
            RIR = RIR_original
        else:
            RIR = RIR_original  # signal.resample(RIR_original,resample_length)
        RIR = np.array([RIR]).astype('float32')

        # if bbox is not None:
        #     R = int(np.maximum(bbox[2], bbox[3]) * 0.75)
        #     center_x = int((2 * bbox[0] + bbox[2]) / 2)
        #     center_y = int((2 * bbox[1] + bbox[3]) / 2)
        #     y1 = np.maximum(0, center_y - R)
        #     y2 = np.minimum(height, center_y + R)
        #     x1 = np.maximum(0, center_x - R)
        #     x2 = np.minimum(width, center_x + R)
        #     RIR = RIR.crop([x1, y1, x2, y2])
        # load_size = int(self.rirsize * 76 / 64)
        # RIR = RIR.resize((load_size, load_size), PIL.Image.BILINEAR)
        # if self.transform is not None:
        #     RIR = self.transform(RIR)
        # print(length, '=>', len(RIR_original))
        return RIR

    def load_inputWAVs(self, data_dir):
        input_dict = {}
        for wav_name in self.filenames:
            tmp = os.path.join(data_dir, 'input_wav_files_cropped')
            tmp = os.path.join(tmp, wav_name + '.wav')
            input_rate, input_sig = wavfile.read(tmp)
            input_sig = pcm2float(input_sig, 'float32')

            input_dict[wav_name] = input_sig

        return input_dict

    # def load_class_id(self, data_dir, total_num):
    #     if os.path.isfile(data_dir + '/class_info.pickle'):
    #         with open(data_dir + '/class_info.pickle', 'rb') as f:
    #             class_id = pickle.load(f)
    #     else:
    #         class_id = np.arange(total_num)
    #     return class_id

    def load_filenames(self, data_dir):
        filepath = os.path.join(data_dir, 'filenames_batch8.txt')
        filenames = []
        with open(filepath, 'r') as f:
            for line in f:
                line = re.sub(r'\s+', "", line)
                if line is not '':
                    filenames.append(line)

        print('Load dataset of %d inputs from: %s' % (len(filenames), filepath))
        return filenames

    def __getitem__(self, index):
        key = self.filenames[index]
        RIR_name_from_key = re.search(r'(RIR-\d+)', key).group(1)

        data_dir = self.data_dir

        # captions = self.captions[key]
        inputWAVs = self.inputWAV[key]
        RIR_name = '%sRIRs_cropped/%s.wav' % (data_dir, RIR_name_from_key)
        RIR = self.get_RIR(RIR_name)  # [:, :, 0]  # take mono channel RIR
        inputWAV = np.array(inputWAVs).astype('float32')
        # if self.target_transform is not None:
        #     embedding = self.target_transform(embedding)
        return RIR, inputWAV

    def __len__(self):
        return len(self.filenames)
