%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [correctScreenSection, correctScreenSectionNEW, statisticsMat, successNum, VJ_ErrorNum, TM_ErrorNum, goodFrameNum] = eyeTracker( video, audio, Fs, filter, bufferSize, shift, isRandom )   
%%  
    [video, ~] = videosPreProcess(video, audio, Fs); 

%% initialized global variables
    quantizationNum = 10;
    
    correctScreenSection1 = [];
    correctScreenSection2 = [];
    avgGrayLevelLookRightVec1 = [];
    avgGrayLevelLookRightVec2 = [];
    avgGrayLevelLookLeftVec1 = [];
    avgGrayLevelLookLeftVec2 = [];
    avgGrayLevelVec1 = [];
    avgGrayLevelVec2 = [];
    xLookRightVec1 = [];
    yLookRightVec1 = [];
    rLookRightVec1 = [];
    xLookRightVec2 = [];
    yLookRightVec2 = [];
    rLookRightVec2 = [];
    xLookLeftVec1 = [];
    yLookLeftVec1 = [];
    rLookLeftVec1 = [];
    xLookLeftVec2 = [];
    yLookLeftVec2 = [];
    rLookLeftVec2 = [];
    xVec1 = [];
    yVec1 = [];
    rVec1 = [];
    xVec2 = [];
    yVec2 = [];
    rVec2 = [];

    frameNum = 0;
    bufferCnt = 0;
    goofFrameNum1 = 0;
    goofFrameNum2 = 0;
    analizeClibratingFlag = true;
    successNum = 0;
    VJ_ErrorNum = 0;
    TM_ErrorNum1 = 0;
    TM_ErrorNum2 = 0;
    shiftNumber = 0;
    if (strcmp(shift,'shift5'))
        shiftNumber = 5;
    elseif (strcmp(shift,'shift10'))
        shiftNumber = 10;
    end
    startBuffer = 1;
    endBuffer = 15;
    if (strcmp(bufferSize,'5-11'))
        startBuffer = 5;
        endBuffer = 11;
    end
    if (isRandom == false)
        endFrame = 1860;
    else
        endFrame = 1260;
    end

%%
    disp("FREAME NUMBER:");
    while hasFrame(video)
        
%% ======================== preparing needed frames and skip not needed ones ========================

        frameNum = frameNum + 1;
        fprintf('%d\n',frameNum);

        pic = flip(readFrame(video),2); % needed because the camera pictured with flip

        if (frameNum >= 1 && frameNum <= 150) % frame skip 0-5 sec (look straight)
            continue;
        end

        if (frameNum > 180 && frameNum <= 240) %frame skip 6-8 sec
            continue;
        end

        if (frameNum > 270 && frameNum <= 300) %frame skip 9-10 sec
            continue;
        end
        
        if (frameNum > endFrame) %frame skip 62-end sec
            continue;
        end
        
%% ======================== V & J ========================
        [EYE1,EYE2,VJ_Error,faceBox,xNoseFinal,yNoseFinal] = faceEyesNoseBoxDetect(pic); 
        if (VJ_Error ~= 0) % for statistics
            VJ_ErrorNum = VJ_ErrorNum + 1;
        end
        if (VJ_Error == 0)
            Face=im2double(rgb2gray(imcrop(pic,faceBox)));
            if (EYE1(1) < EYE2(1))% correct the side of each eye
               tmp = EYE2;
               EYE2 = EYE1;
               EYE1 = tmp;
            end   
%% ======================== prepare eye1_im (right eye) ========================
            eye1_im_rgb = (imcrop(pic,EYE1));

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

%% ======================== prepare eye2_im (left eye) ========================
            eye2_im_rgb = (imcrop(pic,EYE2));

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

