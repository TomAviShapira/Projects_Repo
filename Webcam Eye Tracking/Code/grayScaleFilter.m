%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ indVec, threshold ] = grayScaleFilter( avgGrayLevelVec, oldThreshold )
    minAvgGrayLevel = min(avgGrayLevelVec(:,2));
    maxAvgGrayLevel = max(avgGrayLevelVec(:,2));
    if (maxAvgGrayLevel - minAvgGrayLevel < 0.03)
        threshold = maxAvgGrayLevel;
    else
            threshold = minAvgGrayLevel + ((maxAvgGrayLevel - minAvgGrayLevel) / 3);
    end
    if (minAvgGrayLevel > oldThreshold) % all the results in avgGrayLevelVec are not good
        threshold = oldThreshold;
    end
    indVec = (avgGrayLevelVec(:,2) <= threshold);
%     newAvgGrayLevelVec = avgGrayLevelVec(ind,:);
end
