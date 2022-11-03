%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ rightEYE_3_0_lookStraight, rightEYE_3_0_lookRight, rightEYE_3_0_lookLeft,...
           rightEYE_2_1_lookStraight, rightEYE_2_1_lookRight, rightEYE_2_1_lookLeft,...
           rightEYE_2_2_lookStraight, rightEYE_2_2_lookRight, rightEYE_2_2_lookLeft,...
           rightEYE_2_3_lookStraight, rightEYE_2_3_lookRight, rightEYE_2_3_lookLeft,...
           rightEYE_2_4_lookStraight, rightEYE_2_4_lookRight, rightEYE_2_4_lookLeft,...
           rightEYE_2_5_lookStraight, rightEYE_2_5_lookRight, rightEYE_2_5_lookLeft,...
           rightEYE_2_6_lookStraight, rightEYE_2_6_lookRight, rightEYE_2_6_lookLeft,...
           rightEYE_2_7_lookStraight, rightEYE_2_7_lookRight, rightEYE_2_7_lookLeft,...
           leftEYE_3_0_lookStraight, leftEYE_3_0_lookRight, leftEYE_3_0_lookLeft,...
           leftEYE_2_1_lookStraight, leftEYE_2_1_lookRight, leftEYE_2_1_lookLeft,...
           leftEYE_2_2_lookStraight, leftEYE_2_2_lookRight, leftEYE_2_2_lookLeft,...
           leftEYE_2_3_lookStraight, leftEYE_2_3_lookRight, leftEYE_2_3_lookLeft,...
           leftEYE_2_4_lookStraight, leftEYE_2_4_lookRight, leftEYE_2_4_lookLeft,...
           leftEYE_2_5_lookStraight, leftEYE_2_5_lookRight, leftEYE_2_5_lookLeft,...
           leftEYE_2_6_lookStraight, leftEYE_2_6_lookRight, leftEYE_2_6_lookLeft,...
           leftEYE_2_7_lookStraight, leftEYE_2_7_lookRight, leftEYE_2_7_lookLeft...
           ] = createTemplates()
%% template eye1_im
    rightEYE = imread('imagesALL/rightEYE2.png');
    rightEYE = rgb2gray(rightEYE);
    rightEYE_1_0 = imresize(rightEYE, [34,55]);
    rightEYE_2_0 = impyramid(rightEYE_1_0,'reduce');
    rightEYE_3_0 = impyramid(rightEYE_2_0,'reduce');
    rightEYE_3_0 = histeq(rightEYE_3_0);
%--------------------------------------------------------------------------
    rightEYE_3_0(9,6:9) = 80;
    rightEYE_3_0(9,10) = 100;
    rightEYE_3_0(9,5) = 100;
    rightEYE_3_0(8,11) = 100;
    rightEYE_3_0(7,12) = 100;
    rightEYE_3_0(6,13) = 100;
    rightEYE_3_0(8,4) = 120;
    rightEYE_3_0(4:7,4:5) = 230;
    rightEYE_3_0(4:7,10:11) = 230;
    rightEYE_3_0(5:6,3) = 230;
    rightEYE_3_0(5:6,12) = 230;
    rightEYE_3_0(3,5) = 230;
    rightEYE_3_0(3,10) = 230;
    rightEYE_3_0(8,6:10) = 230;
    rightEYE_3_0(7,6) = 230;
    rightEYE_3_0(7,9) = 230;
    rightEYE_3_0(9,1:3) = 206;
    rightEYE_3_0(7:9,14) = 206;
    rightEYE_3_0(9,13) = 206;
    rightEYE_3_0(2,6:9) = 67;
%--------------------------------------------------------------------------
    rightEYE_3_0 = imgaussfilt(rightEYE_3_0,0.5);
    rightEYE_3_0 = im2double(rightEYE_3_0);
    rightEYE_2_0 = impyramid(rightEYE_3_0,'expand');
    width_rightEYE_2_0 = size(rightEYE_2_0,2);
    rightEYE_2_0 = imcrop(rightEYE_2_0,[1,3,width_rightEYE_2_0,12]);