%% ======================== Template Matching ========================
            [~, ~, ~, ~, eye1_im_1, eye1_im_1_original, ~, eye1_im_1_backOffsetA, eye1_im_1_backOffsetB, TM_Error1] = templateMatching1(eye1_im_3, eye1_im_3_original, eye1_im_2, eye1_im_2_original, eye1_im_1, eye1_im_1_original, eye1_im_rgb);
            [~, ~, ~, ~, eye2_im_1, eye2_im_1_original, ~, eye2_im_1_backOffsetA, eye2_im_1_backOffsetB, TM_Error2] = templateMatching2(eye2_im_3, eye2_im_3_original, eye2_im_2, eye2_im_2_original, eye2_im_1, eye2_im_1_original, eye2_im_rgb);
            if (TM_Error1 ~= 0) % for statistics
                TM_ErrorNum1 = TM_ErrorNum1 + 1;
            end
            if (TM_Error2 ~= 0) % for statistics
                TM_ErrorNum2 = TM_ErrorNum2 + 1;
            end

%% ======================== find iris ========================
            Rmin = 5;
            Rmax = 25;
            low_pass_disk = fspecial('disk',1);

%                    ====== iris 1 ======        
            [centersDark_eye1, radiiDark_eye1] = imfindcircles(eye1_im_1_original,[Rmin Rmax],'ObjectPolarity','dark','sensitivity',0.89);
            widthpic1=size(eye1_im_1,2);
            flag1 = ((length(radiiDark_eye1)==1) && ((centersDark_eye1(1,1)<0.28*widthpic1) || (centersDark_eye1(1,1)>0.68*widthpic1)));
            if ( (isempty(radiiDark_eye1)) || (flag1) )
                eye1_im_1 = imadjust(eye1_im_1,stretchlim(eye1_im_1),[]);
                eye1_im_1 = imsharpen(eye1_im_1);
                eye1_im_1 = imadjust(eye1_im_1,stretchlim(eye1_im_1),[]);
                eye1_im_1 = imfilter(eye1_im_1, low_pass_disk); 
                eye1_im_1 = imadjust(eye1_im_1,stretchlim(eye1_im_1),[]);

                [centersDark_eye1, radiiDark_eye1] = imfindcircles(eye1_im_1,[Rmin Rmax],'ObjectPolarity','dark','sensitivity',0.95);
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
                    if ( (S1<min1) && (centersDark_eye1(j,1)>0.28*widthpic1) && (centersDark_eye1(j,1)<0.68*widthpic1) )
                        min1 = S1;
                        ii1 = j;
                    end
                end
                centersDark_eye1 = centersDark_eye1(ii1,:);
                radiiDark_eye1 = radiiDark_eye1(ii1);
            end

%                    ====== iris 2 ======         
            [centersDark_eye2, radiiDark_eye2] = imfindcircles(eye2_im_1_original,[Rmin Rmax],'ObjectPolarity','dark','sensitivity',0.89);
            widthpic2=size(eye2_im_1,2);
            flag2 = ((length(radiiDark_eye2)==1) && ((centersDark_eye2(1,1)<0.28*widthpic2) || (centersDark_eye2(1,1)>0.68*widthpic2)));
            if ( (isempty(radiiDark_eye2)) || (flag2) )
                eye2_im_1 = imadjust(eye2_im_1,stretchlim(eye1_im_1),[]);
                eye2_im_1 = imsharpen(eye2_im_1);
                eye2_im_1 = imadjust(eye2_im_1,stretchlim(eye2_im_1),[]);
                eye2_im_1 = imfilter(eye2_im_1, low_pass_disk); 
                eye2_im_1 = imadjust(eye2_im_1,stretchlim(eye2_im_1),[]);

                [centersDark_eye2, radiiDark_eye2] = imfindcircles(eye2_im_1,[Rmin Rmax],'ObjectPolarity','dark','sensitivity',0.95);
            end 
            if (length(radiiDark_eye2)>1)
                min2 = 10;
                ii2=1;
                for j = 1:length(radiiDark_eye2)
                    widthpic2=size(eye2_im_1,2);
                    xOffset2 = centersDark_eye2(j,1)-round(radiiDark_eye2(j)/2);
                    yOffset2 = centersDark_eye2(j,2)-round(radiiDark_eye2(j)/2);
                    width2 = 2*radiiDark_eye2(j);
                    height2 = 2*radiiDark_eye2(j);
                    tmp2 = imcrop(eye2_im_1_original,[xOffset2,yOffset2,width2,height2]);
                    S2 = sum(sum(tmp2))./(size(tmp2,1).*size(tmp2,2));
                    if ( (S2<min2) && (centersDark_eye2(j,1)>0.28*widthpic2) && (centersDark_eye2(j,1)<0.68*widthpic2)) 
                        min2 = S2;
                        ii2 = j;
                    end
                end
                centersDark_eye2 = centersDark_eye2(ii2,:);
                radiiDark_eye2 = radiiDark_eye2(ii2);
            end 

