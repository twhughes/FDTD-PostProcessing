clear all; close all; clc

%%

eps0 = 8.854e-12;  % vacuum permittivity in farad/L0
mu0 = pi * 4e-7;  % vacuum permeability in henry/L0
c = 1/sqrt(eps0*mu0);  % speed of light in vacuum in L0/sec
L0 = 1e-8; 

B = importdata('~/Documents/Fan/FDTD_PLUS/signal_ref.dat'); 

time_ref = B.data(:, 1); 
% hz_ref = B.data(:, 2); 
% ex_ref = B.data(:, 3); 
 ey_ref = B.data(:, 4); 

clear B; 

%B = importdata('field_time_coupled2.dat'); 
%B = importdata('field_time_center_ref.dat'); 
B = importdata('~/Documents/Fan/FDTD_PLUS/signal5.dat'); 

time = B.data(:, 1); 
% hz = B.data(:, 2); 
% ex = B.data(:, 3); 
 ey2 = B.data(:, 4); 
ey = ey2;
%ey(000:end) = 0;
%% Zero-padding if necessary
%ey(200:end) = 0;
L1 = length(time_ref); 
L2 = length(time); 
if L1 < L2
    ex_ref(L1:L2) = 0; 
    ey_ref(L1:L2) = 0; 
    hz_ref(L1:L2) = 0; 
end

%% Plot Ez with respect to time
% time = [1:length(Ez_ring_small)] * ht; 
time = time / c * L0; 
ht = time(2)-time(1); 

figure(1);
figHandle = figure(1);
set(figHandle, 'Position', [100, 100, 1049, 895]);
subplot(2,2,1);
plot(time*1e15, ey_ref); 
xlabel('Time (fs)'); ylabel('Ey(t)'); 
title('Ey without device');
set(gca,'FontSize',15,'fontWeight','bold')
set(findall(gcf,'type','text'),'FontSize',15,'fontWeight','bold')
subplot(2,2,2);
plot(time*1e15, ey); 
xlabel('Time (fs)'); ylabel('Ey(t)'); 
title('Ey with device'); 
set(gca,'FontSize',15,'fontWeight','bold')
set(findall(gcf,'type','text'),'FontSize',15,'fontWeight','bold')
%% Perform Fourier transform to obtain frequency spectrum

[Ex_ref_freq, freq] = Fourier_Normalized(ey_ref, ht); 
Ex_freq = Fourier_Normalized(ey, ht); 
wvlens = c./freq*1e9; 

%% Plot the reference spectrum

subplot(2,2,3);
plot(wvlens, abs(Ex_ref_freq), 'k'); 
axis([10 5000 0 max(abs(Ex_ref_freq))])
xlabel('Wavelength (nm)'); ylabel('Source'); 
title('Source Spectrum');
set(gca,'FontSize',15,'fontWeight','bold')
set(findall(gcf,'type','text'),'FontSize',15,'fontWeight','bold')
%% Grab the range from the spectral plot
lowIndex = 10;
highIndex = 5000;
cutoff = max(abs(Ex_ref_freq))/100;
for i = (1:length(Ex_ref_freq)-1)
    if ((abs(Ex_ref_freq(i)) < cutoff) && (abs(Ex_ref_freq(i+1)) > cutoff))
        lowIndex = i;
    elseif ((abs(Ex_ref_freq(i)) > cutoff) && (abs(Ex_ref_freq(i+1)) < cutoff))
        highIndex = i;
    end
end
upperWvl = wvlens(lowIndex);
lowerWvl = wvlens(highIndex);

%% Calculate and plot transmission spectrum
Transmission_small = abs(Ex_freq./Ex_ref_freq).^2; 

%wvlens(1:length(wvlens)/2+2) = 0;
subplot(2,2,4);
plot(wvlens, Transmission_small, 'r'); 
set(gca,'FontSize',15,'fontWeight','bold')
set(findall(gcf,'type','text'),'FontSize',15,'fontWeight','bold')
%plot(wvlens(lowIndex:highIndex), Transmission_small(lowIndex:highIndex), 'r'); 

% line([1000 2500], [1 1], 'Color', 'k'); 


axis([ lowerWvl upperWvl 0 max(Transmission_small(lowIndex:highIndex))+10])
xlabel('Wavelength (nm)'); ylabel('|E(0,0,0)|^2'); 
title('GOLD {1,10,4} L=100nm d=40nm w=40nm t=40nm h=40nm'); 
set(gca,'FontSize',15,'fontWeight','bold')
set(findall(gcf,'type','text'),'FontSize',15,'fontWeight','bold')
%% Test
% Fs = 2000;                    % Sampling frequency
% ht = 1/Fs;                     % Sample time
% L = 1000;                     % Length of signal
% t = (0:L-1)*ht;                % Time vector
% % Sum of a 50 Hz sinusoid and a 120 Hz sinusoid
% x = sin(2*pi*600*t); 
% % plot(t, x)
% 
% [freq X] = Fourier_Normalized(x, ht); 
% plot(freq, abs(X))