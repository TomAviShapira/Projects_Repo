%%
% Tom-Avi Shapira
% Lital Yakobov

%%
clear all;
close all;
clc;
warning off;

%%
correctScreenSection1 = [];
correctScreenSection2 = [];
for i=1:5
    pic=imread(sprintf('imagesALLdirection/%d.png',i));
    fprintf('IMAGE %d:\n',i);
    [EYE1,EYE2,Error,faceBox,xNoseFinal,yNoseFinal] = faceEyesNoseBoxDetect( pic );
    if (Error ~= 0)
        continue;
    end
    Face=im2double(rgb2gray(imcrop(pic,faceBox)));
    % correct the side of each eye
    if (EYE1(1) < EYE2(1))
       tmp = EYE2;
       EYE2 = EYE1;
       EYE1 = tmp;
    end
    
    % we found 2 eyes
    if (EYE1~=-1 & EYE2~=-1)    
        
%% eye1_im
        eye1_im_rgb = (imcrop(pic,EYE1));
%         eye1_im_1_rgb = imresize(eye1_im_rgb, [48,68]);
        
        eye1_im_1 = rgb2gray(eye1_im_rgb); 
        eye1_im_1 = im2double(eye1_im_1);
        eye1_im_1_originalSize = size(eye1_im_1);
        eye1_im_1_newSize = [48,68];
        eye1_im_1 = imresize(eye1_im_1, eye1_im_1_newSize);
        eye1_im_1_original = eye1_im_1;

        eye1_im_2 = impyramid(eye1_im_1,'reduce');
        eye1_im_2_original = eye1_im_2;
        
        eye1_im_3 = impyramid(eye1_im_2,'reduce');
        eye1_im_3_original = eye1_im_3;
        
%% eye2_im
        eye2_im_rgb = (imcrop(pic,EYE2));
%         eye2_im_1_rgb = imresize(eye2_im_rgb, [48,68]);
        
        eye2_im_1 = rgb2gray(eye2_im_rgb); 
        eye2_im_1 = im2double(eye2_im_1);
        eye2_im_1_originalSize = size(eye2_im_rgb);
        eye2_im_1_newSize = [48,68];
        eye2_im_1 = imresize(eye2_im_1, eye2_im_1_newSize);
        eye2_im_1_original = eye2_im_1;

        eye2_im_2 = impyramid(eye2_im_1,'reduce');
        eye2_im_2_original = eye2_im_2;

        eye2_im_3 = impyramid(eye2_im_2,'reduce');
        eye2_im_3_original = eye2_im_3;
        
%% Template Matching
        [~, ~, ~, ~, eye1_im_1, eye1_im_1_original, ~, eye1_im_1_backOffsetA, eye1_im_1_backOffsetB] = templateMatching1(eye1_im_3, eye1_im_3_original, eye1_im_2, eye1_im_2_original, eye1_im_1, eye1_im_1_original, eye1_im_rgb);
        [~, ~, ~, ~, eye2_im_1, eye2_im_1_original, ~, eye2_im_1_backOffsetA, eye2_im_1_backOffsetB] = templateMatching2(eye2_im_3, eye2_im_3_original, eye2_im_2, eye2_im_2_original, eye2_im_1, eye2_im_1_original, eye2_im_rgb);
    
%% find circles
        Rmin = 5;
        Rmax = 25;
        low_pass_disk = fspecial('disk',1);
        
%% iris 1        
        [centersDark_eye1, radiiDark_eye1] = imfindcircles(eye1_im_1_original,[Rmin Rmax],'ObjectPolarity','dark','sensitivity',0.89);
        widthpic1=size(eye1_im_1,2);
        flag1 = ((length(radiiDark_eye1)==1) && ((centersDark_eye1(1,1)<0.28*widthpic1) || (centersDark_eye1(1,1)>0.68*widthpic1)));
        if ( (isempty(radiiDark_eye1)) || (flag1) )
            eye1_im_1 = imadjust(eye1_im_1,stretchlim(eye1_im_1),[]);
            eye1_im_1 = imsharpen(eye1_im_1);
            eye1_im_1 = imadjust(eye1_im_1,stretchlim(eye1_im_1),[]);
            eye1_im_1 = imfilter(eye1_im_1, low_pass_disk); 
            eye1_im_1 = imadjust(eye1_im_1,stretchlim(eye1_im_1),[]);

            [centersDark_eye1, radiiDark_eye1] = imfindcircles(eye1_im_1,[Rmin Rmax],'ObjectPolarity','dark','sensitivity',0.95); %0.94
        end      
        if (length(radiiDark_eye1)>1)
            min1 = 10;
            ii1=1;
            for j = 1:length(radiiDark_eye1)
                widthpic1=size(eye1_im_1,2);
                xOffset1 = centersDark_eye1(j,1)-round(radiiDark_eye1(j)/2);
                yOffset1 = centersDark_eye1(j,2)-round(radiiDark_eye1(j)/2);
                width1 = 2*radiiDark_eye1(j);
                height1 = 2*radiiDark_eye1(j);
                tmp1 = imcrop(eye1_im_1_original,[xOffset1,yOffset1,width1,height1]);
                S1 = sum(sum(tmp1))./(size(tmp1,1).*size(tmp1,2));
                if ( (S1<min1) && (centersDark_eye1(j,1)>0.28*widthpic1) && (centersDark_eye1(j,1)<0.68*widthpic1) ) %%%temp!
                    min1 = S1;
                    ii1 = j;
                end
            end
            centersDark_eye1 = centersDark_eye1(ii1,:);
            radiiDark_eye1 = radiiDark_eye1(ii1);
        end
        
