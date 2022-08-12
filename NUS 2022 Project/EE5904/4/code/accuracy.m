function acc = accuracy(label, prediction)
% parameter:
% label: the ground truth label;    size: num * 1
% prediction: the prediction;       size: num * 1

% output:
% accuracy: correct num / total num

[num, ~] = size(label);
count = 0;
for i = 1 : num
    agreement = label(i) * prediction(i);
    if agreement >= 0
        count = count + 1;
    end
end

acc = count / num;