<div  align="center">

# ROOM IMPULSE RESPONSE ESTIMATIOM FROM REVERBERANT SPEECH USING GAN

</div>

## Abstract

Room impulse response (RIR) estimation is a fascinating problem that has a lot of applications.
Augmented and virtual reality, automatic speech recognition (ASR) and dereverberation audio
processing are some of them. In this paper we present a method for RIR estimation from a reverberant
speech audio file, using a neural network. The network archi-tecture is based on FASR-RIR architecture,
which generates RIR from an embedded vector that represents room pa-rameters as an input.
To estimate RIR of a real room, in this paper we suggest a modification to the FAST-RIR architecture
which allows to use audio file as an input. Namely the network was designed to generate new RIR that
estimates the ground-truth RIR of the room where the input audio file was recorded in.
We have shown that our model succeeds to extract a target room’s features from a reverberant speech
and then estimate RIRs well enough for a proof of concept.

## Our work and code are based on

```
@article{ratnarajah2021fast,
  title={FAST-RIR: Fast neural diffuse room impulse response generator},
  author={Ratnarajah, Anton and Zhang, Shi-Xiong and Yu, Meng and Tang, Zhenyu and Manocha, Dinesh and Yu, Dong},
  journal={arXiv preprint arXiv:2110.04057},
  year={2021}
}
```

```
@inproceedings{steinmetz2021wavebeat,
    title={{WaveBeat}: End-to-end beat and downbeat tracking in the time domain},
    author={Steinmetz, Christian J. and Reiss, Joshua D.},
    booktitle={151st AES Convention},
    year={2021}}
```

## Datasets

```
Vassil Panayotov, Guoguo Chen, Daniel Povey, and San-jeev Khudanpur, “Librispeech: An ASR corpus based on public domain audio books,” in ICASSP. 2015, pp. 5206–5210, IEEE.
```

```
https://www.iks.rwth aachen.de/en/research/tools
downloads/databases/aachen impulse response
database/
```

## About

This work was written as part of M.Sc. studies in electrical engineering at the
Technion - Israel Institute of Technology.

Author: Tom-Avi Shapira  
Supervisor: Prof. Israel Cohen
