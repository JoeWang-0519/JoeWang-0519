clear all;
clc;
% since my student ID is A0236307J, then I need to choose GROUP1!!
% data pre-process
% first, load the images
ext = {'*.jpeg', '*.jpg', '*.png'};

path1 = '/Users/wangjiangyi/Desktop/group_1/automobile/';
path2 = '/Users/wangjiangyi/Desktop/group_1/dog/';
%load manmade objects
images = [];
for i = 1 : length(ext)
    images = [images dir([path1 ext{i}])];
end

for i = 1 : length(images)
    img = imread([path1, images(i).name]);
    img_gray = rgb2gray(img);
    img_graycol = reshape(img_gray, [1024,1]);
    image_all(:,i) = double(img_graycol);
end
%load animals
images = [];
for i = 1 : length(ext)
    images = [images dir([path2 ext{i}])];
end

for i = 1 : length(images)
    img = imread([path2, images(i).name]);
    img_gray = rgb2gray(img);
    img_graycol = reshape(img_gray, [1024,1]);
    image_all(:,i+500) = double(img_graycol);
end

target_all = [zeros(1, 500), ones(1, 500)];

%save datasample
%save datasample_256