%--------------------------------------------------------------------------
    rightEYE_3_0_lookStraight = impyramid(rightEYE_2_0,'reduce');
    rightEYE_3_0_lookRight = rightEYE_3_0_lookStraight;
    rightEYE_3_0_lookRight(2:6,9:11) = 0;
    rightEYE_3_0_lookRight(2:6,5:6) = 0.7;
    rightEYE_3_0_lookRight = imgaussfilt(rightEYE_3_0_lookRight,1);
    rightEYE_3_0_lookLeft = rightEYE_3_0_lookStraight;
    rightEYE_3_0_lookLeft(2:6,4:6) = 0;
    rightEYE_3_0_lookLeft(2:6,9:10) = 0.7;
    rightEYE_3_0_lookLeft = imgaussfilt(rightEYE_3_0_lookLeft,1);
%--------------------------------------------------------------------------
    rightEYE_2_1_lookStraight = imresize(rightEYE_2_0, [8,width_rightEYE_2_0]);
    rightEYE_2_1_lookRight = rightEYE_2_1_lookStraight;
    rightEYE_2_1_lookRight(2:7,14:19) = 0;
    rightEYE_2_1_lookRight(2:7,7:13) = 0.7;
    rightEYE_2_1_lookRight = imgaussfilt(rightEYE_2_1_lookRight,1);
    rightEYE_2_1_lookLeft = rightEYE_2_1_lookStraight;
    rightEYE_2_1_lookLeft(2:7,8:13) = 0;
    rightEYE_2_1_lookLeft(2:7,14:20) = 0.7;
    rightEYE_2_1_lookLeft = imgaussfilt(rightEYE_2_1_lookLeft,1);
%--------------------------------------------------------------------------    
    rightEYE_2_2_lookStraight = imresize(rightEYE_2_0, [9,width_rightEYE_2_0]);
    rightEYE_2_2_lookRight = rightEYE_2_2_lookStraight;
    rightEYE_2_2_lookRight(2:8,14:19) = 0;
    rightEYE_2_2_lookRight(2:8,7:13) = 0.7;
    rightEYE_2_2_lookRight = imgaussfilt(rightEYE_2_2_lookRight,1);
    rightEYE_2_2_lookLeft = rightEYE_2_2_lookStraight;
    rightEYE_2_2_lookLeft(2:8,8:13) = 0;
    rightEYE_2_2_lookLeft(2:8,14:20) = 0.7;
    rightEYE_2_2_lookLeft = imgaussfilt(rightEYE_2_2_lookLeft,1);
%--------------------------------------------------------------------------    
    rightEYE_2_3_lookStraight = imresize(rightEYE_2_0, [10,width_rightEYE_2_0]);
    rightEYE_2_3_lookRight = rightEYE_2_3_lookStraight;
    rightEYE_2_3_lookRight(2:9,14:19) = 0;
    rightEYE_2_3_lookRight(2:9,7:13) = 0.7;
    rightEYE_2_3_lookRight = imgaussfilt(rightEYE_2_3_lookRight,1);
    rightEYE_2_3_lookLeft = rightEYE_2_3_lookStraight;
    rightEYE_2_3_lookLeft(2:9,8:13) = 0;
    rightEYE_2_3_lookLeft(2:9,14:20) = 0.7;
    rightEYE_2_3_lookLeft = imgaussfilt(rightEYE_2_3_lookLeft,1);  
%--------------------------------------------------------------------------    
    rightEYE_2_4_lookStraight = imresize(rightEYE_2_0, [11,width_rightEYE_2_0]);
    rightEYE_2_4_lookRight = rightEYE_2_4_lookStraight;
    rightEYE_2_4_lookRight(2:10,14:19) = 0;
    rightEYE_2_4_lookRight(2:10,7:13) = 0.7;
    rightEYE_2_4_lookRight = imgaussfilt(rightEYE_2_4_lookRight,1);
    rightEYE_2_4_lookLeft = rightEYE_2_4_lookStraight;
    rightEYE_2_4_lookLeft(2:10,8:13) = 0;
    rightEYE_2_4_lookLeft(2:10,14:20) = 0.7;
    rightEYE_2_4_lookLeft = imgaussfilt(rightEYE_2_4_lookLeft,1);