%% ======================== clculate iris location in the face ========================
            xFace_eye1_im_1 = [];
            yFace_eye1_im_1 = [];
            rFace_eye1_im_1 = [];
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

            xFace_eye2_im_1 = [];
            yFace_eye2_im_1 = [];
            rFace_eye2_im_1 = [];
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
        end

%% ======================== calculate direction in the screen (including frame plot for debugging) ========================
%                    ================ calibrating frames ================          
        if (frameNum > 150 && frameNum <= 180) % 5-6 sec (look right)
%                    ====== create frame buffers ======
            if (VJ_Error == 0)
                if (~isempty(rFace_eye1_im_1))
                    [xLookRightVec1, yLookRightVec1, rLookRightVec1, avgGrayLevelLookRightVec1]...
                        = createRightEyeFrameBuffer(xLookRightVec1, yLookRightVec1, rLookRightVec1, avgGrayLevelLookRightVec1,...
                                             xFace_eye1_im_1, yFace_eye1_im_1, rFace_eye1_im_1,...
                                             xNoseFinal, yNoseFinal,...
                                             Face, frameNum);
                end
                if (~isempty(rFace_eye2_im_1))
                    [xLookRightVec2, yLookRightVec2, rLookRightVec2, avgGrayLevelLookRightVec2]...
                        = createLeftEyeFrameBuffer(xLookRightVec2, yLookRightVec2, rLookRightVec2, avgGrayLevelLookRightVec2,...
                                             xFace_eye2_im_1, yFace_eye2_im_1, rFace_eye2_im_1,...
                                             xNoseFinal, yNoseFinal,...
                                             Face, frameNum);
                end
%                    ====== plot (debugging) ======          
%                     figure(frameNum);
%                     imshow(Face);
%                     hold on;
%                      if (~isempty(rFace_eye1_im_1))
%                         viscircles([xFace_eye1_im_1, yFace_eye1_im_1], rFace_eye1_im_1,'Color','b');
%                         hold on;
%                         plot(xFace_eye1_im_1,yFace_eye1_im_1,'+b');
%                     end
%                     hold on;
%                     if (~isempty(rFace_eye2_im_1))
%                         viscircles([xFace_eye2_im_1, yFace_eye2_im_1], rFace_eye2_im_1,'Color','b');
%                         hold on;
%                         plot(xFace_eye2_im_1,yFace_eye2_im_1,'+b');
%                     end
%                     hold on;
%                     plot(xNoseFinal,yNoseFinal,'+b');
%                     impixelinfo;
            end
        elseif (frameNum > 240 && frameNum <= 270) % 8-9 sec (look left)
%                    ====== create frame buffers ====== 
            if (VJ_Error == 0)
                if (~isempty(rFace_eye1_im_1))
                    [xLookLeftVec1, yLookLeftVec1, rLookLeftVec1, avgGrayLevelLookLeftVec1]...
                        = createRightEyeFrameBuffer(xLookLeftVec1, yLookLeftVec1, rLookLeftVec1, avgGrayLevelLookLeftVec1,...
                                            xFace_eye1_im_1, yFace_eye1_im_1, rFace_eye1_im_1,...
                                            xNoseFinal, yNoseFinal,...
                                            Face, frameNum);
                end
                if (~isempty(rFace_eye2_im_1))
                    [xLookLeftVec2, yLookLeftVec2, rLookLeftVec2, avgGrayLevelLookLeftVec2]...
                        = createLeftEyeFrameBuffer(xLookLeftVec2, yLookLeftVec2, rLookLeftVec2, avgGrayLevelLookLeftVec2,...
                                            xFace_eye2_im_1, yFace_eye2_im_1, rFace_eye2_im_1,...
                                            xNoseFinal, yNoseFinal,...
                                            Face, frameNum);
                end            
