%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [] = runVideo(video, audio, Fs, videoName, isRandom, folderName)
%% 1
    th = 'th5';
    filter = 'mean';
    bufferSize = '1-15';
    shift = 'shift0';
    msg = sprintf('%s_%s_%s_%s_%s\n',videoName, th, filter, bufferSize, shift);
    fprintf('%s:\n',msg);
    [correctScreenSection1, ~, statisticsMat1, successNum, VJ_ErrorNum, TM_ErrorNum, goodFrameNum1]...
        = eyeTracker(video, audio, Fs, filter, bufferSize, shift, isRandom);
    
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\correctScreenSection1', folderName),'correctScreenSection1');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\statisticsMat1', folderName),'statisticsMat1');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\goodFrameNum1', folderName),'goodFrameNum1');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\successNum', folderName),'successNum');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\VJ_ErrorNum', folderName),'VJ_ErrorNum');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\TM_ErrorNum', folderName),'TM_ErrorNum');
    
%     sendMail(videoName, th, filter, bufferSize, shift);

%% 2
    th = 'th5';
    filter = 'mean';
    bufferSize = '1-15';
    shift = 'shift5';
    msg = sprintf('%s_%s_%s_%s_%s\n',videoName, th, filter, bufferSize, shift);
    fprintf('%s:\n',msg);
    [correctScreenSection2, ~, statisticsMat2, ~, ~, ~, goodFrameNum2]...
        = eyeTracker(video, audio, Fs, filter, bufferSize, shift, isRandom);

    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\correctScreenSection2', folderName),'correctScreenSection2');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\statisticsMat2', folderName),'statisticsMat2');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\goodFrameNum2', folderName),'goodFrameNum2');

%     sendMail(videoName, th, filter, bufferSize, shift);
 
%% 3
    th = 'th5';
    filter = 'mean';
    bufferSize = '1-15';
    shift = 'shift10';
    msg = sprintf('%s_%s_%s_%s_%s\n',videoName, th, filter, bufferSize, shift);
    fprintf('%s:\n',msg);
    [correctScreenSection3, ~, statisticsMat3, ~, ~, ~, goodFrameNum3]...
        = eyeTracker(video, audio, Fs, filter, bufferSize, shift, isRandom);

    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\correctScreenSection3', folderName),'correctScreenSection3');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\statisticsMat3', folderName),'statisticsMat3');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\goodFrameNum3', folderName),'goodFrameNum3');

%     sendMail(videoName, th, filter, bufferSize, shift);
 
%% 4
    th = 'th5';
    filter = 'median';
    bufferSize = '1-15';
    shift = 'shift0';
    msg = sprintf('%s_%s_%s_%s_%s\n',videoName, th, filter, bufferSize, shift);
    fprintf('%s:\n',msg);
    [correctScreenSection4, ~, statisticsMat4, ~, ~, ~, goodFrameNum4]...
        = eyeTracker(video, audio, Fs, filter, bufferSize, shift, isRandom);
    
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\correctScreenSection4', folderName),'correctScreenSection4');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\statisticsMat4', folderName),'statisticsMat4');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\goodFrameNum4', folderName),'goodFrameNum4');

%     sendMail(videoName, th, filter, bufferSize, shift);
 
%% 5
    th = 'th5';
    filter = 'median';
    bufferSize = '1-15';
    shift = 'shift5';
    msg = sprintf('%s_%s_%s_%s_%s\n',videoName, th, filter, bufferSize, shift);
    fprintf('%s:\n',msg);
    [correctScreenSection5, ~, statisticsMat5, ~, ~, ~, goodFrameNum5]...
        = eyeTracker(video, audio, Fs, filter, bufferSize, shift, isRandom);

    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\correctScreenSection5', folderName),'correctScreenSection5');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\statisticsMat5', folderName),'statisticsMat5');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\goodFrameNum5', folderName),'goodFrameNum5');

%     sendMail(videoName, th, filter, bufferSize, shift);

%% 6
    th = 'th5';
    filter = 'median';
    bufferSize = '1-15';
    shift = 'shift10';
    msg = sprintf('%s_%s_%s_%s_%s\n',videoName, th, filter, bufferSize, shift);
    fprintf('%s:\n',msg);
    [correctScreenSection6, ~, statisticsMat6, ~, ~, ~, goodFrameNum6]...
        = eyeTracker(video, audio, Fs, filter, bufferSize, shift, isRandom);

    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\correctScreenSection6', folderName),'correctScreenSection6');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\statisticsMat6', folderName),'statisticsMat6');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\goodFrameNum6', folderName),'goodFrameNum6');

%     sendMail(videoName, th, filter, bufferSize, shift);

%% 7
    th = 'th5';
    filter = 'mean';
    bufferSize = '5-11';
    shift = 'shift0';
    msg = sprintf('%s_%s_%s_%s_%s\n',videoName, th, filter, bufferSize, shift);
    fprintf('%s:\n',msg);
    [correctScreenSection7, ~, statisticsMat7, ~, ~, ~, goodFrameNum7]...
        = eyeTracker(video, audio, Fs, filter, bufferSize, shift, isRandom);
    
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\correctScreenSection7', folderName),'correctScreenSection7');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\statisticsMat7', folderName),'statisticsMat7');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\goodFrameNum7', folderName),'goodFrameNum7');

%     sendMail(videoName, th, filter, bufferSize, shift);
 
%% 8
    th = 'th5';
    filter = 'median';
    bufferSize = '5-11';
    shift = 'shift0';
    msg = sprintf('%s_%s_%s_%s_%s\n',videoName, th, filter, bufferSize, shift);
    fprintf('%s:\n',msg);
    [correctScreenSection8, ~, statisticsMat8, ~, ~, ~, goodFrameNum8]...
        = eyeTracker(video, audio, Fs, filter, bufferSize, shift, isRandom);
    
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\correctScreenSection8', folderName),'correctScreenSection8');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\statisticsMat8', folderName),'statisticsMat8');
    save(sprintf('C:\\Users\\tom-avi\\Desktop\\projectA_v8\\outputs\\%s\\goodFrameNum8', folderName),'goodFrameNum8');

%     sendMail(videoName, th, filter, bufferSize, shift);

%%
    sendMail(videoName, [], [], [], []);
end