%--------------------------------------------------------------------------    
    rightEYE_2_5_lookStraight = imresize(rightEYE_2_0, [12,width_rightEYE_2_0]);
    rightEYE_2_5_lookRight = rightEYE_2_5_lookStraight;
    rightEYE_2_5_lookRight(2:11,14:19) = 0;
    rightEYE_2_5_lookRight(2:11,7:13) = 0.7;
    rightEYE_2_5_lookRight = imgaussfilt(rightEYE_2_5_lookRight,1);
    rightEYE_2_5_lookLeft = rightEYE_2_5_lookStraight;
    rightEYE_2_5_lookLeft(2:11,8:13) = 0;
    rightEYE_2_5_lookLeft(2:11,14:20) = 0.7;
    rightEYE_2_5_lookLeft = imgaussfilt(rightEYE_2_5_lookLeft,1);
%--------------------------------------------------------------------------    
    rightEYE_2_6_lookStraight = imresize(rightEYE_2_0, [13,width_rightEYE_2_0]);
    rightEYE_2_6_lookRight = rightEYE_2_6_lookStraight;
    rightEYE_2_6_lookRight(2:12,13:19) = 0;
    rightEYE_2_6_lookRight(2:12,7:12) = 0.7;
    rightEYE_2_6_lookRight = imgaussfilt(rightEYE_2_6_lookRight,1);
    rightEYE_2_6_lookLeft = rightEYE_2_6_lookStraight;
    rightEYE_2_6_lookLeft(3:12,8:15) = 0;
    rightEYE_2_6_lookLeft(3:12,15:20) = 0.7;
    rightEYE_2_6_lookLeft = imgaussfilt(rightEYE_2_6_lookLeft,1);
 %--------------------------------------------------------------------------   
    rightEYE_2_7_lookStraight = imresize(rightEYE_2_0, [14,width_rightEYE_2_0]); 
    rightEYE_2_7_lookRight = rightEYE_2_7_lookStraight;
    rightEYE_2_7_lookRight(3:13,12:19) = 0;
    rightEYE_2_7_lookRight(3:13,5:11) = 0.7;
    rightEYE_2_7_lookRight = imgaussfilt(rightEYE_2_7_lookRight,1);
    rightEYE_2_7_lookLeft = rightEYE_2_7_lookStraight;
    rightEYE_2_7_lookLeft(3:13,8:15) = 0;
    rightEYE_2_7_lookLeft(3:13,16:22) = 0.7;
    rightEYE_2_7_lookLeft = imgaussfilt(rightEYE_2_7_lookLeft,1);

%% template eye2_im
    leftEYE_3_0_lookStraight = flip(rightEYE_3_0_lookStraight,2);
    leftEYE_3_0_lookRight = leftEYE_3_0_lookStraight;
    leftEYE_3_0_lookRight(2:6,9:11) = 0;
    leftEYE_3_0_lookRight(2:6,5:6) = 0.7;
    leftEYE_3_0_lookRight = imgaussfilt(leftEYE_3_0_lookRight,1);
    leftEYE_3_0_lookLeft = leftEYE_3_0_lookStraight;
    leftEYE_3_0_lookLeft(2:6,4:6) = 0;
    leftEYE_3_0_lookLeft(2:6,9:10) = 0.7;
    leftEYE_3_0_lookLeft = imgaussfilt(leftEYE_3_0_lookLeft,1);
%--------------------------------------------------------------------------
    leftEYE_2_1_lookStraight = flip(rightEYE_2_1_lookStraight,2);
    leftEYE_2_1_lookRight = leftEYE_2_1_lookStraight;
    leftEYE_2_1_lookRight(2:7,14:19) = 0;
    leftEYE_2_1_lookRight(2:7,7:13) = 0.7;
    leftEYE_2_1_lookRight = imgaussfilt(leftEYE_2_1_lookRight,1);
    leftEYE_2_1_lookLeft = leftEYE_2_1_lookStraight;
    leftEYE_2_1_lookLeft(2:7,8:13) = 0;
    leftEYE_2_1_lookLeft(2:7,14:20) = 0.7;
    leftEYE_2_1_lookLeft = imgaussfilt(leftEYE_2_1_lookLeft,1);
