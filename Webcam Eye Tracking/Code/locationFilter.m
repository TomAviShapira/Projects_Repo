%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ indVec ] = locationFilter( vec )
    threshold = 5;
    indVec = [];
    flag = 1;
    for i=2 : length(vec)
        if (abs(vec(i) - vec(i-1)) > threshold && flag == i)
            indVec = [indVec i];
            flag = i+2;
            continue;
        end
        flag = i+1;
    end
    indVec = indVec';
end

