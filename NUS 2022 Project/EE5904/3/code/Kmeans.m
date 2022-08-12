% Kmeans algorithm
function [record_centroids] = Kmeans(X_train, K)

% Parameter:
% X_train: training sample; dimension * number of training sample
% K: number of centroids

% Return:
% record_centroids: the centroids of Kmeans algorithm; dimension * number
% of centroids

[dim, ~] = size(X_train);
% find the range for each dimension
X_minmax = zeros(dim, 2);
for i = 1 : dim
    maxima = max(X_train(i,:));
    minima = min(X_train(i,:));
    X_minmax(i,:) = [minima, maxima];
end

% initialization
Kmu = zeros(dim, K);
for i = 1 : dim
    mini = X_minmax(i,1);
    maxi = X_minmax(i,2);
    Kmu(i,:) = mini+ (maxi-mini) * rand(1,K);
end

max_iteration = 1000;

for iter = 1 : max_iteration
    % calculate the distance between data sample and each centroid
    SqD_matrix = CalcSqDistance(X_train, Kmu); % K * N
    
    % determine the reassignment after calculating the centroid
    reassign_matrix = Reassign(SqD_matrix);

    Kmu_update = RecalKmu(reassign_matrix, X_train, Kmu); % D * K matrix

    if sum(abs(Kmu_update(:)-Kmu(:))) < 1e-6
        disp(iter);
        break
    else
        Kmu = Kmu_update;
    end
end

record_centroids = Kmu;

end


