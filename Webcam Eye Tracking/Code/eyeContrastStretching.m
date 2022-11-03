%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ new_image, new_centersDark_eye ] = eyeContrastStretching( image, centersDark_eye, radiiDark_eye )
%%
    leftPart = imcrop(image,[1,1,floor(centersDark_eye(1)-radiiDark_eye)-1,size(image,1)]);
    middlePart = imcrop(image,[floor(centersDark_eye(1)-radiiDark_eye),1,floor(2*radiiDark_eye),size(image,1)]);
    rightPart = imcrop(image,[floor(centersDark_eye(1)+radiiDark_eye)+1,1,size(image,2),size(image,1)]);

%%    
    leftPart = imadjust(leftPart,stretchlim(leftPart),[]);
    rightPart = imadjust(rightPart,stretchlim(rightPart),[]);
    
%     leftPart = histeq(leftPart);
%     rightPart = histeq(rightPart);

%%
    new_image = [leftPart middlePart rightPart];
    new_image = imresize(new_image,[size(new_image,1),68]);
    new_centersDark_eye = [];
%%
%     figure();
%     imshow(new_image);

end

