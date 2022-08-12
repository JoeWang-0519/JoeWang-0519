clear all;
clc;

load datasample.mat

% since the activation function is logistic function, we set the target as follows:
% 0.2->0 (manmade objects)
% 0.8->1 (dog)

% target is the 0-1 target
target = target_all;
% target all is the 0.2-0.8 target
target_all = [0.2*ones(1,500), 0.8*ones(1,500)];


% split the training and validation set
train_image = image_all(:, [1:450, 501:950]);
val_image = image_all(:, [451:500, 951:1000]);

train_target = target_all([1:450, 501:950]);
val_target = target_all([451:500, 951:1000]);

t_target = target([1:450, 501:950]);
v_target = target([451:500, 951:1000]);

% we apply the normalization on the row vector
mu1 = mean(train_image, 2);
s1 = std(train_image, 0, 2);
for i = 1:1024
    train_image_norm1(i,:) = (train_image(i,:) - mu1(i)) / s1(i);
    val_image_norm1(i,:) = (val_image(i,:) - mu1(i)) / s1(i);
end



h_initial = 300;
threshold = 0.95;

svd_record = [];
svd_dim = [h_initial];
while true
    % Baseline
    net = patternnet(h_initial);
    % for pattern recognition, we try 'trainrp'
    net.trainFcn = 'trainrp';
    net.trainParam.epochs = 400;
    net.divideFcn = 'dividetrain';
    net.performParam.regularization = 0;
    
    net = train(net, train_image_norm1, train_target);
    w = net.IW{1};
    b = net.b{1};
    H = zeros(900, 300);
    for i = 1 : 900
        for j = 1 : h_initial
            H(i,j) = tansig(w(j,:)*train_image_norm1(:,i)+b(j));
        end
    end
    
    singular_value = svd(H);
    svd_record = [svd_record, singular_value];
    % effective: desired hidden neurons
    effctive = sv_reduction(H, threshold, h_initial);
    if (effctive == h_initial)
        break;
    else
        h_initial = effctive;
        svd_dim = [svd_dim, h_initial];
    end
end

figure(1);
for i = 1:9
    subplot(3,3,i);
    dim = svd_dim(i);
    dim_next = svd_dim(i+1);
    y_svd = svd_record(1:dim , i);
    bar(y_svd);
    hold on,
    plot([dim_next, dim_next], [0, y_svd(1)], 'k', 'linewidth', 2);
    set(gca,'YLim',[0 y_svd(1)]);
    title(['number of hidden neurons: ', num2str(dim)])
end