%                    ====== plot (debugging) ======
%                     figure(frameNum);
%                     imshow(Face);
%                     hold on;
%                      if (~isempty(rFace_eye1_im_1))
%                         viscircles([xFace_eye1_im_1, yFace_eye1_im_1], rFace_eye1_im_1,'Color','b');
%                         hold on;
%                         plot(xFace_eye1_im_1,yFace_eye1_im_1,'+b');
%                     end
%                     hold on;
%                     if (~isempty(rFace_eye2_im_1))
%                         viscircles([xFace_eye2_im_1, yFace_eye2_im_1], rFace_eye2_im_1,'Color','b');
%                         hold on;
%                         plot(xFace_eye2_im_1,yFace_eye2_im_1,'+b');
%                     end
%                     hold on;
%                     plot(xNoseFinal,yNoseFinal,'+b');
%                     impixelinfo;        
            end
        elseif (frameNum > 300 + shiftNumber && frameNum <= endFrame) % 10-(endFrame/30) sec
            bufferCnt = bufferCnt + 1;
            if (VJ_Error == 0)
                if (analizeClibratingFlag == true)
                    
%                    ====== analize look right frames ======  
                    [xLookRightVec1, yLookRightVec1, rLookRightVec1, xfinalLookRight1, yfinalLookRight1, grayScaleThreshold1]...
                        = frameBufferAnalyze(xLookRightVec1, yLookRightVec1, rLookRightVec1, avgGrayLevelLookRightVec1, -1, true, filter);

                    [xLookRightVec2, yLookRightVec2, rLookRightVec2, xfinalLookRight2, yfinalLookRight2, grayScaleThreshold2]...
                        = frameBufferAnalyze(xLookRightVec2, yLookRightVec2, rLookRightVec2, avgGrayLevelLookRightVec2, -1, true, filter);

%                    ====== analize look left frames ======       
                    [xLookLeftVec1, yLookLeftVec1, rLookLeftVec1, xfinalLookLeft1, yfinalLookLeft1, grayScaleThreshold1]...
                        = frameBufferAnalyze(xLookLeftVec1, yLookLeftVec1, rLookLeftVec1, avgGrayLevelLookLeftVec1, grayScaleThreshold1, true, filter);

                    [xLookLeftVec2, yLookLeftVec2, rLookLeftVec2, xfinalLookLeft2, yfinalLookLeft2, grayScaleThreshold2]...
                        = frameBufferAnalyze(xLookLeftVec2, yLookLeftVec2, rLookLeftVec2, avgGrayLevelLookLeftVec2, grayScaleThreshold2, true, filter);
                    analizeClibratingFlag = false;
                end

%                    ================ non calibrating frames ================    
%                    ====== create frame buffers ======
%                    ====== take frames withput overlap ======
                if (bufferCnt >= startBuffer && bufferCnt <= endBuffer) 
                    if (~isempty(rFace_eye1_im_1))
                        [xVec1, yVec1, rVec1, avgGrayLevelVec1]...
                            = createRightEyeFrameBuffer(xVec1, yVec1, rVec1, avgGrayLevelVec1,...
                                                xFace_eye1_im_1, yFace_eye1_im_1, rFace_eye1_im_1,...
                                                xNoseFinal, yNoseFinal,...
                                                Face, frameNum);
                    end
                    if (~isempty(rFace_eye2_im_1))
                        [xVec2, yVec2, rVec2, avgGrayLevelVec2]...
                            = createLeftEyeFrameBuffer(xVec2, yVec2, rVec2, avgGrayLevelVec2,...
                                                xFace_eye2_im_1, yFace_eye2_im_1, rFace_eye2_im_1,...
                                                xNoseFinal, yNoseFinal,...
                                                Face, frameNum);
                    end
                end

