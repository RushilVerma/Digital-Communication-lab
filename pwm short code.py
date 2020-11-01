import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sci

Fs=1000
T=1/Fs
L=5001   # Keep this odd for ease of Mathematics
t=np.linspace(0,L-1,L)*T

f0=.9
f1=8*f0

#Input Sin
sig0=np.sin(2*np.pi*f0*t)
#Sawtooth
sig1=sci.sawtooth(2*np.pi*f1*t)

#Comparator---------modulation------------
sig2=sig0>sig1

#-----------Demodulation------------------

#Reference wave generator
sig3=sig2*sci.square(2*np.pi*f0*t)
#Ramp generator
sig4=sig2*sci.sawtooth(2*np.pi*f1*t)
#Summation
sig5=sig4+sig3
#LPF filtering
normf=2*f0/Fs
b,a=sci.butter(5,normf)
fsig=sci.lfilter(b,a,sig5)
#Signal inversion
sig6=-fsig
#Plotting
fig0,ax0=plt.subplots(4)
fig0.show()

ax0[0].plot(t,sig0,color='g')
ax0[0].grid()
ax0[0].set_title("SIGNAL IN TIME DOMAIN")

ax0[1].plot(t,sig2,color='y')
ax0[1].grid()
ax0[1].set_title("Pulse Width Modulated Signal")

ax0[2].plot(t,sig5,color='b')
ax0[2].grid()
ax0[2].set_title("Pulse Width Demodulated Signal")

ax0[3].plot(t,sig6,color='r')
ax0[3].grid()
ax0[3].set_title("LPF Output")

