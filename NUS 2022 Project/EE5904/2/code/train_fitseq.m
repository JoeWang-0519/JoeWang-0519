% MLP training sequentially
function [net, accu_train, accu_val] = train_fitseq(n, images, labels, train_num, val_num, epochs)
    % Construct a 1-n-1 MLP and conduct sequential mode:
    %
    % Args: 
    % n: the number of hidden neurons
    % images: matrix of input( dimension * image_num)
    % labels: lebel of each iamge
    % train_num: number of training set
    % val_num: number of validation set
    % epochs: number of epoch
    %
    % Return:
    % net: trained network
    % accu_train: performance of training set (epochs * 1)
    % accu_val: perfomance of validation set (epochs * 1)

    images_seq = num2cell(images, 1);
    labels_seq = num2cell(labels, 1);

    % set the NN
    net = fitnet(n);

    net.divideFcn = 'dividetrain'; %all samples are used to train models
    net.performParam.regularization = 0; % no regularization
    net.trainFcn = 'traingd'; %use (Gradient Descent) Backpropagation
    %net.trainParam.epochs =epochs;

    accu_train = zeros(epochs, 1);
    accu_val = zeros(epochs, 1);

    % train the NN sequentially
    for i = 1 : epochs
        display(['Epoch: ', num2str(i), '  Hidden Layer: ', num2str(n)]);

        idx = randperm( train_num ); % shuffle the list, which represents the training sequence
        % NOTE: the difference between ADAPT & TRAIN
        % ADAPT FOR THE ONLINE(SEQUENTIAL) LEARNING;
        % TRAIN FOR THE BATCH MODE LEARNING
        net = adapt(net, images_seq(:, idx), labels_seq(:, idx));

        pred_train = net(images(: , 1:train_num ));
        accu_train(i) = mean( abs( pred_train - labels(1 : train_num) ) );

        if (val_num == 0)
            accu_val(i) = 0;
        else
            pred_val = net(images(:, (train_num+1): end));
            accu_val(i) = mean( abs( pred_val - labels((train_num+1) : end) ) );
        end
    end
end

    