%                    ====== plot (debugging) ======
%                     figure(frameNum);
%                     imshow(Face);
%                     hold on;
%                      if (~isempty(rFace_eye1_im_1))
%                         viscircles([xFace_eye1_im_1, yFace_eye1_im_1], rFace_eye1_im_1,'Color','b');
%                         hold on;
%                         plot(xFace_eye1_im_1,yFace_eye1_im_1,'+b');
%                     end
%                     hold on;
%                     if (~isempty(rFace_eye2_im_1))
%                         viscircles([xFace_eye2_im_1, yFace_eye2_im_1], rFace_eye2_im_1,'Color','b');
%                         hold on;
%                         plot(xFace_eye2_im_1,yFace_eye2_im_1,'+b');
%                     end
%                     hold on;
%                     plot(xNoseFinal + xfinalLookLeft1, yNoseFinal - yfinalLookLeft1, '+r');
%                     hold on;
%                     plot(xNoseFinal + xfinalLookRight1, yNoseFinal - yfinalLookRight1, '+r');
%                     hold on;
%                     plot(xNoseFinal - xfinalLookLeft2, yNoseFinal - yfinalLookLeft2, '+r');
%                     hold on;
%                     plot(xNoseFinal - xfinalLookRight2, yNoseFinal - yfinalLookRight2, '+r');
%                     hold on;
%                     plot(xNoseFinal, yNoseFinal,'+b');
%                     impixelinfo;
            end

%                    ====== analyze frame buffer, analyze every 0.5 sec (15 frames) ======           
            if (bufferCnt == 15)
                bufferCnt = 0;
                if(~isempty(xVec1))
                    [xVec1, yVec1, rVec1, xfinal1, yfinal1, grayScaleThreshold1]...
                        = frameBufferAnalyze(xVec1, yVec1, rVec1, avgGrayLevelVec1, grayScaleThreshold1, false, filter);
                end
                if(~isempty(xVec2))
                    [xVec2, yVec2, rVec2, xfinal2, yfinal2, grayScaleThreshold2]...
                        = frameBufferAnalyze(xVec2, yVec2, rVec2, avgGrayLevelVec2, grayScaleThreshold2, false, filter);
                end
                goofFrameNum1 = goofFrameNum1 + size(xVec1,1);
                goofFrameNum2 = goofFrameNum2 + size(xVec2,1);
                
%                    ====== calculate direction in the screen ======      
                if(~isempty(xVec1))
                    correctScreenSection1 = [correctScreenSection1 ; getDirection1(quantizationNum,...
                                                                                 xfinalLookLeft1, xfinalLookRight1,...
                                                                                 xfinal1)];                                                               
                else
                    correctScreenSection1 = [correctScreenSection1 ; -3];
                end
                if(~isempty(xVec2))
                    correctScreenSection2 = [correctScreenSection2 ; getDirection2(quantizationNum,...
                                                                                 xfinalLookLeft2, xfinalLookRight2,...
                                                                                 xfinal2)];
                else
                    correctScreenSection2 = [correctScreenSection2 ; -3];
                end
%                    ====== reset frame buffers ======           
                xVec1 = [];
                yVec1 = [];
                rVec1 = [];
                xVec2 = [];
                yVec2 = [];
                rVec2 = [];
                avgGrayLevelVec1 = [];
                avgGrayLevelVec2 = [];
            end                                       
        end
        if (VJ_Error == 0 && TM_Error1 == 0 && TM_Error2 == 0) % for statistics
            successNum = successNum + 1;
        end
    end

    correctScreenSection = [correctScreenSection2  correctScreenSection1];
    goodFrameNum = [goofFrameNum2 goofFrameNum1];
    TM_ErrorNum = [TM_ErrorNum2 TM_ErrorNum1];

%%
    correctScreenSectionNEW = getDirectionIrregularValuesHandler (correctScreenSection);
    if (isRandom == false)
        statisticsMat = analizeOutput(correctScreenSectionNEW);
    else
        statisticsMat = analizeOutputR(correctScreenSectionNEW);
    end

%%
%     load handel
%     sound(y,Fs);

end

