%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ video, startTime ] = videosPreProcess(video, audio, Fs)
%% pre processing
    dt = 1/Fs;
    t = 0:dt:(length(audio)*dt)-dt;
%     figure();
%     plot(t,audio);
    m = max(audio(1:220500)); % take max from 1-5 sec
    startTime = t(find(audio>0.5*m,1));
    video.CurrentTime = startTime;
end

