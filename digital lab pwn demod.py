import my_package.my_functions as mf # This is a user defined package
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import scipy.fft as sfft

#-----------------MODULATION---------------------------------

#time frequency axis defination
Fs=1000
T=1/Fs
L=1001   # Keep this odd for ease of Mathematics
t=np.linspace(0,L-1,L)*T
freq_axis=np.linspace(-(L-1)/2,(L-1)/2,L)*Fs/L

#Sinusodial signal
f=5
sig0=np.sin(2*np.pi*f*t)


fig0,ax0=plt.subplots(3)
fig0.show()

ax0[0].plot(t,sig0,label='Signal Sine')
ax0[0].grid()
ax0[0].set_title("SIGNAL INPUT")        
ax0[0].set_xlabel("Time")               
ax0[0].set_ylabel("Amplitude")


#Sawtooth Waveform

f=25

sig1=signal.sawtooth(2*np.pi*f*t)


ax0[1].plot(t,sig1,label='Signal Sawtooth')
ax0[1].grid()
ax0[1].set_title("Sawtooth SIGNAL")        
ax0[1].set_xlabel("Time")               
ax0[1].set_ylabel("Amplitude")


#modulated signal

sig2=sig0>sig1

ax0[2].plot(t,sig2,label='Signal Modulated')
ax0[2].grid()
ax0[2].set_title("Modulated SIGNAL")        
ax0[2].set_xlabel("Time")               
ax0[2].set_ylabel("Amplitude")

#-------------------DEMODULATION------------------------------

fig1,ax1=plt.subplots(6)
fig1.show()

ax1[0].plot(t,sig2,label='Signal Modulated')
ax1[0].grid()
ax1[0].set_title("Modulated SIGNAL")        
ax1[0].set_xlabel("Time")               
ax1[0].set_ylabel("Amplitude")

#Ramp generator

b=0
a=.02

sig3=np.zeros([L])

for n in range(len(t)):
    b=sig3[n-1]
    
    if (sig2[n-1]==0 and sig2[n]==1):
        b=0
        
    sig3[n]=(a*sig2[n]+b)


ax1[1].plot(t,sig3,label='Ramp Generated')
ax1[1].grid()
ax1[1].set_title("RAMP GENERATOR SIGNAL")        
ax1[1].set_xlabel("Time")               
ax1[1].set_ylabel("Amplitude")
        
#Ref. Pulse generator
f=10

sig4=signal.square(2*np.pi*f*t,duty=0.5)


ax1[2].plot(t,sig4,label='Ref. Pulse Generated')
ax1[2].grid()
ax1[2].set_title("Reference Pulse SIGNAL")        
ax1[2].set_xlabel("Time")               
ax1[2].set_ylabel("Amplitude")

#summed up generator


sig5=np.zeros([L])

for n in range(len(t)):
    
    sig5[n]=sig4[n]+sig3[n]+1


ax1[3].plot(t,sig5,label='summation Generated')
ax1[3].grid()
ax1[3].set_title("SUMMATION SIGNAL")        
ax1[3].set_xlabel("Time")               
ax1[3].set_ylabel("Amplitude")
clipV=np.max(sig5)-2
maxsig=np.ones([L])*(clipV)

ax1[3].plot(t,maxsig)
        
#PAM signal 


sig6=np.zeros([L])
peakpulse=1
for n in range(len(t)):
    if sig5[n]-clipV>0:
        sig6[n]=sig5[n]-clipV
    

ax1[4].plot(t,sig6,label='PAM Signal')
ax1[4].grid()
ax1[4].set_title("PAM SIGNAL")        
ax1[4].set_xlabel("Time")               
ax1[4].set_ylabel("Amplitude")


#LPF Filtered signal
cut_off=10

fft_sig1=sfft.fftshift(sfft.fft(sig6)/L)

filter_LPF=np.ones([len(freq_axis)])
filter_LPF[np.asarray(np.where(  (freq_axis>cut_off)|(freq_axis<-cut_off)  ))]=0

fft_sig1=fft_sig1*filter_LPF
sig7=L*sfft.ifft(sfft.ifftshift(fft_sig1))

ax1[5].plot(t,sig7,label='LPF processed Signal')
ax1[5].grid()
ax1[5].set_title("LPF FILTERED SIGNAL")        
ax1[5].set_xlabel("Time")               
ax1[5].set_ylabel("Amplitude")