%% iris 2        
        [centersDark_eye2, radiiDark_eye2] = imfindcircles(eye2_im_1_original,[Rmin Rmax],'ObjectPolarity','dark','sensitivity',0.89);
        widthpic2=size(eye2_im_1,2);
        flag2 = ((length(radiiDark_eye2)==1) && ((centersDark_eye2(1,1)<0.28*widthpic2) || (centersDark_eye2(1,1)>0.68*widthpic2)));
        if ( (isempty(radiiDark_eye2)) || (flag2) )
            eye2_im_1 = imadjust(eye2_im_1,stretchlim(eye1_im_1),[]);
            eye2_im_1 = imsharpen(eye2_im_1);
            eye2_im_1 = imadjust(eye2_im_1,stretchlim(eye2_im_1),[]);
            eye2_im_1 = imfilter(eye2_im_1, low_pass_disk); 
            eye2_im_1 = imadjust(eye2_im_1,stretchlim(eye2_im_1),[]);

            [centersDark_eye2, radiiDark_eye2] = imfindcircles(eye2_im_1,[Rmin Rmax],'ObjectPolarity','dark','sensitivity',0.95); %0.94 
        end 
        if (length(radiiDark_eye2)>1)
            min2 = 10;
            ii2=1;
            for j = 1:length(radiiDark_eye2)
                widthpic2=size(eye2_im_1,2); %%temp!
                xOffset2 = centersDark_eye2(j,1)-round(radiiDark_eye2(j)/2);
                yOffset2 = centersDark_eye2(j,2)-round(radiiDark_eye2(j)/2);
                width2 = 2*radiiDark_eye2(j);
                height2 = 2*radiiDark_eye2(j);
                tmp2 = imcrop(eye2_im_1_original,[xOffset2,yOffset2,width2,height2]);
                S2 = sum(sum(tmp2))./(size(tmp2,1).*size(tmp2,2));
                if ( (S2<min2) && (centersDark_eye2(j,1)>0.28*widthpic2) && (centersDark_eye2(j,1)<0.68*widthpic2)) %%%temp!
                    min2 = S2;
                    ii2 = j;
                end
            end
            centersDark_eye2 = centersDark_eye2(ii2,:);
            radiiDark_eye2 = radiiDark_eye2(ii2);
        end
        
%% imcrop due to the radius of each iris
%         if (~isempty(radiiDark_eye1))
%             eye1_im_1_original = imcrop(eye1_im_1_original,[1,centersDark_eye1(2)-radiiDark_eye1,size(eye1_im_1_original,2),2*radiiDark_eye1]);
%             centersDark_eye1(2) = radiiDark_eye1;
%             [eye1_im_1, ~] = eyeContrastStretching(eye1_im_1_original, centersDark_eye1, radiiDark_eye1);
%         end
%         if (~isempty(radiiDark_eye2))
%             eye2_im_1_original = imcrop(eye2_im_1_original,[1,centersDark_eye2(2)-radiiDark_eye2,size(eye2_im_1_original,2),2*radiiDark_eye2]);
%             centersDark_eye2(2) = radiiDark_eye2;
%             [eye2_im_1, ~] = eyeContrastStretching(eye2_im_1_original, centersDark_eye2, radiiDark_eye2);
%         end   
    
%% plot eyes with iris detection
%         figure();
%         subplot(1,2,2);imshow(eye1_im_1_original);
%         hold on;
%         viscircles(centersDark_eye1, radiiDark_eye1,'Color','b');
%         hold on;
%         if (~isempty(radiiDark_eye1))
%             hold on;plot(centersDark_eye1(1),centersDark_eye1(2),'+b');
%         end
%         subplot(1,2,1);imshow(eye2_im_1_original);
%         hold on;
%         viscircles(centersDark_eye2, radiiDark_eye2,'Color','b');
%         hold on;
%         if (~isempty(radiiDark_eye2))
%             hold on;plot(centersDark_eye2(1),centersDark_eye2(2),'+b');
%         end
%         impixelinfo; 
    
