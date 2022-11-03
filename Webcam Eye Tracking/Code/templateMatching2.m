%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [eye2_im_3, eye2_im_3_original, eye2_im_2, eye2_im_2_original, eye2_im_1, eye2_im_1_original, eye2_im_1_rgb, eye2_im_1_backOffsetA, eye2_im_1_backOffsetB, Error] = templateMatching2(eye2_im_3, eye2_im_3_original, eye2_im_2, eye2_im_2_original, eye2_im_1, eye2_im_1_original, eye2_im_1_rgb)
%% create templates    
    [~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...
    leftEYE_3_0_lookStraight, leftEYE_3_0_lookRight, leftEYE_3_0_lookLeft,...
    leftEYE_2_1_lookStraight, leftEYE_2_1_lookRight, leftEYE_2_1_lookLeft,...
    leftEYE_2_2_lookStraight, leftEYE_2_2_lookRight, leftEYE_2_2_lookLeft,...
    leftEYE_2_3_lookStraight, leftEYE_2_3_lookRight, leftEYE_2_3_lookLeft,...
    leftEYE_2_4_lookStraight, leftEYE_2_4_lookRight, leftEYE_2_4_lookLeft,...
    leftEYE_2_5_lookStraight, leftEYE_2_5_lookRight, leftEYE_2_5_lookLeft,...
    leftEYE_2_6_lookStraight, leftEYE_2_6_lookRight, leftEYE_2_6_lookLeft,...
    leftEYE_2_7_lookStraight, leftEYE_2_7_lookRight, leftEYE_2_7_lookLeft...
    ] = createTemplates();

%% Template matching eye1_im
    [~, yOffsetA, ~, heightA, vA ] = templateMatching_considerDirection( leftEYE_3_0_lookStraight, leftEYE_3_0_lookRight, leftEYE_3_0_lookLeft, eye2_im_3,2,30);
    eye2_im_2 = imcrop(eye2_im_2, [1, 2*(yOffsetA-2),size(eye2_im_2,2),2*(heightA+2)]);
    eye2_im_2_original = imcrop(eye2_im_2_original, [1, 2*(yOffsetA-2),size(eye2_im_2_original,2),2*(heightA+2)]);
    eye2_im_1 = imcrop(eye2_im_1, [1, 4*(yOffsetA-2),size(eye2_im_1,2),4*(heightA+2)]);
    eye2_im_1_original = imcrop(eye2_im_1_original, [1, 4*(yOffsetA-2),size(eye2_im_1_original,2),4*(heightA+2)]);
    eye2_im_1_backOffsetA = 4*(yOffsetA-2);
%     eye2_im_1_rgb = imcrop(eye2_im_1_rgb, [1, 4*(yOffsetA-2),size(eye2_im_1_rgb,2),4*(heightA+2)]); % optional, if wiil be needed in the future.
%--------------------------------------------------------------------------        
    [~, yOffset1, ~, height1, v1 ] = templateMatching_considerDirection( leftEYE_2_1_lookStraight, leftEYE_2_1_lookRight, leftEYE_2_1_lookLeft, eye2_im_2,2,21);
    [~, yOffset2, ~, height2, v2 ] = templateMatching_considerDirection( leftEYE_2_2_lookStraight, leftEYE_2_2_lookRight, leftEYE_2_2_lookLeft, eye2_im_2,2,22);
    [~, yOffset3, ~, height3, v3 ] = templateMatching_considerDirection( leftEYE_2_3_lookStraight, leftEYE_2_3_lookRight, leftEYE_2_3_lookLeft, eye2_im_2,2,23);
    [~, yOffset4, ~, height4, v4 ] = templateMatching_considerDirection( leftEYE_2_4_lookStraight, leftEYE_2_4_lookRight, leftEYE_2_4_lookLeft, eye2_im_2,2,24);
    [~, yOffset5, ~, height5, v5 ] = templateMatching_considerDirection( leftEYE_2_5_lookStraight, leftEYE_2_5_lookRight, leftEYE_2_5_lookLeft, eye2_im_2,2,25);
    [~, yOffset6, ~, height6, v6 ] = templateMatching_considerDirection( leftEYE_2_6_lookStraight, leftEYE_2_6_lookRight, leftEYE_2_6_lookLeft, eye2_im_2,2,26);
    [~, yOffset7, ~, height7, v7 ] = templateMatching_considerDirection( leftEYE_2_7_lookStraight, leftEYE_2_7_lookRight, leftEYE_2_7_lookLeft, eye2_im_2,2,27);

    Error = 0;
    if (v1==0 || v2==0 || v3==0 || v4==0 || v5==0 || v6==0 || v7==0)
        Error = 1;
    end

    vMax = max([v1 v2 v3 v4 v5 v6 v7]);
    if (vMax == v1)
        yOffsetB = yOffset1;
        heightB = height1;
    elseif (vMax == v2)
        yOffsetB = yOffset2;
        heightB = height2;
    elseif (vMax == v3) 
        yOffsetB = yOffset3;
        heightB = height3;
    elseif (vMax == v4) 
        yOffsetB = yOffset4;
        heightB = height4; 
    elseif (vMax == v5) 
        yOffsetB = yOffset5;
        heightB = height5;
    elseif (vMax == v6) 
        yOffsetB = yOffset6;
        heightB = height6;
    else 
        yOffsetB = yOffset7;
        heightB = height7;
    end
    eye2_im_2 = imcrop(eye2_im_2, [1,yOffsetB-4,size(eye2_im_2,2),heightB+4]);
    eye2_im_2_original = imcrop(eye2_im_2_original, [1,yOffsetB-4,size(eye2_im_2_original,2),heightB+4]);
    eye2_im_1 = imcrop(eye2_im_1, [1, 2*(yOffsetB-4),size(eye2_im_1,2),2*(heightB+4)]);
    eye2_im_1_original = imcrop(eye2_im_1_original, [1, 2*(yOffsetB-4),size(eye2_im_1_original,2),2*(heightB+4)]);
    eye2_im_1_backOffsetB = 2*(yOffsetB-4);
%     eye2_im_1_rgb = imcrop(eye2_im_1_rgb, [1, 2*(yOffsetB-4),size(eye2_im_1_rgb,2),2*(heightB+4)]); % optional, if wiil be needed in the future.
    
end

