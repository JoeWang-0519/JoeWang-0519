% MLP training sequentially (pattern recognition)
function [net, accu_train, accu_val, A_train, P_train, R_train, A_val, P_val, R_val] = train_prseq(n, images, val_image_norm1, labels, t_target, v_target, train_num, epochs)
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
    total_num = length(labels);

    images_seq = num2cell(images, 1);
    labels_seq = num2cell(labels, 1);

    % set the NN
    net = patternnet(n);

    net.divideFcn = 'dividetrain'; %all samples are used to train models
    net.performParam.regularization = 0.2; % no regularization
    net.trainFcn = 'trainbr'; %use 'trainrp' function to train patternnet
    net.trainParam.epochs = epochs;

    accu_train = zeros(epochs, 1);
    accu_val = zeros(epochs, 1);

    % train the NN sequentially
    for i = 1 : epochs
        display(['Epoch: ', num2str(i), '  Hidden Layer: ', num2str(n)]);
        

        % shuffle the list, which represents the training sequence
        % idx = randperm( train_num ); 
        disorder = randperm(total_num);
        train_idx = disorder(1 : train_num);

        test_idx = setdiff(disorder, train_idx);


        % a better choice of idx
        
        
        % NOTE: the difference between ADAPT & TRAIN
        % ADAPT FOR THE ONLINE(SEQUENTIAL) LEARNING
        % TRAIN FOR THE BATCH MODE LEARNING

        net = adapt(net, images_seq(:, train_idx), labels_seq(:, train_idx));

        pred_train = net(images(: , train_idx ));
        accu_train(i) = 1 - mean(abs(pred_train - labels(train_idx)));

        pred_val = round(net(images(: , test_idx))); 
        accu_val(i) = 1 - mean(abs(pred_val - labels(test_idx)));
        
        pred_train = round(net(images));
        pred_val = round(net(val_image_norm1));

        [recall_train, precision_train, accu_train1] = perf_meas(pred_train, t_target);
        R_train(i) = recall_train;
        P_train(i) = precision_train;
        A_train(i) = accu_train1;
            
        [recall_val, precision_val, accu_val1] = perf_meas(pred_val, v_target);
        R_val(i) = recall_val;
        P_val(i) = precision_val;
        A_val(i) = accu_val1;
    end
end

    







