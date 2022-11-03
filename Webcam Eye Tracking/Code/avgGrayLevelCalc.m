%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ avgGrayLevel ] = avgGrayLevelCalc( Face, x, y, r, frameNum )
    avgGrayLevel(1,1) = frameNum;
    irisImage = imcrop(Face, [x-r, y-r, 2*r, 2*r]);
%     figure();imshow(irisImage);
    avgGrayLevel(1,2) = mean(mean(irisImage));
end

