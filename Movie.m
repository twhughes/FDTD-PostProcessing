clear all; close all; clc; 
cd '~/Documents/Fan/FDTD_PLUS/';        %cd to the directory where the files are

%%
%define parameters

sweep = 'space';                        %sweep 'space' or 'time'
filename = 'field_space_wide2.h5';      %field plots file name
structFile = 'structure.h5';            %structure file name
axis = 2;                               %{0,1,2} = {x,y,z}
time = 2400;                            %time step (if doing space sweep) (must be present in field_space.h5)
position = 40;                          %index of plane along axis (if doing time sweep)
field = 'ex';                           %field component to look at
delay = 0.1;                            %movie frame delay time (sec)

%%
%get the structure

B = double(h5read(structFile, '/MaterialMap')); 
figure(1);
%for i = (1:80)
%    xrange = [-1.5 1.5]; 
%    yrange = [-1.8 1.8]; 
%    visreal(permute(B(:,i,:), [3 1 2]), xrange, yrange);
%    pause(0.5)
%end
%clf


%%
%
%get the dataset names and time parameters

info = h5info(filename);                %get info for field plots file
dsets = info.Datasets;                  %get an array of the datasets ey_500, hz_750, ...etc
tpoints = [];                           %time points list (to be stripped from dataset name
fields  = [];                           %field values

for i = (1:length(dsets))
    name = dsets(i).Name;               %get dataset name
    C = strsplit(name, '_');            %strip into field and timestep
    timeStep = C(2);                    %get time step
    tpoints = [tpoints, timeStep];      %append to time step list
    for j = (1:length(fields))
        display(C(1));
        if (strcmp(fields(j), C(1)))
            fields = [fields, C(1)];
        end
    end
end

%clear unused variables
clear name
clear timeStep
clear i
clear C

%
%%
%if you know the info and want it to run faster, just use this array
tpoints = (2400:80:4800);
fields = ['ex','ey','ez'];

%%
figure(1);
figHandle = figure(1);
set(figHandle, 'Position', [100, 100, 1049, 895]);

if (strcmp(sweep,'space'))
    dataset = strcat('/',field,'_',num2str(time));
    A = h5read(filename, dataset); 
    xrange = [-1.5 1.5]; 
    yrange = [-1.8 1.8]; 
    zrange = [0 1]; 

    [X,Y,Z] = size(A);
    sizes = [X Y Z];
    numPoints = sizes(axis+1);
    for i = (1:numPoints)
         if (axis == 2)
            subplot(2,1,1)
            visreal(permute(A(i, :, :), [3 2 1]), xrange, yrange);
            xlabel('x');
            ylabel('y');
            title(strcat('Field=', ': z = ', num2str(i), ' (unit cells)'));
            subplot(2,1,2)
            visreal(permute(B(i, :, :), [3 2 1]), xrange, yrange);
            %hold off;
            xlabel('x');
            ylabel('y');
            title(strcat('Structure: z = ', num2str(i), ' (unit cells)'));
         elseif (axis == 1)
            visreal(permute(A(:, i, :), [3 1 2]), xrange, yrange);
            xlabel('x');
            ylabel('z');
         elseif (axis == 0)
            visreal(permute(A(:, :, i), [1 2 3]), xrange, yrange);
            xlabel('z');
            ylabel('y');
         end
         pause(delay)
    end
    
elseif (strcmp(sweep,'time'))
    for t = tpoints
        filename = strcat('/',field,'_',num2str(t));
        A = h5read('field_space_wide2.h5', filename); 
        xrange = [-1.5 1.5]; 
        yrange = [-1.8 1.8]; 
        zrange = [0 1]; 

        [X,Y,Z] = size(A);
        sizes = [X Y Z];
        if (axis == 2)
            visreal(permute(A(position, :, :), [3 2 1]), xrange, yrange);
            xlabel('x');
            ylabel('y');
        elseif (axis == 1)
            visreal(permute(A(:, position, :), [3 1 2]), xrange, yrange);
            xlabel('x');
            ylabel('z');
        elseif (axis == 0)
            visreal(permute(A(:, :, position), [1 2 3]), xrange, yrange);
            xlabel('z');
            ylabel('y');
        end
        pause(delay)
    end
end

%A = h5read('field_space_wide.h5', '/ex_1200');
%%
%visreal(permute(A(31, :, :), [3 2 1]), xrange, yrange);

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