function Kmu_update = RecalKmu(reassign_matrix, X_train, Kmu)

% Parameter:
% reassign_matrix: K * N matrix, the (i,j)-th element represents:
%       if value = 0, then not assign
%       if value = 1, then assign (x_j to mu_i)
% X_train: D * N matrix, training sample;
% Kmu: old version; D * K matrix

% Reurn:
% Kmu_update: K centroids vector; D * K matrix

[D, N] = size(X_train);
[K, ~] = size(reassign_matrix);
Kmu_update = zeros(D, K);
for i = 1 : K
    sum = zeros(D,1);
    count = 0;
    for j = 1 : N
        if reassign_matrix(i,j) == 1
            sum = sum + X_train(:,j);
            count = count + 1;
        end
    end
    if count == 0
        Kmu_update(:, i) = Kmu(:, i);
    else
        Kmu_update(:, i) = sum / count;
    end
end



