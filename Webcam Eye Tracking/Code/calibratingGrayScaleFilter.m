%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ indVec, threshold ] = calibratingGrayScaleFilter( avgGrayLevelVec )
    minAvgGrayLevel = min(avgGrayLevelVec(:,2));
    maxAvgGrayLevel = max(avgGrayLevelVec(:,2));
    if (maxAvgGrayLevel - minAvgGrayLevel < 0.03)
        threshold = maxAvgGrayLevel;
    else
        threshold = minAvgGrayLevel + ((maxAvgGrayLevel - minAvgGrayLevel) / 3);
    end
    indVec = (avgGrayLevelVec(:,2) <= threshold);
%     newAvgGrayLevelVec = avgGrayLevelVec(ind,:);
end
