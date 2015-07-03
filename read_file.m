clear all; close all; clc; 

%A = h5read('field_space.h5', '/ey_100'); 

A = h5read('structure.h5', '/MaterialMap'); 

%A = h5read('field_space_wide.h5', '/ex_1200'); 
xrange = [-1.5 1.5]; 
yrange = [-1.8 1.8]; 
zrange = [0 1]; 

figure; 
visreal(permute(A(31, :, :), [3 2 1]), xrange, yrange);

% visreal(permute(A(:, 20, :), [3 1 2]), xrange, yrange);

% visreal(A(:, :, 21), zrange, yrange);

% csvread('field_time_center.dat'); 


% [time_value hz ex ey] = csvimport('field_time_center.xlsx', 'columns', {'time_value1', 'hz1', 'ex1', 'ey1'}); 
% load 'field_time_center.dat'; 
delimiterIn = ' ';
headerlinesIn = 1;
% B = importdata('field_time_center.dat', delimiterIn, headerlinesIn); 

%% 
% B = importdata('field_time_center_ref1.dat'); 
% 
% time = B.data(:, 1); 
% hz = B.data(:, 2); 
% ex = B.data(:, 3); 
% ey = B.data(:, 4); 
% 
% % load field_time.xlsx
% 
% % xrange = [0 20]; 
% % yrange = [0 408]; 
% % visreal(permute(A(1, :, :), [3 2 1]), xrange, yrange); 
% 
% % import('field_time_center.dat'); 
% 
% figure; 
% plot(time, ey)