function reassign_matrix = Reassign(SqD_matrix)

% parameter
% SqD_matrix: K * N matrix, the (i,j)-th element represents the distance
% between x_j and mu_i

% return
% reassign_matrix: K * N matrix, the (i,j)-th element represents:
%       if value = 0, then not assign
%       if value = 1, then assign (x_j to mu_i)
[K, N] = size(SqD_matrix);
reassign_matrix = zeros(K, N);

% find the minima index
[~, minidx] = min(SqD_matrix, [], 1);   % 1 * N matrix

% expensive way
for i = 1 : N
    position = minidx(i);
    reassign_matrix(position, i) = 1;
end

% cheap way
%position_vector = 1 : N;
%idx_vector = N * (minidx-1) + position_vector;
%reassign_matrix(idx_vector) = 1;
end




