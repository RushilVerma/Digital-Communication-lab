import my_package.my_functions as mf # This is a user defined package
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

#-----------------MODULATION---------------------------------

#time frequency axis defination
Fs=1000
T=1/Fs
L=5001   # Keep this odd for ease of Mathematics

t=np.linspace(0,L-1,L)*T

#Sinusodial signal------INPUT Signal
f0=1
sig0=np.sin(2*np.pi*f0*t)

#Sawtooth Waveform

f1=f0*6

sig1=signal.sawtooth(2*np.pi*f1*t)

#-----------------Modulated Signal-------------------
# PWM Signal
sig2=sig0>sig1

# PPM Signal
ppm=np.zeros(L)
count=0

for i in range(L-2):
    if count>0:
        ppm[i]=1;
        count=count-1;
        continue;
    
    if sig2[i]==1 and sig2[i+1]==0:
        ppm[i]=1;
        count=L/1000+1;

#-------------------DEMODULATION------------------------------

fig1,ax1=plt.subplots(8)
fig1.show()

#PWM SIGNAL DISPLAY

ax1[0].plot(t,sig1,label='Signal Sawtooth')
ax1[0].plot(t,sig0,label='Input Signal', color='y')
ax1[0].plot(t,2*sig2-1,label='PWM Signal', color='r')

ax1[0].grid()
ax1[0].set_title("PWM Signal")        
ax1[0].set_xlabel("Time")               
ax1[0].set_ylabel("Amplitude")

#PPM SIGNAL DISPLAY
ax1[1].plot(t,ppm,label='PPM Signal')
ax1[1].grid()
ax1[1].set_title("PPM Signal")        
ax1[1].set_xlabel("Time")               
ax1[1].set_ylabel("Amplitude")
#Ramp generator

b=0
a=.025
sig3=np.zeros([L])

for n in range(len(t)):
    b=sig3[n-1]
    if (sig2[n-1]==0 and sig2[n]==1):
        b=0
    sig3[n]=(a*sig2[n]+b)

ax1[2].plot(t,sig3,label='Ramp Generator')
ax1[2].grid()
ax1[2].set_title("Ramp Generator")        
ax1[2].set_xlabel("Time")               
ax1[2].set_ylabel("Amplitude")
        
#Ref. Pulse generator
f2=f0*5

sig4=signal.square(2*np.pi*f2*t,duty=0.5)


ax1[3].plot(t,sig4,label='Ref. Pulse Generated')
ax1[3].grid()
ax1[3].set_title("Reference Pulse Signal")        
ax1[3].set_xlabel("Time")               
ax1[3].set_ylabel("Amplitude")

# Summation Ramp + Ref. Pulse Signal

sig5=sig4+sig3


ax1[4].plot(t,sig5,label='Ramp + Ref. Pulse Signal')
ax1[4].grid()
ax1[4].set_title("Ramp + Ref. Pulse Signal")        
ax1[4].set_xlabel("Time")               
ax1[4].set_ylabel("Amplitude")

clipV=np.max(sig5)-2
maxsig=np.ones([L])*(clipV)

ax1[4].plot(t,maxsig)
        
#PAM signal 


sig6=np.zeros([L])
peakpulse=1
for n in range(len(t)):
    if sig5[n]-clipV>0:
        sig6[n]=sig5[n]-clipV
    

ax1[5].plot(t,sig6,label='PAM Signal')
ax1[5].grid()
ax1[5].set_title("PAM Signal")        
ax1[5].set_xlabel("Time")               
ax1[5].set_ylabel("Amplitude")


#Filtered signal
normf=3*f0/Fs
b,a=signal.butter(5,normf)
sig7=signal.filtfilt(b,a,sig5)

ax1[6].plot(t,sig7,label='Filter processed Signal')
ax1[6].grid()
ax1[6].set_title("Filtered Signal")        
ax1[6].set_xlabel("Time")               
ax1[6].set_ylabel("Amplitude")

# Input display for comparision
ax1[7].plot(t,sig0,label='Input Signal')
ax1[7].grid()
ax1[7].set_title("Input")        
ax1[7].set_xlabel("Time")               
ax1[7].set_ylabel("Amplitude")