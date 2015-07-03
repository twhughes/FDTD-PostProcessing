clear all; close all; clc; 
cd '~/Documents/Fan/FDTD_PLUS/';        % cd to the directory where the files are
addpath(genpath('~/Documents/Fan/filesbrah'));

%% 
% define parameters

sweep = 'space';                         % sweep 'space' or 'time'
filename = 'field_space_wide2.h5';      % field plots file name
structFile = 'structure.h5';            % structure file name
axis = 2;                               % {0,1,2} = {x,y,z}
time = 2400;                            % time step (if doing space sweep) (must be present in field_space.h5)
position = 40;                          % index of plane along axis (if doing time sweep)
delay = 0.01;                           % movie frame delay time (sec)
xrange = [-1.5 1.5];                    % xrange in your simulation
yrange = [-1.5 1.5];                    % yrange in your simulation
zrange = [-1.5 1.5];                    % zrange in your simulation

%% 
% get the structure

B = double(h5read(structFile, '/MaterialMap')); 

%% 
% get the dataset names and time parameters (comment out if fields
% {ex,ey,hz, ...} and times {100, 120, 130, ...} are known and enter in block below

info = h5info(filename);                % get info for field plots file
dsets = info.Datasets;                  % get an array of the datasets ey_500, hz_750, ...etc
tpoints = {};                           % time points list (to be stripped from dataset name
fields  = {};                           % field values

for i = (1:length(dsets))
    name = dsets(i).Name;               % get dataset name
    C = strsplit(name, '_');            % strip into field and timestep
    tpoints(i) = C(2);      % append to time step list
    fields(i) = C(1);                   % make a cell array of field names
end

fields = unique(fields);                % make the field name array unique
% clear unused variables
clear name
clear i
clear C

%% 

%{
% if you know the info and want it to run faster, just use these arrays and
% comment out above block
tpoints = (2400:80:4800);
fields = {'ex','ey','hz'};
%}

%% 
% plot the fields

% open a figure and make it large
figure(1);
figHandle = figure(1);
set(figHandle, 'Position', [100, 100, 1049, 895]);

% for spacial sweeps
if (strcmp(sweep,'space'))
    
    % make a cell array of the fields for each ex, ey, hz, etc
    As = {};                                            
    for f = (1:length(fields))
        field = fields{f};
        dataset = strcat('/',field,'_',num2str(time));
        A = h5read(filename, dataset);
        As{f} = A;
    end
    
    % get sizes (take first A for convenience)
    [X,  Y,  Z] = size(As{1});
    [Xb, Yb, Zb] = size(B);
    sizes  = [X  Y  Z];
    bSizes = [Xb Yb Zb];
    numPoints = sizes(axis+1);
    bScale = bSizes(axis+1)/numPoints;
    
    % iterate through planes in the axis you choose
    for i = (1:numPoints)
        
        % z axis
        if (axis == 2)
            
            % vis A for each field component and put each in subplot
            for j = (1:length(fields))
                field = fields(j);
                A = As{j};
            
                subplot(2,2,j)
                visreal(permute(A(i, :, :), [3 2 1]), xrange, yrange);
                xlabel('x');
                ylabel('y');
                title(strcat('Field= ', field, ': z = ', num2str(i), ' (unit cells)'));
            end
            
            % plot the structure
            subplot(2,2,4)
            visreal(permute(B(floor(i*bScale), :, :), [3 2 1]), xrange, yrange);
            xlabel('x');
            ylabel('y');
            title(strcat('Structure: z = ', num2str(i), ' (unit cells)')); 
            
        % y axis
        elseif (axis == 1)
            
            % vis A for each field component and put each in subplot
            for j = (1:length(fields))
                field = fields(j);
                A = As{j};
                subplot(2,2,j)
                visreal(permute(A(:, i, :), [3 1 2]), xrange, yrange);
                xlabel('x');
                ylabel('z');            
                title(strcat('Field=', field, ': y = ', num2str(i), ' (unit cells)'));
            end
            
            % plot the structure            
            subplot(2,2,4)
            visreal(permute(B(:, floor(i*bScale), :), [3 1 2]), xrange, yrange);
            xlabel('x');
            ylabel('y');
            title(strcat('Structure: y = ', num2str(i), ' (unit cells)'));
            
        % x axis
        elseif (axis == 0)
            
            % vis A for each field component and put each in subplot            
            for j = (1:length(fields))
                field = fields(j);
                A = As{j};
                subplot(2,2,j)
                visreal(permute(A(:, :, i), [1 2 3]), xrange, yrange);
                xlabel('z');
                ylabel('y');
                title(strcat('Field=', field, ': x = ', num2str(i), ' (unit cells)'));
            end   

            % plot the structure            
            subplot(2,2,4)
            visreal(permute(B(:, :, floor(i*bScale)), [1 2 3]), xrange, yrange);
            xlabel('x');
            ylabel('y');
            title(strcat('Structure: y = ', num2str(i), ' (unit cells)'));
        end
        
        % delay the animation (probably not necessary bc code runs so slow)
        pause(delay)
    end
    
% plot temporal data
elseif (strcmp(sweep,'time'))

    % iterate through time steps
    for i = (1:length(tpoints))
        t = tpoints{i};
        
        % create the A cell array for this timestep
        As = {};
        for f = (1:length(fields))
            field = fields{f};
            dataset = strcat('/',field,'_',num2str(t));
            A = h5read(filename, dataset);
            As{f} = A;
        end
        
        % get sizes (take first A for convenience)
        [X,  Y,  Z] = size(As{1});
        [Xb, Yb, Zb] = size(B);
        sizes  = [X  Y  Z];
        bSizes = [Xb Yb Zb];
        numPoints = sizes(axis+1);
        bScale = bSizes(axis+1)/numPoints;
        
        % z axis
        if (axis == 2)
            
            % vis A for each field component and put each in subplot                        
            for j = (1:length(fields))
                field = fields(j);
                A = As{j};
                subplot(2,2,j)
                visreal(permute(A(position, :, :), [3 2 1]), xrange, yrange);
                xlabel('x');
                ylabel('y');
                title(strcat('Field=', field, '  ,  time = ', num2str(t)));
            end
            
            % plot the structure                        
            subplot(2,2,4)
            visreal(permute(B(floor(position*bScale), :, :), [3 2 1]), xrange, yrange);
            xlabel('x');
            ylabel('y');
            title(strcat('Structure: z axis  ,  time = ', num2str(t)));
            
        % y axis
        elseif (axis == 1)
            
            % vis A for each field component and put each in subplot                        
            for j = (1:length(fields))
                field = fields(j);
                A = As{j};
                subplot(2,2,j)
                visreal(permute(A(:, position, :), [3 1 2]), xrange, yrange);
                xlabel('x');
                ylabel('z');            
                title(strcat('Field=', field, '  ,  time = ', num2str(t)));
            end
            
            % plot the structure                        
            subplot(2,2,4)
            visreal(permute(B(:, floor(position*bScale), :), [3 1 2]), xrange, yrange);
            xlabel('x');
            ylabel('y');
            title(strcat('Structure: y axis  ,  time = ', num2str(t)));
            
        % x axis
        elseif (axis == 0)
            
            % vis A for each field component and put each in subplot                        
            for j = (1:length(fields))
                field = fields(j);
                A = As{j};
                subplot(2,2,j)
                visreal(permute(A(:, :, position), [1 2 3]), xrange, yrange);
                xlabel('z');
                ylabel('y');
                title(strcat('Field=', field, '  ,  time = ', num2str(t)));
            end   
            
            % plot the structure                        
            subplot(2,2,4)
            visreal(permute(B(:, :, floor(position*bScale)), [1 2 3]), xrange, yrange);
            xlabel('x');
            ylabel('y');
            title(strcat('Structure: x axis  ,  time = ', num2str(t)));
        end

        % delay the animation (probably not necessary bc code runs so slow)        
        pause(delay)
    end
end
