%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [] = videoDisplay(video, correctScreenSectionNEW)
%% display the results after analyzing
% video has to be synchronized (after videosPreProcess)
% correctScreenSectionNEW is the result vector of the algorithm (result of eyeTracker)
    monitorVideo = VideoReader('videos/monitorVideo.mp4');
    i = 0;
    frameNum = 0;
    while hasFrame(video) && hasFrame(monitorVideo)
        frameNum = frameNum + 1;
        subplot(2,1,2);
        monitorVidFrame = readFrame(monitorVideo);
        
        if (mod(frameNum,3) == 0) %frame skip
            image(monitorVidFrame);
            hold on;
            if (frameNum >=300 && mod(frameNum,15) == 0)
                rectangle('Position',[correctScreenSectionNEW(i+1,2)*192-190 10 190 1050],'EdgeColor','y','LineWidth',3);
                i = i+1;
                hold off;
            end
        end

        subplot(2,1,1);
        vidFrame = readFrame(video);
        if (mod(frameNum,3) == 0) %frame skip
            image(flip(vidFrame,2));
        end

        pause(1/monitorVideo.framerate);
    end    
end

