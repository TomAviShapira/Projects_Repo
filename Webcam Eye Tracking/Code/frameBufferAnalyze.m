%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ xVec, yVec, rVec, xfinal, yfinal, threshold ] = frameBufferAnalyze( xVec, yVec, rVec, avgGrayLevelVec, oldThreshold, isCalibrating, filter )
    if (isCalibrating)
        [indVec, newThreshold] = calibratingGrayScaleFilter(avgGrayLevelVec);
    else
        [indVec, newThreshold] = grayScaleFilter(avgGrayLevelVec, oldThreshold);
    end
    if (oldThreshold == -1)
        oldThreshold = newThreshold;
    end
    threshold = mean([oldThreshold newThreshold]);
    xVec = xVec(indVec,:);
    yVec = yVec(indVec,:);
    rVec = rVec(indVec,:);
    irregularLocationIndVec = locationFilter(yVec(:,2));
    xVec(irregularLocationIndVec,:) = [];
    yVec(irregularLocationIndVec,:) = [];
    rVec(irregularLocationIndVec,:) = []; 
    irregularLocationIndVec = locationFilter(xVec(:,2));
    xVec(irregularLocationIndVec,:) = [];
    yVec(irregularLocationIndVec,:) = [];
    rVec(irregularLocationIndVec,:) = []; 
    if (strcmp(filter,'mean'))
        xfinal = mean(xVec(:,2));
        yfinal = mean(yVec(:,2));
    elseif (strcmp(filter,'median'))
        xfinal = median(xVec(:,2));
        yfinal = median(yVec(:,2));
    end
    
end

