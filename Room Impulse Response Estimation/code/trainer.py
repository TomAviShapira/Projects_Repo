from __future__ import print_function

import sys

from six.moves import range
from PIL import Image

import torch.backends.cudnn as cudnn
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
import os
import time
from scipy.stats import pearsonr

import numpy as np
import torchfile
import pickle

import soundfile as sf
import re
import math
from wavefile import WaveWriter, Format

from miscc.config import cfg
from miscc.utils import mkdir_p, send_mail
from miscc.utils import weights_init
from miscc.utils import save_RIR_results, save_model, load_ckp
from miscc.utils import KL_loss
from miscc.utils import compute_discriminator_loss, compute_generator_loss

import RT60
from multiprocessing import Pool

from torch.utils.tensorboard import summary
from torch.utils.tensorboard import FileWriter
from torch.utils.tensorboard import SummaryWriter


class GANTrainer(object):
    def __init__(self, output_dir):
        if cfg.TRAIN.FLAG:
            self.model_dir = os.path.join(output_dir, 'Model')
            self.best_model_dir = os.path.join(output_dir, 'Best_Models')
            self.RIR_dir = os.path.join(output_dir, 'RIR')
            self.log_dir = os.path.join(output_dir, 'Log')
            self.checkpoints_dir = os.path.join(output_dir, 'Checkpoints')
            self.best_checkpoints_dir = os.path.join(output_dir, 'Best_Checkpoints')
            self.c_code_dir = os.path.join(output_dir, 'C_Code')
            self.data_loader_dir = os.path.join(output_dir, 'DataLoader')
            mkdir_p(self.model_dir)
            mkdir_p(self.best_model_dir)
            mkdir_p(self.RIR_dir)
            mkdir_p(self.log_dir)
            mkdir_p(self.checkpoints_dir)
            mkdir_p(self.best_checkpoints_dir)
            mkdir_p(self.c_code_dir)
            mkdir_p(self.data_loader_dir)
            # self.summary_writer = FileWriter(self.log_dir)

        self.max_epoch = cfg.TRAIN.MAX_EPOCH
        self.snapshot_interval = cfg.TRAIN.SNAPSHOT_INTERVAL

        s_gpus = cfg.GPU_ID.split(',')
        self.gpus = [int(ix) for ix in s_gpus]
        self.num_gpus = len(self.gpus)
        self.batch_size = cfg.TRAIN.BATCH_SIZE * self.num_gpus
        if cfg.CUDA:  # tom
            torch.cuda.set_device(self.gpus[0])
        cudnn.benchmark = True  # tom: was uncommented

    # ############# For training stageI GAN #############
    def load_network_stageI(self):
        from model import STAGE1_G, STAGE1_D
        netG = STAGE1_G()
        netG.apply(weights_init)
        print(netG)
        netD = STAGE1_D()
        netD.apply(weights_init)
        print(netD)

        if cfg.NET_G != '':
            state_dict = \
                torch.load(cfg.NET_G,
                           map_location=lambda storage, loc: storage)
            netG.load_state_dict(state_dict)
            print('Load from: ', cfg.NET_G)
        if cfg.NET_D != '':
            state_dict = \
                torch.load(cfg.NET_D,
                           map_location=lambda storage, loc: storage)
            netD.load_state_dict(state_dict)
            print('Load from: ', cfg.NET_D)
        if cfg.CUDA:
            netG.cuda()
            netD.cuda()
        return netG, netD

    # ############# For training stageII GAN  #############
    def load_network_stageII(self):
        from model import STAGE1_G, STAGE2_G, STAGE2_D

        Stage1_G = STAGE1_G()
        netG = STAGE2_G(Stage1_G)
        netG.apply(weights_init)
        print(netG)
        if cfg.NET_G != '':
            state_dict = \
                torch.load(cfg.NET_G,
                           map_location=lambda storage, loc: storage)
            netG.load_state_dict(state_dict)
            print('Load from: ', cfg.NET_G)
        elif cfg.STAGE1_G != '':
            state_dict = \
                torch.load(cfg.STAGE1_G,
                           map_location=lambda storage, loc: storage)
            netG.STAGE1_G.load_state_dict(state_dict)
            print('Load from: ', cfg.STAGE1_G)
        else:
            print("Please give the Stage1_G path")
            return

        netD = STAGE2_D()
        netD.apply(weights_init)
        if cfg.NET_D != '':
            state_dict = \
                torch.load(cfg.NET_D,
                           map_location=lambda storage, loc: storage)
            netD.load_state_dict(state_dict)
            print('Load from: ', cfg.NET_D)
        print(netD)

        if cfg.CUDA:
            netG.cuda()
            netD.cuda()
        return netG, netD

    def train(self, data_loader, stage=1):
        # writer = SummaryWriter()

        if data_loader is None:
            data_loader_path = cfg.TRAIN.DATA_LOADER_PATH
            data_loader = torch.load(data_loader_path)
            print('Load data_loader of %d inputs from: %s' % (len(data_loader) * self.batch_size, data_loader_path))
        else:
            torch.save(data_loader, self.data_loader_dir + '\\DataLoader.pth')

        if stage == 1:
            netG, netD = self.load_network_stageI()
        else:
            netG, netD = self.load_network_stageII()

        # nz = cfg.Z_DIM
        batch_size = self.batch_size
        # noise = Variable(torch.FloatTensor(batch_size, nz))
        # fixed_noise = \
        #     Variable(torch.FloatTensor(batch_size, nz).normal_(0, 1),
        #              volatile=True)
        real_labels = Variable(torch.FloatTensor(batch_size).fill_(1))
        fake_labels = Variable(torch.FloatTensor(batch_size).fill_(0))
        if cfg.CUDA:
            # noise, fixed_noise = noise.cuda(), fixed_noise.cuda()
            real_labels, fake_labels = real_labels.cuda(), fake_labels.cuda()

        # min_lr = cfg.TRAIN.MIN_LR
        # max_lr = cfg.TRAIN.MAX_LR
        lr_decay_step = cfg.TRAIN.LR_DECAY_EPOCH

        # optimizerD = \
        #     optim.Adam(netD.parameters(),
        #                lr=cfg.TRAIN.DISCRIMINATOR_LR, betas=(0.5, 0.999))
        optimizerD = \
            optim.RMSprop(netD.parameters(),
                          lr=cfg.TRAIN.MAX_LR)
        discriminator_lr = cfg.TRAIN.MAX_LR
        netG_para = []
        for p in netG.parameters():
            if p.requires_grad:
                netG_para.append(p)
        # optimizerG = optim.Adam(netG_para,
        #                         lr=cfg.TRAIN.GENERATOR_LR,
        #                         betas=(0.5, 0.999))
        optimizerG = optim.RMSprop(netG_para,
                                   lr=cfg.TRAIN.MAX_LR)
        generator_lr = cfg.TRAIN.MAX_LR
        # count = 0
        # least_RT = 10

        min_errG = 100000

        if cfg.TRAIN.LOAD_CKP:
            ckp_path = cfg.TRAIN.CKP_FILE_PATH
            netG, optimizerG, netD, optimizerD, last_epoch, epoch_cnt, reset_lr_val = \
                load_ckp(ckp_path, netG, optimizerG, netD, optimizerD)  # reset_lr_val is measured in epochs
            start_epoch = last_epoch + 1

            for param_group in optimizerG.param_groups:
                generator_lr = param_group['lr']
            for param_group in optimizerD.param_groups:
                discriminator_lr = param_group['lr']

            print('Load model from: %s\n' % ckp_path)
        else:
            start_epoch = 0
            reset_lr_val = -1  # measured in epochs
            epoch_cnt = -1

        for epoch in range(start_epoch, self.max_epoch):

            epoch_errD, epoch_errG, epoch_errD_real, epoch_errD_wrong, epoch_errD_fake, epoch_MSE_error, Epoch_RT_error \
                = [0, 0, 0, 0, 0, 0, 0]

            '''
            if epoch_cnt == reset_lr_val:
                epoch_cnt = 0
            else:
                epoch_cnt += 1
            '''

            epoch_start_t = time.time()

            # '''
            if epoch % lr_decay_step == 0 and epoch > 0:
                generator_lr *= 0.7
                for param_group in optimizerG.param_groups:
                    param_group['lr'] = generator_lr
                discriminator_lr *= 0.7
                for param_group in optimizerD.param_groups:
                    param_group['lr'] = discriminator_lr
            # '''

            '''
            generator_lr = min_lr + 0.5 * (max_lr - min_lr) * (1 + math.cos((epoch_cnt / reset_lr_val) * math.pi))
            discriminator_lr = min_lr + 0.5 * (max_lr - min_lr) * (1 + math.cos((epoch_cnt / reset_lr_val) * math.pi))
            for param_group in optimizerG.param_groups:
                param_group['lr'] = generator_lr
            for param_group in optimizerD.param_groups:
                param_group['lr'] = discriminator_lr
            '''

            i = 0
            for i, data in enumerate(data_loader, 0):
                batch_start_t = time.time()
                ######################################################
                # (1) Prepare training data
                ######################################################
                real_RIR_cpu, inputWAV = data
                real_RIRs = Variable(real_RIR_cpu)
                inputWAV = torch.unsqueeze(inputWAV, 1)
                inputWAV = Variable(inputWAV)
                if cfg.CUDA:
                    real_RIRs = real_RIRs.cuda()
                    inputWAV = inputWAV.cuda()
                # print("trianer RIRs ",real_RIRs.size())
                # print("trianer embedding ",inputWAV.size())

                #######################################################
                # (2) Generate fake images
                ######################################################
                # noise.data.normal_(0, 1)
                # inputs = (inputWAV, noise)
                inputs = (inputWAV)
                # _, fake_RIRs, mu, logvar = \
                #     nn.parallel.data_parallel(netG, inputs, self.gpus)
                if cfg.CUDA:
                    _, fake_RIRs, c_code = nn.parallel.data_parallel(netG, inputs, self.gpus)
                else:
                    _, fake_RIRs, c_code = \
                        netG(inputs)

                ############################
                # (3) Update D network
                ###########################
                netD.zero_grad()
                errD, errD_real, errD_wrong, errD_fake = \
                    compute_discriminator_loss(netD, real_RIRs, fake_RIRs,
                                               real_labels, fake_labels,

                                               c_code, self.gpus)

                errD_total = errD * 5
                errD_total.backward()
                optimizerD.step()
                ############################
                # (2) Update G network
                ###########################
                # kl_loss = KL_loss(mu, logvar)
                netG.zero_grad()
                errG, MSE_error, RT_error = compute_generator_loss(epoch, netD, real_RIRs, fake_RIRs,
                                                                   real_labels, c_code, self.gpus)
                errG_total = errG * 5  # + kl_loss * cfg.TRAIN.COEFF.KL
                errG_total.backward()
                optimizerG.step()
                for p in range(2):
                    inputs = (inputWAV)
                    # _, fake_RIRs, mu, logvar = \
                    #     nn.parallel.data_parallel(netG, inputs, self.gpus)
                    if cfg.CUDA:
                        _, fake_RIRs, c_code = nn.parallel.data_parallel(netG, inputs, self.gpus)
                    else:
                        _, fake_RIRs, c_code = \
                            netG(inputs)
                    netG.zero_grad()
                    errG, MSE_error, RT_error = compute_generator_loss(epoch, netD, real_RIRs, fake_RIRs,
                                                                       real_labels, c_code, self.gpus)
                    # kl_loss = KL_loss(mu, logvar)
                    errG_total = errG * 5  # + kl_loss * cfg.TRAIN.COEFF.KL
                    errG_total.backward()
                    optimizerG.step()

                # count = count + 1
                # if i % 100 == 0:
                # summary_D = summary.scalar('D_loss', errD.data[0])
                # summary_D_r = summary.scalar('D_loss_real', errD_real)
                # summary_D_w = summary.scalar('D_loss_wrong', errD_wrong)
                # summary_D_f = summary.scalar('D_loss_fake', errD_fake)
                # summary_G = summary.scalar('G_loss', errG.data[0])
                # summary_KL = summary.scalar('KL_loss', kl_loss.data[0])
                # summary_D = summary.scalar('D_loss', errD.data)
                # summary_D_r = summary.scalar('D_loss_real', errD_real)
                # summary_D_w = summary.scalar('D_loss_wrong', errD_wrong)
                # summary_D_f = summary.scalar('D_loss_fake', errD_fake)
                # summary_G = summary.scalar('G_loss', errG.data)
                # summary_KL = summary.scalar('KL_loss', kl_loss.data)

                # self.summary_writer.add_summary(summary_D, count)
                # self.summary_writer.add_summary(summary_D_r, count)
                # self.summary_writer.add_summary(summary_D_w, count)
                # self.summary_writer.add_summary(summary_D_f, count)
                # self.summary_writer.add_summary(summary_G, count)
                # self.summary_writer.add_summary(summary_KL, count)

                # writer.add_scalar('D_loss', errD.data, count)
                # writer.add_scalar('D_loss_real', errD_real, count)
                # writer.add_scalar('D_loss_wrong', errD_wrong, count)
                # writer.add_scalar('D_loss_fake', errD_fake, count)
                # writer.add_scalar('G_loss', errG.data, count)

                if i % 5 == 0 or i == len(data_loader) - 1:
                    inputs = (inputWAV)

                    if cfg.CUDA:
                        lr_fake, fake, _ = \
                            nn.parallel.data_parallel(netG, inputs, self.gpus)
                    else:
                        lr_fake, fake, _ = \
                            netG(inputs)

                    save_RIR_results(real_RIR_cpu, fake, epoch, self.RIR_dir)
                    if lr_fake is not None:
                        save_RIR_results(None, lr_fake, epoch, self.RIR_dir)

                    with open(self.c_code_dir + '\\Epoch%d_Batch%d.txt' % (epoch, i), 'wb') as f:
                        pickle.dump(c_code, f)

                batch_end_t = time.time()
                epoch_errD += errD.data
                epoch_errG += errG.data
                epoch_errD_real += errD_real
                epoch_errD_wrong += errD_wrong
                epoch_errD_fake += errD_fake
                epoch_MSE_error += MSE_error
                Epoch_RT_error += RT_error

                batch_log = '[%d/%d][%d/%d] Loss_D: %.4f , Loss_G: %.4f\n' \
                            'Loss_real: %.4f , Loss_wrong: %.4f , Loss_fake: %.4f  ,  MSE_ERROR: %.4f ,' \
                            ' RT_error: %.4f\n' \
                            'Batch_Time: %.2f sec\n' \
                            % (epoch, self.max_epoch - 1, i, len(data_loader) - 1,
                               errD.data, errG.data,
                               errD_real, errD_wrong, errD_fake, MSE_error * 4096, RT_error,
                               (batch_end_t - batch_start_t))
                batch_log += 'lr:   generator_lr = ' + str(generator_lr) + ' , discriminator_lr = ' + \
                             str(discriminator_lr) + '\n'
                batch_log += 'epoch_cnt = ' + str(epoch_cnt) + ' , reset_lr_val = ' + \
                             str(reset_lr_val) + '\n\n'
                sys.stdout.write(batch_log)
                with open(self.log_dir + '\\log.txt', 'a') as log_file:
                    log_file.write(batch_log)

                '''
                # learning rate test
                # ===================================================================================
                generator_lr *= 10 ** 0.1  # 0.5
                for param_group in optimizerG.param_groups:
                    param_group['lr'] = generator_lr
                discriminator_lr *= 10 ** 0.1  # 0.5
                for param_group in optimizerD.param_groups:
                    param_group['lr'] = discriminator_lr
                # ===================================================================================
                '''

            epoch_end_t = time.time()
            # print('''[%d/%d][%d/%d] Loss_D: %.4f Loss_G: %.4f Loss_KL: %.4f
            #          Loss_real: %.4f Loss_wrong:%.4f Loss_fake %.4f
            #          Total Time: %.2fsec
            #       '''
            #       % (epoch, self.max_epoch, i, len(data_loader),
            #          errD.data[0], errG.data[0], kl_loss.data[0],
            #          errD_real, errD_wrong, errD_fake, (end_t - start_t)))
            # print('''[%d/%d][%d/%d] Loss_D: %.4f Loss_G: %.4f Loss_KL: %.4f
            #          Loss_real: %.4f Loss_wrong:%.4f Loss_fake %.4f
            #          Total Time: %.2fsec
            #       '''
            #       % (epoch, self.max_epoch, i, len(data_loader),
            #          errD.data, errG.data, kl_loss.data,
            #          errD_real, errD_wrong, errD_fake, (end_t - start_t)))

            epoch_errD /= len(data_loader)
            epoch_errG /= len(data_loader)
            epoch_errD_real /= len(data_loader)
            epoch_errD_wrong /= len(data_loader)
            epoch_errD_fake /= len(data_loader)
            epoch_MSE_error /= len(data_loader)
            Epoch_RT_error /= len(data_loader)

            epoch_log = '=================================== EPOCH SUMMARY ===================================\n' \
                        '[%d/%d][%d/%d] Epoch_Loss_D: %.4f Epoch_Loss_G: %.4f\n' \
                        'Epoch_Loss_real: %.4f , Epoch_Loss_wrong: %.4f , Epoch_Loss_fake: %.4f  ,  ' \
                        'Epoch_MSE_ERROR: %.4f , Epoch_RT_error: %.4f\n' \
                        'Total_Epoch_Time: %.2f sec\n' \
                        'last lr:   generator_lr = %s , discriminator_lr = %s\n' \
                        'epoch_cnt = %d , reset_lr_val = %d\n' \
                        '=====================================================================================\n\n' \
                        % (epoch, self.max_epoch - 1, i, len(data_loader) - 1,
                           epoch_errD, epoch_errG,
                           epoch_errD_real, epoch_errD_wrong, epoch_errD_fake, epoch_MSE_error * 4096,
                           Epoch_RT_error,
                           (epoch_end_t - epoch_start_t),
                           str(generator_lr), str(discriminator_lr),
                           epoch_cnt, reset_lr_val)
            sys.stdout.write(epoch_log)

            with open(self.log_dir + '\\log.txt', 'a') as log_file:
                log_file.write(epoch_log)

            '''
            if RT_error < least_RT:
                least_RT = RT_error
                save_model(netG, netD, epoch, self.model_dir_RT)
            '''
            is_best = False
            if epoch_errG < min_errG:
                min_errG = epoch_errG
                is_best = True

            is_save_model = False
            if epoch % self.snapshot_interval == 0:
                is_save_model = True

            if is_save_model or is_best:
                save_model(netG, optimizerG, netD, optimizerD, epoch, is_save_model, is_best, self.model_dir,
                           self.best_model_dir, self.checkpoints_dir, self.best_checkpoints_dir,
                           epoch_cnt, reset_lr_val)

            # send email
            try:
                send_mail('Epoch%d Summary' % epoch, epoch_log)
            except:
                print('mail is not sent\n\n')
            #

        #
        save_model(netG, optimizerG, netD, optimizerD, epoch, True, is_best, self.model_dir,
                   self.best_model_dir, self.checkpoints_dir, self.best_checkpoints_dir,
                   epoch_cnt, reset_lr_val)
        #
        # self.summary_writer.close()

    def sample(self, file_path, stage=1):
        if stage == 1:
            netG, _ = self.load_network_stageI()
        else:
            netG, _ = self.load_network_stageII()
        netG.eval()

        time_list = []

        embedding_path = file_path
        with open(embedding_path, 'rb') as f:
            embeddings_pickle = pickle.load(f)

        embeddings_list = []
        num_embeddings = len(embeddings_pickle)
        for b in range(num_embeddings):
            embeddings_list.append(embeddings_pickle[b])

        embeddings = np.array(embeddings_list)

        save_dir_GAN = "Generated_RIRs"
        mkdir_p(save_dir_GAN)

        normalize_embedding = []

        batch_size = np.minimum(num_embeddings, self.batch_size)

        count = 0
        count_this = 0
        while count < num_embeddings:

            iend = count + batch_size
            if iend > num_embeddings:
                iend = num_embeddings
                count = num_embeddings - batch_size
            embeddings_batch = embeddings[count:iend]

            txt_embedding = Variable(torch.FloatTensor(embeddings_batch))
            if cfg.CUDA:
                txt_embedding = txt_embedding.cuda()

            #######################################################
            # (2) Generate fake images
            ######################################################
            start_t = time.time()
            inputs = (txt_embedding)

            if cfg.CUDA:  # tom
                _, fake_RIRs, c_code = \
                    nn.parallel.data_parallel(netG, inputs, self.gpus)
            else:  # tom
                _, fake_RIRs, c_code = \
                    netG(inputs)

            end_t = time.time()
            diff_t = end_t - start_t
            time_list.append(diff_t)

            RIR_batch_size = batch_size  # int(batch_size/2)
            print("batch_size ", RIR_batch_size)
            # channel_size = 64
            channel_size = np.minimum(64, fake_RIRs.size()[0])

            for i in range(channel_size):
                fs = 16000
                wave_name = "RIR-" + str(count + i) + ".wav"
                save_name_GAN = '%s/%s' % (save_dir_GAN, wave_name)
                print("wave : ", save_name_GAN)
                res = {}
                res_buffer = []
                rate = 16000
                res['rate'] = rate

                wave_GAN = fake_RIRs[i].data.cpu().numpy()
                wave_GAN = np.array(wave_GAN[0])

                res_buffer.append(wave_GAN)
                res['samples'] = np.zeros((len(res_buffer), np.max([len(ps) for ps in res_buffer])))
                for k, c in enumerate(res_buffer):
                    res['samples'][k, :len(c)] = c

                w = WaveWriter(save_name_GAN, channels=np.shape(res['samples'])[0], samplerate=int(res['rate']))
                w.write(np.array(res['samples']))

            print("counter = ", count)
            count = count + channel_size
            count_this = count_this + 1

        print("Num of generated RIR: ", len(time_list))
        print("Avg time: ", sum(time_list) / len(time_list))
        print("Total time: ", sum(time_list))

    def tom_sample(self, data_loader, stage=1):

        save_dir_GAN = "Generated_RIRs"
        mkdir_p(save_dir_GAN)

        if stage == 1:
            netG, _ = self.load_network_stageI()
        else:
            netG, _ = self.load_network_stageII()
        netG.eval()

        RIR_cnt = 11
        speech_cnt = 0
        time_list = []

        for i, data in enumerate(data_loader, 0):
            ######################################################
            # (1) Prepare training data
            ######################################################
            real_RIR_cpu, inputWAV = data
            real_RIRs = Variable(real_RIR_cpu)
            inputWAV = torch.unsqueeze(inputWAV, 1)
            inputWAV = Variable(inputWAV)
            if cfg.CUDA:
                real_RIRs = real_RIRs.cuda()
                inputWAV = inputWAV.cuda()
            # print("trianer RIRs ",real_RIRs.size())
            # print("trianer embedding ",txt_embedding.size())

            #######################################################
            # (2) Generate fake images
            ######################################################
            start_t = time.time()
            # noise.data.normal_(0, 1)
            # inputs = (txt_embedding, noise)
            inputs = (inputWAV)
            # _, fake_RIRs, mu, logvar = \
            #     nn.parallel.data_parallel(netG, inputs, self.gpus)
            if cfg.CUDA:
                _, fake_RIRs, c_code = nn.parallel.data_parallel(netG, inputs, self.gpus)
            else:
                _, fake_RIRs, c_code = \
                    netG(inputs)
            end_t = time.time()
            diff_t = end_t - start_t
            time_list.append(diff_t)

            batch_size = self.batch_size
            print("batch_size ", batch_size)

            for j in range(batch_size):
                fs = 16000
                if RIR_cnt == 84:
                    RIR_cnt = 11
                    speech_cnt += 1
                wave_name = "RIR-" + str(speech_cnt) + '_' + str(RIR_cnt) + ".wav"
                pickle_name = "RIR-" + str(speech_cnt) + '_' + str(RIR_cnt) + ".txt"
                RIR_cnt += 1
                save_name_GAN = '%s/%s' % (save_dir_GAN, wave_name)
                save_name_pickle = '%s/C_code/%s' % (save_dir_GAN, pickle_name)
                print("wave : ", save_name_GAN)
                res = {}
                res_buffer = []
                rate = 16000
                res['rate'] = rate

                wave_GAN = fake_RIRs[j].data.cpu().numpy()
                wave_GAN = np.array(wave_GAN[0])

                res_buffer.append(wave_GAN)
                res['samples'] = np.zeros((len(res_buffer), np.max([len(ps) for ps in res_buffer])))
                for k, c in enumerate(res_buffer):
                    res['samples'][k, :len(c)] = c

                w = WaveWriter(save_name_GAN, channels=np.shape(res['samples'])[0], samplerate=int(res['rate']))
                w.write(np.array(res['samples']))

                with open(save_name_pickle, 'wb') as f:
                    pickle.dump(c_code, f)

            MSE_loss = nn.MSELoss()
            MSE_error = MSE_loss(real_RIRs, fake_RIRs)

            # RT_ERROR
            channel = 1
            fs = 16000
            real_wave = np.array(real_RIRs.to("cpu").detach())
            real_wave = real_wave.reshape(channel, 4096)
            fake_wave = np.array(fake_RIRs.to("cpu").detach())
            fake_wave = fake_wave.reshape(channel, 4096)

            results = []
            for n in range(channel):
                results.append(RT60.t60_parallel(n, real_wave, fake_wave, fs))

            T60_error = 0
            for result in results:
                T60_error = T60_error + result

            RT_error = T60_error / channel

            # Pearson correlation
            Pearson, _ = pearsonr(real_wave[0], fake_wave[0])

            print("MSE_ERROR: %.4f      RT_ERROR: %.4f      Pearson: %.4f       Avg_Time: %.4f\n" \
                  % (MSE_error * 4096, RT_error, Pearson, sum(time_list) / len(time_list)))

    def RT_calc(self, RIRs_path):
        for RIR_ in os.listdir(RIRs_path):
            wav, fs = sf.read(RIRs_path + '\\' + RIR_)
            fs = 16000
            RT = RT60.t60_impulse(wav, fs)
            print('%s RT: %s' % (str(RIR_), str(RT)))
