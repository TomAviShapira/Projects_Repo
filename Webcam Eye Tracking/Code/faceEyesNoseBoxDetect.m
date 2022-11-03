%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ EYE1,EYE2,Error,faceBox,xNoseFinal,yNoseFinal ] = faceEyesNoseBoxDetect( IMAGE )
    %%
    Error = 0;
    d = 0;
    EYE1 = -1;
    EYE2 = -1;
    faceBox = -1;
    xNoseFinal = -1;
    yNoseFinal = -1;
    
    %%
    pic=IMAGE; %image to be read 
    I=rgb2gray(pic);
    avg = sum(sum(I))./(size(I,1)*size(I,2));
    while (avg < 147)
        I(:,:) = I(:,:)+1;
        avg = sum(sum(I))./(size(I,1)*size(I,2));
    end
    faceDetect = vision.CascadeObjectDetector();
    eyeDetect = vision.CascadeObjectDetector('RightEye');
    noseDetect = vision.CascadeObjectDetector('Nose');

    facebox=faceDetect(I);

    if (isempty(facebox))
        Error = 1;
        disp('faceEyesNoseBoxDetect : FAIL (a face not found)');
    end

    if (Error == 0)
        for i=1:size(facebox,1)
            Face=imcrop(I,facebox(i,:));
            Face = imadjust(Face,stretchlim(Face),[]);
            FaceXwidth = size(Face,1);
            FaceYwidth = size(Face,2);
            deltaX = FaceXwidth/5;
            deltaY = FaceYwidth/18;
            Eyebox=eyeDetect(Face);
            nEyebox = size(Eyebox,1);

            if (nEyebox < 2) % 2 eyes not found in this specific "face"
                continue;
            end

            e=[];
            for it=1:nEyebox
                for j=1:nEyebox
                     if (j > it) 
                         if ((abs(Eyebox(j,2)-Eyebox(it,2))<deltaY)&& (abs(Eyebox(j,1)-Eyebox(it,1))>deltaX))
                             e(1,:)=Eyebox(it,:);
                             e(2,:)=Eyebox(j,:);
                             d = 1;
                             break;
                         end 
                     end
                 end
                 if(d == 1)
                     break;
                 end
            end
            if (d == 0)
                break;
            end
            Eyebox(1,:)=e(1,:);
            Eyebox(2,:)=e(2,:);
            c=Eyebox(1,3)/2;
            d=Eyebox(1,4)/2;
            eyeCenter1x=Eyebox(1,1)+c+facebox(i,1);
            eyeCenter1y=Eyebox(1,2)+d+facebox(i,2);
            e=Eyebox(2,3)/2;
            f=Eyebox(2,4)/2;
            eyeCenter2x=Eyebox(2,1)+e+facebox(i,1);
            eyeCenter2y=Eyebox(2,2)+f+facebox(i,2);
            faceBox = facebox(i,:);
            Face=imcrop(I,faceBox);
            noseBox = noseDetect(Face);        
            if (isempty(noseBox))
                Error = 1;
                disp('faceEyesNoseBoxDetect : FAIL (a nose not found)');
                continue;
            end
            xMidFace = size(Face,2)/2;
            yMidFace = size(Face,1)/2;
            distanceX = size(Face,2);
            distanceY = size(Face,1);
            for j=1:size(noseBox,1)
                xNose = noseBox(j,1)+noseBox(j,3)/2;
                yNose = noseBox(j,2)+noseBox(j,4)/2;
                if (abs(xNose-xMidFace) < distanceX)
                    xNoseFinal = xNose;
                    distanceX = abs(xNose-xMidFace);
                end
                if (abs(yNose-yMidFace) < distanceY)
                    yNoseFinal = yNose;
                    distanceY = abs(yNose-yMidFace);
                end
            end
            break; % new line
        end
    end

    if (d == 0)
        Error = 1;
        disp('faceEyesNoseBoxDetect : FAIL (2 eyes not found)'); % 2 eyes not found in all "faces" that recognaized
    end

    if (Error == 0)
        %disp('faceEyesNoseBoxDetect : COMPLETE'); 
        EYE1 = [eyeCenter1x-c eyeCenter1y-d Eyebox(1,3) Eyebox(1,4)];
        EYE2 = [eyeCenter2x-e eyeCenter2y-f Eyebox(2,3) Eyebox(2,4)];
    end



end

