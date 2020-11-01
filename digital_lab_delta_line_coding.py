import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz, square

#time-frequency axis defination
fs=1001
T=1/fs
L=5001  # Keep this odd for ease of Mathematics
t=np.linspace(0,L-1,L)*T
#------------------------Delta-Modulation-------------------------
#INPUT Signal
f0=0.05
sig0=np.sin(2*np.pi*f0*t)

x=sig0
u=np.zeros(L)
tx=np.zeros(L)#contains parallel output

b=np.zeros(L)
delta=0.1
count=0 #this counter will make sample and hold circuit
for n in range(L):
    if(count>0):
        u[n]=u[n-1]
        tx[n]=tx[n-1]
        
        
    else:
        count=50
        if x[n] > u[n-1]:
            b[n]=delta
            tx[n]=1
        elif x[n] < u[n-1]:
            b[n]=-delta
            tx[n]=0
        u[n]=u[n-1]+b[n]
        
    count-=1
    
sig1=u
fig0,ax0=plt.subplots(6)
fig0.show()
ax0[0].plot(t,sig0,label='Input Signal', color='y')
ax0[0].legend()
ax0[0].set_ylabel("Amplitude")
ax0[0].plot(t,sig1,label='Delta Modulated Signal')
ax0[0].legend()
ax0[0].set_ylabel("Amplitude")
ax0[1].plot(t,tx,label='tx')
ax0[1].set_ylabel("Amplitude")
ax0[1].legend()


#---------------------Line-Coding------------

#NRZ-L

sig2=square(2*np.pi*5*t,duty=tx)

ax0[2].plot(t,sig2,label='NRZ-L',color='y')
ax0[2].set_ylabel("Amplitude")
ax0[2].legend()

#NRZ-M
tmp=np.zeros(L)
count=0 #this counter will make sample and hold circuit
for n in range(L):
    if(count>0):
        tmp[n]=tmp[n-1]
    else:
        count=50
        if(tx[n]==1 and tmp[n-1]==1):
            tmp[n]=0
        elif(tx[n]==1 and tmp[n-1]==0):
            tmp[n]=1
        else:
            tmp[n]=tmp[n-1]
    count-=1
sig3=square(2*np.pi*5*t,duty=tmp)

ax0[3].plot(t,sig3,label='NRZ-M',color='y')
ax0[3].set_ylabel("Amplitude")
ax0[3].legend()

#NRZ-S
count=1#this counter will make sample and hold circuit
for n in range(L):
    if(count>0):
        tmp[n]=tmp[n-1]
    else:
        count=50
        if(tx[n]==0 and tmp[n-1]==1):
            tmp[n]=0
        elif(tx[n]==0 and tmp[n-1]==0):
            tmp[n]=1
        else:
            tmp[n]=tmp[n-1]
    count-=1

sig4=square(2*np.pi*5*t,duty=tmp)

ax0[4].plot(t,sig4,label='NRZ-S',color='y')
ax0[4].set_ylabel("Amplitude")
ax0[4].legend()

#RZ
count=1#this counter will make sample and hold circuit
for n in range(L):
    if(count>0):
        tmp[n]=tmp[n-1]
    else:
        count=25
        if(tx[n]==1 and tmp[n-1]==1):
            tmp[n]=0
        elif(tx[n]==1 and tmp[n-1]==0):
            tmp[n]=1
        else:
            tmp[n]=tmp[n-1]
    count-=1    
sig5=square(2*np.pi*5*t,duty=tmp)
ax0[5].plot(t,tx,label='tx')
ax0[5].plot(t,sig5,label='RZ',color='y')
ax0[5].set_ylabel("Amplitude")
ax0[5].legend()