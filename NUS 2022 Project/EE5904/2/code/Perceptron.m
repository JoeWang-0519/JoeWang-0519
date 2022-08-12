function w = Perceptron(X, y, eta, epoch)

% Perception Learning Algorithm
% Args:
% X: each column is one image (dim * number)
% y: target (1 * number), either 0 or 1
% eta: learning rate
% epoch: number of epoch
% Return:
% w: learnt weights
[dim, num] = size(X);  
X = [ones(1,num);
    X];  
w = zeros(1, dim+1);  

for step = 1: epoch
    flag = true;
    for index = 1 : num
        err_signal = y(index) - sign(w * X(:,index));
        if err_signal ~= 0
            flag = false;  
            w = w + eta * err_signal .* X(:, index)';
        end  
    end  
    if flag == true  
        break;  
    end  
end  