%%
% Tom-Avi Shapira
% Lital Yakobov

%%
close all;
clear all;
clc;
warning off;

% runVideo also save rezults in the 'videoName' folder

%%  ===========================================================================
%% tom
video = VideoReader('videos/tom.mp4');
[audio,Fs]=audioread('videos/tom.mp4');
videoName = 'tom';
runVideo(video, audio, Fs, videoName, false, videoName);

%% tomR
video = VideoReader('videos/tomR.mp4');
[audio,Fs]=audioread('videos/tomR.mp4');
videoName = 'tomR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% lital
video = VideoReader('videos/lital.mp4');
[audio,Fs]=audioread('videos/lital.mp4');
videoName = 'lital';
runVideo(video, audio, Fs, videoName, false, videoName);

%% litalR
video = VideoReader('videos/litalR.mp4');
[audio,Fs]=audioread('videos/litalR.mp4');
videoName = 'litalR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% bar
video = VideoReader('videos/bar.mp4');
[audio,Fs]=audioread('videos/bar.mp4');
videoName = 'bar';
runVideo(video, audio, Fs, videoName, false, videoName);

%% barR
video = VideoReader('videos/barR.mp4');
[audio,Fs]=audioread('videos/barR.mp4');
videoName = 'barR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% alon
video = VideoReader('videos/alon.mp4');
[audio,Fs]=audioread('videos/alon.mp4');
videoName = 'alon';
runVideo(video, audio, Fs, videoName, false, videoName);

%% alonR
video = VideoReader('videos/alonR.mp4');
[audio,Fs]=audioread('videos/alonR.mp4');
videoName = 'alonR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% amitay
video = VideoReader('videos/amitay.mp4');
[audio,Fs]=audioread('videos/amitay.mp4');
videoName = 'amitay';
runVideo(video, audio, Fs, videoName, false, videoName);

%% amitayR
video = VideoReader('videos/amitayR.mp4');
[audio,Fs]=audioread('videos/amitayR.mp4');
videoName = 'amitayR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% aviya
video = VideoReader('videos/aviya.mp4');
[audio,Fs]=audioread('videos/aviya.mp4');
videoName = 'aviya';
runVideo(video, audio, Fs, videoName, false, videoName);

%% aviyaR
video = VideoReader('videos/aviyaR.mp4');
[audio,Fs]=audioread('videos/aviyaR.mp4');
videoName = 'aviyaR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% batSheva
video = VideoReader('videos/batSheva.mp4');
[audio,Fs]=audioread('videos/batSheva.mp4');
videoName = 'batSheva';
runVideo(video, audio, Fs, videoName, false, videoName);

%% batShevaR
video = VideoReader('videos/batShevaR.mp4');
[audio,Fs]=audioread('videos/batShevaR.mp4');
videoName = 'batShevaR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% eran
video = VideoReader('videos/eran.mp4');
[audio,Fs]=audioread('videos/eran.mp4');
videoName = 'eran';
runVideo(video, audio, Fs, videoName, false, videoName);

%% eranR
video = VideoReader('videos/eranR.mp4');
[audio,Fs]=audioread('videos/eranR.mp4');
videoName = 'eranR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% erez
video = VideoReader('videos/erez.mp4');
[audio,Fs]=audioread('videos/erez.mp4');
videoName = 'erez';
runVideo(video, audio, Fs, videoName, false, videoName);

%% erezR
video = VideoReader('videos/erezR.mp4');
[audio,Fs]=audioread('videos/erezR.mp4');
videoName = 'erezR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% hanan
video = VideoReader('videos/hanan.mp4');
[audio,Fs]=audioread('videos/hanan.mp4');
videoName = 'hanan';
runVideo(video, audio, Fs, videoName, false, videoName);

%% hananR
video = VideoReader('videos/hananR.mp4');
[audio,Fs]=audioread('videos/hananR.mp4');
videoName = 'hananR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% idank
video = VideoReader('videos/idank.mp4');
[audio,Fs]=audioread('videos/idank.mp4');
videoName = 'idank';
runVideo(video, audio, Fs, videoName, false, videoName);

%% idankR
video = VideoReader('videos/idankR.mp4');
[audio,Fs]=audioread('videos/idankR.mp4');
videoName = 'idankR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% lior
video = VideoReader('videos/lior.mp4');
[audio,Fs]=audioread('videos/lior.mp4');
videoName = 'lior';
runVideo(video, audio, Fs, videoName, false, videoName);

