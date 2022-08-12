clear all;
clc;
load Digits.mat
% Since my student ID is: A0236307J, I should omit class 2 and class 3;

trainIdx = find(train_classlabel==0 | train_classlabel==1 | train_classlabel==4); 
testIdx = find(test_classlabel==0 | test_classlabel==1 | test_classlabel==4); 
% find the location of classes 0, 1, 4
Train_ClassLabel = train_classlabel(trainIdx);
Train_Data = train_data(:,trainIdx);
Test_ClassLabel = test_classlabel(testIdx);
Test_Data = test_data(:,testIdx);


%save Digits_modify.mat
