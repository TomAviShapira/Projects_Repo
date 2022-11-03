%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ correctScreenSection ] = getDirection2(quantizationNum,...
                                                  xLookLeft, xLookRight,...
                                                  x)
    xLookLeft = xLookLeft - xLookRight;
    x = x - xLookRight;
    xLookRight = 0;
    
    sectionInd = -3; % that value meanning nothing due to lines 22-29
                     % at the end sectionInd will be alwayse one of this:
                     % [-1 , -2 , [1 quantizationNum]]
    
    sectionLen =  xLookLeft / quantizationNum;
    xStart = xLookLeft;
    xFinel = xStart - sectionLen;
    for i = 1:quantizationNum
        if (x-0.0001 <= xStart && x >= xFinel-0.0001)
            sectionInd = i;
            break;
        end
        xStart = xFinel;
        xFinel = xStart - sectionLen;
    end
    
     if (sectionInd == -3)
         if (abs(x-xLookLeft) < abs(x-xLookRight))
             sectionInd = -1;
         else
             sectionInd = -2;
         end
        disp("getDirection2 : FAIL");
     end

    correctScreenSection = sectionInd;
end

