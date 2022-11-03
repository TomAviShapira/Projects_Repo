%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ xVec, yVec, rVec, avgGrayLevelVec ] = createLeftEyeFrameBuffer( xVec, yVec, rVec, avgGrayLevelVec,...
                                              xFace, yFace, rFace,...
                                              xNoseFinal, yNoseFinal,...
                                              Face, frameNum)
%                    ====== saving coordinates ======          
    xVec = [xVec ; frameNum (xNoseFinal - xFace)];
    yVec = [yVec ; frameNum (yNoseFinal - yFace)];
    rVec = [rVec ; frameNum rFace];
%                    ====== calculationg avg gray level for results filter ======          
    avgGrayLevelVec = [avgGrayLevelVec ; avgGrayLevelCalc(Face, xFace, yFace, rFace, frameNum)];


end