%--------------------------------------------------------------------------    
    leftEYE_2_2_lookStraight = flip(rightEYE_2_2_lookStraight,2);
    leftEYE_2_2_lookRight = leftEYE_2_2_lookStraight;
    leftEYE_2_2_lookRight(2:8,14:19) = 0;
    leftEYE_2_2_lookRight(2:8,7:13) = 0.7;
    leftEYE_2_2_lookRight = imgaussfilt(leftEYE_2_2_lookRight,1);
    leftEYE_2_2_lookLeft = leftEYE_2_2_lookStraight;
    leftEYE_2_2_lookLeft(2:8,8:13) = 0;
    leftEYE_2_2_lookLeft(2:8,14:20) = 0.7;
    leftEYE_2_2_lookLeft = imgaussfilt(leftEYE_2_2_lookLeft,1);
%--------------------------------------------------------------------------   
    leftEYE_2_3_lookStraight = flip(rightEYE_2_3_lookStraight,2);
    leftEYE_2_3_lookRight = leftEYE_2_3_lookStraight;
    leftEYE_2_3_lookRight(2:9,14:19) = 0;
    leftEYE_2_3_lookRight(2:9,7:13) = 0.7;
    leftEYE_2_3_lookRight = imgaussfilt(leftEYE_2_3_lookRight,1);
    leftEYE_2_3_lookLeft = leftEYE_2_3_lookStraight;
    leftEYE_2_3_lookLeft(2:9,8:13) = 0;
    leftEYE_2_3_lookLeft(2:9,14:20) = 0.7;
    leftEYE_2_3_lookLeft = imgaussfilt(leftEYE_2_3_lookLeft,1);
%--------------------------------------------------------------------------    
    leftEYE_2_4_lookStraight = flip(rightEYE_2_4_lookStraight,2);
    leftEYE_2_4_lookRight = leftEYE_2_4_lookStraight;
    leftEYE_2_4_lookRight(2:10,14:19) = 0;
    leftEYE_2_4_lookRight(2:10,7:13) = 0.7;
    leftEYE_2_4_lookRight = imgaussfilt(leftEYE_2_4_lookRight,1);
    leftEYE_2_4_lookLeft = leftEYE_2_4_lookStraight;
    leftEYE_2_4_lookLeft(2:10,8:13) = 0;
    leftEYE_2_4_lookLeft(2:10,14:20) = 0.7;
    leftEYE_2_4_lookLeft = imgaussfilt(leftEYE_2_4_lookLeft,1);
%--------------------------------------------------------------------------    
    leftEYE_2_5_lookStraight = flip(rightEYE_2_5_lookStraight,2);
    leftEYE_2_5_lookRight = leftEYE_2_5_lookStraight;
    leftEYE_2_5_lookRight(2:11,14:19) = 0;
    leftEYE_2_5_lookRight(2:11,7:13) = 0.7;
    leftEYE_2_5_lookRight = imgaussfilt(leftEYE_2_5_lookRight,1);
    leftEYE_2_5_lookLeft = leftEYE_2_5_lookStraight;
    leftEYE_2_5_lookLeft(2:11,8:13) = 0;
    leftEYE_2_5_lookLeft(2:11,14:20) = 0.7;
    leftEYE_2_5_lookLeft = imgaussfilt(leftEYE_2_5_lookLeft,1);
%--------------------------------------------------------------------------    
    leftEYE_2_6_lookStraight = flip(rightEYE_2_6_lookStraight,2);
    leftEYE_2_6_lookRight = leftEYE_2_6_lookStraight;
    leftEYE_2_6_lookRight(2:12,13:19) = 0;
    leftEYE_2_6_lookRight(2:12,7:12) = 0.7;
    leftEYE_2_6_lookRight = imgaussfilt(leftEYE_2_6_lookRight,1);
    leftEYE_2_6_lookLeft = leftEYE_2_6_lookStraight;
    leftEYE_2_6_lookLeft(3:12,8:15) = 0;
    leftEYE_2_6_lookLeft(3:12,15:20) = 0.7;
    leftEYE_2_6_lookLeft = imgaussfilt(leftEYE_2_6_lookLeft,1);
