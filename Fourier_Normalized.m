function [signal_freq, freq] = Fourier_Normalized(signal_t, ht)
%UNTITLED6 Summary of this function goes here
%   Detailed explanation goes here

Fs = 1/ht; 
L = length(signal_t);
% t = [0:L-1]*ht; 

NFFT = 2^(nextpow2(L)); 
signal_freq = fftshift(fft(signal_t, NFFT))/L; 
freq = Fs/2*linspace(-1,1,NFFT); 


end

