function data_predict = predict_wobias(data, weight, centroid, std)

% parameter:
% data: dimension * number of data
% weight: 1 * number of centroid;
% centroid: dimension * number of centorid
% std: the width of RBF;

% return:
% data_predict: 1 * number of data
[~, N] = size(data);
[~, K] = size(centroid);

data_predict = zeros(1, N);
for i = 1 : N
    testdata = data(:, i);
    % calculate the distance between test sample and each centroid
    distance_vector = zeros(1, K);
    for j = 1: K
        distance_vector(j) = norm(testdata - centroid(:, j));
    end
    RBF_vector = exp(-distance_vector.^2/(2*std^2));
    data_predict(i) = weight * RBF_vector';
end
end

