%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [eye1_im_3, eye1_im_3_original, eye1_im_2, eye1_im_2_original, eye1_im_1, eye1_im_1_original, eye1_im_1_rgb, eye1_im_1_backOffsetA, eye1_im_1_backOffsetB, Error] = templateMatching1(eye1_im_3, eye1_im_3_original, eye1_im_2, eye1_im_2_original, eye1_im_1, eye1_im_1_original, eye1_im_1_rgb)
%% create templates    
    [rightEYE_3_0_lookStraight, rightEYE_3_0_lookRight, rightEYE_3_0_lookLeft,...
    rightEYE_2_1_lookStraight, rightEYE_2_1_lookRight, rightEYE_2_1_lookLeft,...
    rightEYE_2_2_lookStraight, rightEYE_2_2_lookRight, rightEYE_2_2_lookLeft,...
    rightEYE_2_3_lookStraight, rightEYE_2_3_lookRight, rightEYE_2_3_lookLeft,...
    rightEYE_2_4_lookStraight, rightEYE_2_4_lookRight, rightEYE_2_4_lookLeft,...
    rightEYE_2_5_lookStraight, rightEYE_2_5_lookRight, rightEYE_2_5_lookLeft,...
    rightEYE_2_6_lookStraight, rightEYE_2_6_lookRight, rightEYE_2_6_lookLeft,...
    rightEYE_2_7_lookStraight, rightEYE_2_7_lookRight, rightEYE_2_7_lookLeft,...
    ~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...
    ~, ~, ~,...    
    ~, ~, ~...
    ] = createTemplates();

%% Template matching eye1_im
    [~, yOffsetA, ~, heightA, vA ] = templateMatching_considerDirection( rightEYE_3_0_lookStraight, rightEYE_3_0_lookRight, rightEYE_3_0_lookLeft, eye1_im_3,1,30);
    eye1_im_2 = imcrop(eye1_im_2, [1, 2*(yOffsetA-2),size(eye1_im_2,2),2*(heightA+2)]);
    eye1_im_2 = imgaussfilt(eye1_im_2,1);
    eye1_im_2_original = imcrop(eye1_im_2_original, [1, 2*(yOffsetA-2),size(eye1_im_2_original,2),2*(heightA+2)]);
    eye1_im_1 = imcrop(eye1_im_1, [1, 4*(yOffsetA-2),size(eye1_im_1,2),4*(heightA+2)]);
    eye1_im_1_original = imcrop(eye1_im_1_original, [1, 4*(yOffsetA-2),size(eye1_im_1_original,2),4*(heightA+2)]);
    eye1_im_1_backOffsetA = 4*(yOffsetA-2);
%     eye1_im_1_rgb = imcrop(eye1_im_1_rgb, [1, 4*(yOffsetA-2),size(eye1_im_1_rgb,2),4*(heightA+2)]); % optional, if wiil be needed in the future.
%--------------------------------------------------------------------------   
    [~, yOffset1, ~, height1, v1 ] = templateMatching_considerDirection( rightEYE_2_1_lookStraight, rightEYE_2_1_lookRight, rightEYE_2_1_lookLeft, eye1_im_2,1,21);
    [~, yOffset2, ~, height2, v2 ] = templateMatching_considerDirection( rightEYE_2_2_lookStraight, rightEYE_2_2_lookRight, rightEYE_2_2_lookLeft, eye1_im_2,1,22);
    [~, yOffset3, ~, height3, v3 ] = templateMatching_considerDirection( rightEYE_2_3_lookStraight, rightEYE_2_3_lookRight, rightEYE_2_3_lookLeft, eye1_im_2,1,23);
    [~, yOffset4, ~, height4, v4 ] = templateMatching_considerDirection( rightEYE_2_4_lookStraight, rightEYE_2_4_lookRight, rightEYE_2_4_lookLeft, eye1_im_2,1,24);
    [~, yOffset5, ~, height5, v5 ] = templateMatching_considerDirection( rightEYE_2_5_lookStraight, rightEYE_2_5_lookRight, rightEYE_2_5_lookLeft, eye1_im_2,1,25);
    [~, yOffset6, ~, height6, v6 ] = templateMatching_considerDirection( rightEYE_2_6_lookStraight, rightEYE_2_6_lookRight, rightEYE_2_6_lookLeft, eye1_im_2,1,26);
    [~, yOffset7, ~, height7, v7 ] = templateMatching_considerDirection( rightEYE_2_7_lookStraight, rightEYE_2_7_lookRight, rightEYE_2_7_lookLeft, eye1_im_2,1,27);
    
    Error = 0;
    if (v1==0 || v2==0 || v3==0 || v4==0 && v5==0 || v6==0 || v7==0)
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
    eye1_im_2 = imcrop(eye1_im_2, [1,yOffsetB-4,size(eye1_im_2,2),heightB+4]);
    eye1_im_2_original = imcrop(eye1_im_2_original, [1,yOffsetB-4,size(eye1_im_2_original,2),heightB+4]);
    eye1_im_1 = imcrop(eye1_im_1, [1, 2*(yOffsetB-4),size(eye1_im_1,2),2*(heightB+4)]);
    eye1_im_1_original = imcrop(eye1_im_1_original, [1, 2*(yOffsetB-4),size(eye1_im_1_original,2),2*(heightB+4)]);
    eye1_im_1_backOffsetB = 2*(yOffsetB-4);
%     eye1_im_1_rgb = imcrop(eye1_im_1_rgb, [1, 2*(yOffsetB-4),size(eye1_im_1_rgb,2),2*(heightB+4)]); % optional, if wiil be needed in the future.
    
end

