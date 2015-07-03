function [signal_freq, freq] = fouriernorm(signal_t, ht)
%UNTITLED6 Summary of this function goes here
%   Detailed explanation goes here

Fs = 1/ht; 
L = length(signal_t);
% t = [0:L-1]*ht; 

NFFT = 2^(nextpow2(L)); 
signal_freq2 = (fft(signal_t, NFFT))/L; 


signal_freq = signal_freq2(1:NFFT/2 + 1); 
freq = Fs/2*linspace(0,1,NFFT/2+1); 


end
