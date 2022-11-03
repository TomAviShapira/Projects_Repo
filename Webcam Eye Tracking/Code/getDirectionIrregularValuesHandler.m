%%
% Tom-Avi Shapira
% Lital Yakobov

%%
function [ correctOutput ] = getDirectionIrregularValuesHandler ( output )
%% correct -3 (empth buffer)
    % correct if both eyes are -3
    output1 = output(:,2);
    output2 = output(:,1);
    ind1 = find(output1 == -3);
    ind2 = find(output2 == -3);
    ind = [];
    for i1=1 : length(ind1)
        for i2=1 : length(ind2)
            if (ind1(i1) == ind2(i2))
                ind = [ind ind1(i1)];
            end
        end
    end
    for i=1 : length(ind)
        if (ind(i) == 1) % the first analize
            output1(ind(i)) = 1;
            output2(ind(i)) = 1;
        elseif (ind(i) == size(output,1)) % the last analize
            output1(ind(i)) = 10;
            output2(ind(i)) = 10;
        else
            % assume there are no 2 following lines that both eyes are -3
            output1(ind(i)) = round((output1(ind(i)+1) + output1(ind(i)-1))/2);
            output2(ind(i)) = round((output2(ind(i)+1) + output2(ind(i)-1))/2);
        end
    end
    
    % correct if only one eye is -3
    ind1 = find(output1 == -3);
    if (~isempty(ind1))
        
        output1(ind1) =  output2(ind1);
        
    end
    ind2 = find(output2 == -3);
    if (~isempty(ind2))
        output2(ind2) =  output1(ind2);
    end
%% correct -1 (actually look to section 1)
    ind1 = find(output1 == -1);
    ind2 = find(output2 == -1);
    
    % correct output1 according to output2
    for i=1 : length(ind1)
        if (output2(ind1(i)) > 0)
            output1(ind1(i)) = output2(ind1(i));
        else
             output1(ind1(i)) = 1;
             output2(ind1(i)) = 1;
        end
    end
    % correct output2 according to output1
    for i=1 : length(ind2)
        if (output1(ind2(i)) > 0)
            output2(ind2(i)) = output1(ind2(i));
        end
    end

%% correct -2 (actually look to section 10)
    ind1 = find(output1 == -2);
    ind2 = find(output2 == -2);
    
    % correct output1 according to output2
    for i=1 : length(ind1)
        if (output2(ind1(i)) > 0)
            output1(ind1(i)) = output2(ind1(i));
        else
             output1(ind1(i)) = 10;
             output2(ind1(i)) = 10;
        end
    end
    % correct output2 according to output1
    for i=1 : length(ind2)
        if (output1(ind2(i)) > 0)
            output2(ind2(i)) = output1(ind2(i));
        end
    end
    
%%
    correctOutput = [output2 output1];
end