%--------------------------------------------------------------------------    
    leftEYE_2_7_lookStraight = flip(rightEYE_2_7_lookStraight,2);
    leftEYE_2_7_lookRight = leftEYE_2_7_lookStraight;
    leftEYE_2_7_lookRight(2:13,12:19) = 0;
    leftEYE_2_7_lookRight(2:13,5:11) = 0.7;
    leftEYE_2_7_lookRight = imgaussfilt(leftEYE_2_7_lookRight,1);
    leftEYE_2_7_lookLeft = leftEYE_2_7_lookStraight;
    leftEYE_2_7_lookLeft(3:13,8:15) = 0;
    leftEYE_2_7_lookLeft(3:13,16:22) = 0.7;
    leftEYE_2_7_lookLeft = imgaussfilt(leftEYE_2_7_lookLeft,1);
    
%% check templates
% figure();imshow(rightEYE_3_0_lookStraight);
% figure();imshow(rightEYE_2_1_lookStraight);
% figure();imshow(rightEYE_2_2_lookStraight);
% figure();imshow(rightEYE_2_3_lookStraight);
% figure();imshow(rightEYE_2_4_lookStraight);
% figure();imshow(rightEYE_2_5_lookStraight);
% figure();imshow(rightEYE_2_6_lookStraight);
% figure();imshow(rightEYE_2_7_lookStraight);
% 
% figure();imshow(rightEYE_3_0_lookRight);
% figure();imshow(rightEYE_2_1_lookRight);
% figure();imshow(rightEYE_2_2_lookRight);
% figure();imshow(rightEYE_2_3_lookRight);
% figure();imshow(rightEYE_2_4_lookRight);
% figure();imshow(rightEYE_2_5_lookRight);
% figure();imshow(rightEYE_2_6_lookRight);
% figure();imshow(rightEYE_2_7_lookRight);
% 
% figure();imshow(rightEYE_3_0_lookLeft);
% figure();imshow(rightEYE_2_1_lookLeft);
% figure();imshow(rightEYE_2_2_lookLeft);
% figure();imshow(rightEYE_2_3_lookLeft);
% figure();imshow(rightEYE_2_4_lookLeft);
% figure();imshow(rightEYE_2_5_lookLeft);
% figure();imshow(rightEYE_2_6_lookLeft);
% figure();imshow(rightEYE_2_7_lookLeft);
% 
% %--------------------------------------------------------------------------
% 
% figure();imshow(leftEYE_3_0_lookStraight);
% figure();imshow(leftEYE_2_1_lookStraight);
% figure();imshow(leftEYE_2_2_lookStraight);
% figure();imshow(leftEYE_2_3_lookStraight);
% figure();imshow(leftEYE_2_4_lookStraight);
% figure();imshow(leftEYE_2_5_lookStraight);
% figure();imshow(leftEYE_2_6_lookStraight);
% figure();imshow(leftEYE_2_7_lookStraight);
% 
% figure();imshow(leftEYE_3_0_lookRight);
% figure();imshow(leftEYE_2_1_lookRight);
% figure();imshow(leftEYE_2_2_lookRight);
% figure();imshow(leftEYE_2_3_lookRight);
% figure();imshow(leftEYE_2_4_lookRight);
% figure();imshow(leftEYE_2_5_lookRight);
% figure();imshow(leftEYE_2_6_lookRight);
% figure();imshow(leftEYE_2_7_lookRight);
% 
% figure();imshow(leftEYE_3_0_lookLeft);
% figure();imshow(leftEYE_2_1_lookLeft);
% figure();imshow(leftEYE_2_2_lookLeft);
% figure();imshow(leftEYE_2_3_lookLeft);
% figure();imshow(leftEYE_2_4_lookLeft);
% figure();imshow(leftEYE_2_5_lookLeft);
% figure();imshow(leftEYE_2_6_lookLeft);
% figure();imshow(leftEYE_2_7_lookLeft);

end

