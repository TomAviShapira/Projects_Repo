%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [xOffset, yOffset, width, height, v] = templateMatching_ncc(template,image,eyeNum,templateNum)
    if (size(template,1)>size(image,1) || size(template,2)>size(image,2))
        xOffset = 1;
        yOffset = 1;
        height = size(image,1);
        width = size(image,2);
        v = 0;
        if (eyeNum == 1)
            fprintf('templateMatching_ncc : rightEYE_%d_%d FAIL\n',floor(templateNum/10),mod(templateNum,10));
        else
            fprintf('templateMatching_ncc : leftEYE_%d_%d FAIL\n',floor(templateNum/10),mod(templateNum,10));
        end
        return;
    end

    c = normxcorr2(template,image);
    cVec = c(:);
%     figure, surf(c), shading flat
    [v] = max(cVec);
    [ypeak, xpeak] = find(c==v);
    yOffset = ypeak-size(template,1);
    xOffset = xpeak-size(template,2);
    
    width = size(template,2);
    height = size(template,1);
   
%% show results 
%     figure();
%     imshow(image);
%     imrect(gca, [xOffset, yOffset, width, height]);
%     impixelinfo;
    
    