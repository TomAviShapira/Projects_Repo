<<<<<<< HEAD
import os
import pickle
import re
import numpy as np

import umap
import matplotlib.pyplot as plt
import seaborn as sns

path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
       r'מרחביים\FAST-RIR-main\FAST-RIR-main - tom\code_new\Generated_RIRs\traning set\C_code'

c_code_dict = {}
for filename in os.listdir(path):
    with open(path + '\\' + filename, 'rb') as f:
        m = re.search(r'RIR-(\d)_(\d+)', filename)
        speaker_ind = m.group(1)
        rir_ind = m.group(2)
        if rir_ind not in c_code_dict:
            c_code_dict[rir_ind] = {}
        c_code_dict[rir_ind][speaker_ind] = pickle.load(f)

fig = plt.figure(1)
mat = None
for rir_ind_ in ['16', '83', '38', '28', '44']:
    for speaker_ind_ in c_code_dict[rir_ind_]:
        if mat is None:
            mat = c_code_dict[rir_ind_][speaker_ind_].detach().numpy()
        else:
            mat = np.concatenate((mat, c_code_dict[rir_ind_][speaker_ind_].detach().numpy()), axis=0)

map_vec = np.zeros(8).astype(int)
for k in range(1, 5):
    map_vec = np.concatenate((map_vec, k * np.ones(8).astype(int)))

reducer = umap.UMAP()
embedding = reducer.fit_transform(mat)
print(embedding.shape)
plt.scatter(
    embedding[:, 0],
    embedding[:, 1],
    c=map_vec, cmap='Set3', s=20)
plt.gca().set_aspect('equal', 'datalim')
plt.colorbar(boundaries=np.arange(6)-0.5).set_ticks(np.arange(5))
plt.show()
fig.savefig(path + '6.png')


'''
fig = plt.figure(1)
mat = None

for rir_ind_ in ['11', '15', '60', '81', '32', '35', '18', '26', '39', '44']:
    for speaker_ind_ in c_code_dict[rir_ind_]:
        if mat is None:
            mat = c_code_dict[rir_ind_][speaker_ind_].detach().numpy()
        else:
            mat = np.concatenate((mat, c_code_dict[rir_ind_][speaker_ind_].detach().numpy()), axis=0)

# map_vec = np.zeros(32).astype(int)
# map_vec = np.concatenate((map_vec, 1 * np.ones(16).astype(int)))
# map_vec = np.concatenate((map_vec, 2 * np.ones(16).astype(int)))
# map_vec = np.concatenate((map_vec, 3 * np.ones(16).astype(int)))
# map_vec = np.concatenate((map_vec, 4 * np.ones(16).astype(int)))

map_vec = np.zeros(8).astype(int)
for k in range(1, 10):
    map_vec = np.concatenate((map_vec, k * np.ones(8).astype(int)))

reducer = umap.UMAP()
embedding = reducer.fit_transform(mat)
print(embedding.shape)
plt.scatter(
    embedding[:, 0],
    embedding[:, 1],
    c=map_vec, cmap='tab10', s=5)
# plt.gca().set_aspect('equal')
plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
plt.show()
fig.savefig(path + '7.png')
'''
=======
import os
import pickle
import re
import numpy as np

import umap
import matplotlib.pyplot as plt
import seaborn as sns

path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester A\עיבוד וניתוח אותות ' \
       r'מרחביים\FAST-RIR-main\FAST-RIR-main - tom\code_new\Generated_RIRs\traning set\C_code'

c_code_dict = {}
for filename in os.listdir(path):
    with open(path + '\\' + filename, 'rb') as f:
        m = re.search(r'RIR-(\d)_(\d+)', filename)
        speaker_ind = m.group(1)
        rir_ind = m.group(2)
        if rir_ind not in c_code_dict:
            c_code_dict[rir_ind] = {}
        c_code_dict[rir_ind][speaker_ind] = pickle.load(f)

fig = plt.figure(1)
mat = None
for rir_ind_ in ['16', '83', '38', '28', '44']:
    for speaker_ind_ in c_code_dict[rir_ind_]:
        if mat is None:
            mat = c_code_dict[rir_ind_][speaker_ind_].detach().numpy()
        else:
            mat = np.concatenate((mat, c_code_dict[rir_ind_][speaker_ind_].detach().numpy()), axis=0)

map_vec = np.zeros(8).astype(int)
for k in range(1, 5):
    map_vec = np.concatenate((map_vec, k * np.ones(8).astype(int)))

reducer = umap.UMAP()
embedding = reducer.fit_transform(mat)
print(embedding.shape)
plt.scatter(
    embedding[:, 0],
    embedding[:, 1],
    c=map_vec, cmap='Set3', s=20)
plt.gca().set_aspect('equal', 'datalim')
plt.colorbar(boundaries=np.arange(6)-0.5).set_ticks(np.arange(5))
plt.show()
fig.savefig(path + '6.png')


'''
fig = plt.figure(1)
mat = None

for rir_ind_ in ['11', '15', '60', '81', '32', '35', '18', '26', '39', '44']:
    for speaker_ind_ in c_code_dict[rir_ind_]:
        if mat is None:
            mat = c_code_dict[rir_ind_][speaker_ind_].detach().numpy()
        else:
            mat = np.concatenate((mat, c_code_dict[rir_ind_][speaker_ind_].detach().numpy()), axis=0)

# map_vec = np.zeros(32).astype(int)
# map_vec = np.concatenate((map_vec, 1 * np.ones(16).astype(int)))
# map_vec = np.concatenate((map_vec, 2 * np.ones(16).astype(int)))
# map_vec = np.concatenate((map_vec, 3 * np.ones(16).astype(int)))
# map_vec = np.concatenate((map_vec, 4 * np.ones(16).astype(int)))

map_vec = np.zeros(8).astype(int)
for k in range(1, 10):
    map_vec = np.concatenate((map_vec, k * np.ones(8).astype(int)))

reducer = umap.UMAP()
embedding = reducer.fit_transform(mat)
print(embedding.shape)
plt.scatter(
    embedding[:, 0],
    embedding[:, 1],
    c=map_vec, cmap='tab10', s=5)
# plt.gca().set_aspect('equal')
plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
plt.show()
fig.savefig(path + '7.png')
'''
>>>>>>> 0f8de6e6fdc9bfbddd2c211fd16cb0571793da57
