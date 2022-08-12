function [recall, precision, accuracy] = perf_meas(predict, target)
    % calculate TP FP FN TN
    % TP: target=1 err_sig=0
    % FP: target=1 err_sig=-1
    % TN: target=0 err_sig=0
    % FN: target=0 err_sig=1
    TP = 0;
    FP = 0;
    TN = 0;
    FN = 0;

    err_signal = predict - target;

    for j = 1 : length(target)
        if err_signal(j) == -1
            FP = FP + 1;
        elseif err_signal(j) == 1
            FN = FN + 1;
        elseif target(j)==1
            TP = TP + 1;
        elseif target(j)==0
            TN = TN + 1;
        end
    end
    recall = TP / (TP + FP);
    precision = TP / (TP + FN);
    accuracy = 1 - mean(abs(err_signal));
    
end