%% liorR
video = VideoReader('videos/liorR.mp4');
[audio,Fs]=audioread('videos/liorR.mp4');
videoName = 'liorR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% maya
video = VideoReader('videos/maya.mp4');
[audio,Fs]=audioread('videos/maya.mp4');
videoName = 'maya';
runVideo(video, audio, Fs, videoName, false, videoName);

%% mayaR
video = VideoReader('videos/mayaR.mp4');
[audio,Fs]=audioread('videos/mayaR.mp4');
videoName = 'mayaR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% or
video = VideoReader('videos/or.mp4');
[audio,Fs]=audioread('videos/or.mp4');
videoName = 'or';
runVideo(video, audio, Fs, videoName, false, videoName);

%% orR
video = VideoReader('videos/orR.mp4');
[audio,Fs]=audioread('videos/orR.mp4');
videoName = 'orR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% ori
video = VideoReader('videos/ori.mp4');
[audio,Fs]=audioread('videos/ori.mp4');
videoName = 'ori';
runVideo(video, audio, Fs, videoName, false, videoName);

%% oriR
video = VideoReader('videos/oriR.mp4');
[audio,Fs]=audioread('videos/oriR.mp4');
videoName = 'oriR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% regev
video = VideoReader('videos/regev.mp4');
[audio,Fs]=audioread('videos/regev.mp4');
videoName = 'regev';
runVideo(video, audio, Fs, videoName, false, videoName);

%% regevR
video = VideoReader('videos/regevR.mp4');
[audio,Fs]=audioread('videos/regevR.mp4');
videoName = 'regevR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% rotem
video = VideoReader('videos/rotem.mp4');
[audio,Fs]=audioread('videos/rotem.mp4');
videoName = 'rotem';
runVideo(video, audio, Fs, videoName, false, videoName);

%% rotemR
video = VideoReader('videos/rotemR.mp4');
[audio,Fs]=audioread('videos/rotemR.mp4');
videoName = 'rotemR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% tal
video = VideoReader('videos/tal.mp4');
[audio,Fs]=audioread('videos/tal.mp4');
videoName = 'tal';
runVideo(video, audio, Fs, videoName, false, videoName);

%% talR
video = VideoReader('videos/talR.mp4');
[audio,Fs]=audioread('videos/talR.mp4');
videoName = 'talR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% tamar
video = VideoReader('videos/tamar.mp4');
[audio,Fs]=audioread('videos/tamar.mp4');
videoName = 'tamar';
runVideo(video, audio, Fs, videoName, false, videoName);

%% tamarR
video = VideoReader('videos/tamarR.mp4');
[audio,Fs]=audioread('videos/tamarR.mp4');
videoName = 'tamarR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% yair
video = VideoReader('videos/yair.mp4');
[audio,Fs]=audioread('videos/yair.mp4');
videoName = 'yair';
runVideo(video, audio, Fs, videoName, false, videoName);

%% yairR
video = VideoReader('videos/yairR.mp4');
[audio,Fs]=audioread('videos/yairR.mp4');
videoName = 'yairR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% yovel
video = VideoReader('videos/yovel.mp4');
[audio,Fs]=audioread('videos/yovel.mp4');
videoName = 'yovel';
runVideo(video, audio, Fs, videoName, false, videoName);

%% yovelR
video = VideoReader('videos/yovelR.mp4');
[audio,Fs]=audioread('videos/yovelR.mp4');
videoName = 'yovelR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% zohar
video = VideoReader('videos/zohar.mp4');
[audio,Fs]=audioread('videos/zohar.mp4');
videoName = 'zohar';
runVideo(video, audio, Fs, videoName, false, videoName);

%% zoharR
video = VideoReader('videos/zoharR.mp4');
[audio,Fs]=audioread('videos/zoharR.mp4');
videoName = 'zoharR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% tali
video = VideoReader('videos/tali.mp4');
[audio,Fs]=audioread('videos/tali.mp4');
videoName = 'tali';
runVideo(video, audio, Fs, videoName, false, videoName);

%% taliR
video = VideoReader('videos/taliR.mp4');
[audio,Fs]=audioread('videos/taliR.mp4');
videoName = 'taliR';
runVideo(video, audio, Fs, videoName, true, videoName);
%%  ===========================================================================
%% end simulation msg
sendMail('simulation', [], [], [], []);