%% clculate iris location in the face
        if (~isempty(radiiDark_eye1))
            eye1_im_1_xFactor = eye1_im_1_originalSize(2)/eye1_im_1_newSize(2);
            xFace_eye1_im_1 = centersDark_eye1(1) * eye1_im_1_xFactor;
            xFace_eye1_im_1 = xFace_eye1_im_1 + EYE1(1) - faceBox(1);
            eye1_im_1_yFactor = eye1_im_1_originalSize(1)/eye1_im_1_newSize(1);
            yFace_eye1_im_1 = eye1_im_1_backOffsetA + eye1_im_1_backOffsetB + centersDark_eye1(2);
            yFace_eye1_im_1 = yFace_eye1_im_1 * eye1_im_1_yFactor;
            yFace_eye1_im_1 = yFace_eye1_im_1 + EYE1(2) - faceBox(2);
            rFace_eye1_im_1 = radiiDark_eye1 * (eye1_im_1_xFactor+eye1_im_1_yFactor)/2;
        end
        
        if (~isempty(radiiDark_eye2))
            eye2_im_1_xFactor = eye2_im_1_originalSize(2)/eye2_im_1_newSize(2);
            xFace_eye2_im_1 = centersDark_eye2(1) * eye2_im_1_xFactor;
            xFace_eye2_im_1 = xFace_eye2_im_1 + EYE2(1) - faceBox(1);
            eye2_im_1_yFactor = eye2_im_1_originalSize(1)/eye2_im_1_newSize(1);
            yFace_eye2_im_1 = eye2_im_1_backOffsetA + eye2_im_1_backOffsetB + centersDark_eye2(2);
            yFace_eye2_im_1 = yFace_eye2_im_1 * eye2_im_1_yFactor;
            yFace_eye2_im_1 = yFace_eye2_im_1 + EYE2(2) - faceBox(2);
            rFace_eye2_im_1 = radiiDark_eye2 * (eye2_im_1_xFactor+eye2_im_1_yFactor)/2;
        end
        
%% plot face with iris detection        
%         figure();
%         imshow(Face);
%         hold on;
%          if (~isempty(radiiDark_eye1))
%             viscircles([xFace_eye1_im_1, yFace_eye1_im_1], rFace_eye1_im_1,'Color','g');
%             hold on;
%             plot(xFace_eye1_im_1,yFace_eye1_im_1,'+g');
%         end
%         hold on;
%         if (~isempty(radiiDark_eye2))
%             viscircles([xFace_eye2_im_1, yFace_eye2_im_1], rFace_eye2_im_1,'Color','g');
%             hold on;
%             plot(xFace_eye2_im_1,yFace_eye2_im_1,'+g');
%         end

%% calculate direction in the screen
        if (mod(i,5) == 1) % look left (calibration) 
            correctScreenSection1 = [correctScreenSection1];
            correctScreenSection2 = [correctScreenSection2];
            xLookLeft1 = xFace_eye1_im_1 - xNoseFinal;
            xLookLeft2 =  xNoseFinal - xFace_eye2_im_1;
        elseif (mod(i,5) == 2) % look right (calibration)
            xLookRight1 = xFace_eye1_im_1 - xNoseFinal;
            xLookRight2 = xNoseFinal - xFace_eye2_im_1;
        else % not calibration anymore
            quantizationNum = 5;
            correctScreenSection1 = [correctScreenSection1 ; getDirection1(quantizationNum,...
                                                                         xLookLeft1, xLookRight1,...
                                                                         xFace_eye1_im_1 - xNoseFinal)];                                                               
            
            correctScreenSection2 = [correctScreenSection2 ; getDirection2(quantizationNum,...
                                                                         xLookLeft2, xLookRight2,...
                                                                         xNoseFinal - xFace_eye2_im_1)];                                                                  
 % plot face with iris location and calibration              
            figure();
            imshow(Face);
            hold on;
             if (~isempty(radiiDark_eye1))
                viscircles([xFace_eye1_im_1, yFace_eye1_im_1], rFace_eye1_im_1,'Color','g');
                hold on;
                plot(xFace_eye1_im_1,yFace_eye1_im_1,'+g');
            end
            hold on;
            if (~isempty(radiiDark_eye2))
                viscircles([xFace_eye2_im_1, yFace_eye2_im_1], rFace_eye2_im_1,'Color','g');
                hold on;
                plot(xFace_eye2_im_1,yFace_eye2_im_1,'+g');
            end
            hold on;
            plot(xLookLeft1 + xNoseFinal,yFace_eye1_im_1,'+r');
            hold on;
            plot(xLookRight1 + xNoseFinal,yFace_eye1_im_1,'+r');
            hold on;
            plot(xNoseFinal - xLookLeft2,yFace_eye2_im_1,'+r');
            hold on;
            plot(xNoseFinal - xLookRight2,yFace_eye2_im_1,'+r');
            hold on;
            plot(xNoseFinal,yNoseFinal,'+g');
            impixelinfo;    
        end  
        
    end
    disp(' ');
end
correctScreenSection = [correctScreenSection2  correctScreenSection1];

