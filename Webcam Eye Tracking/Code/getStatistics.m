%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ successPercent1, successPercent2, successPercentPlusMinusOne1, successPercentPlusMinusOne2 ] = getStatistics( output, expectedOutputMat )
%%
    output(size(expectedOutputMat,1)+1:end,:) = [];
    isCorrectVec = zeros(length(output),2);
    isCorrectVecPlusMinusOne = zeros(length(output),2);
   
%%
    for i=1 : size(expectedOutputMat,1)
        for j=1 : size(expectedOutputMat,2)
            if (output(i,2) == expectedOutputMat(i,j))
                isCorrectVec(i,2) = 1;
            end
            if (output(i,1) == expectedOutputMat(i,j))
                isCorrectVec(i,1) = 1;
            end
        end
    end
    successPercent1 = mean(isCorrectVec(:,2))*100;
    successPercent2 = mean(isCorrectVec(:,1))*100;
 
%%
    for i=1 : size(expectedOutputMat,1)
        for j=1 : size(expectedOutputMat,2)
            privious = output(i,2)-1;
            if (privious == 0)
                privious = 10;
            end
            next = output(i,2)+1;
            if (next == 11)
                next = 1;
            end
            if (output(i,2) == expectedOutputMat(i,j) || privious == expectedOutputMat(i,j) || next == expectedOutputMat(i,j))
                isCorrectVecPlusMinusOne(i,2) = 1;
            end
            privious = output(i,1)-1;
            if (privious == 0)
                privious = 10;
            end
            next = output(i,1)+1;
            if (next == 11)
                next = 1;
            end
            if (output(i,1) == expectedOutputMat(i,j) || privious == expectedOutputMat(i,j) || next == expectedOutputMat(i,j))
                isCorrectVecPlusMinusOne(i,1) = 1;
            end
        end
    end
    
    successPercentPlusMinusOne1 = mean(isCorrectVecPlusMinusOne(:,2))*100;
    successPercentPlusMinusOne2 = mean(isCorrectVecPlusMinusOne(:,1))*100;
    
end

