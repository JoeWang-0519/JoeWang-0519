function data_predict = predict_wbias(data, weight, centroid, std)

% parameter:
% data: dimension * number of data
% weight: 1 * number of centroid + 1; the first term is BIAS
% centroid: dimension * number of centorid
% std: the width of RBF;

% return:
% data_predict: 1 * number of data
[~, K] = size(centroid);

data_predict = weight(1) + predict_wobias(data, weight(2:K+1), centroid, std);
end

