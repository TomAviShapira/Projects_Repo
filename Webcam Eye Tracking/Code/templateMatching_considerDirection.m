%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ xOffset, yOffset, width, height, vA ] = templateMatching_considerDirection( lookStraight, lookRight, lookLeft, image,eyeNum,templateNum )
    [xOffsetA1, yOffsetA1, widthA1, heightA1, vA1] = templateMatching_ncc(lookStraight,image,eyeNum,templateNum);
    [xOffsetA2, yOffsetA2, widthA2, heightA2, vA2] = templateMatching_ncc(lookRight,image,eyeNum,templateNum);
    [xOffsetA3, yOffsetA3, widthA3, heightA3, vA3] = templateMatching_ncc(lookLeft,image,eyeNum,templateNum);
    vA = max([vA1 vA2 vA3]);
    if (vA == vA1)
        xOffset = xOffsetA1;
        yOffset = yOffsetA1;
        width = widthA1;
        height = heightA1;
    elseif (vA == vA2)
        xOffset = xOffsetA2;
        yOffset = yOffsetA2;
        width = widthA2;
        height = heightA2;
    else 
        xOffset = xOffsetA3;
        yOffset = yOffsetA3;
        width = widthA3;
        height = heightA3;
    end
end

