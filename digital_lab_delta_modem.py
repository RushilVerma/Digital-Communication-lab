import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

#time-frequency axis defination
fs=1001
T=1/fs
L=5001  # Keep this odd for ease of Mathematics
t=np.linspace(0,L-1,L)*T
#------------------------Delta-Modulation-------------------------
#INPUT Signal
f0=1
sig0=np.sin(2*np.pi*f0*t)

x=sig0
u=np.zeros(L)
tx=np.zeros(L)#contains parallel output

b=np.zeros(L)
delta=0.1
count=0 #for emulating a counter for sampling and holding
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
#------------------------Demodulation-------------------------
#xn=xn-1+b[n]
sig2=np.zeros(L)

for n in range(L):
    if(tx[n]==1):
        sig2[n]=sig2[n-1]+delta
    else:
        sig2[n]=sig2[n-1]-delta

#Low Pass Filter
cutoff=f0
fs=fs
order=5
nyq = 0.5 * fs
normal_cutoff = cutoff / nyq

b, a = butter(order, normal_cutoff, btype='low', analog=False)
sig3 = -lfilter(b, a, sig2)*2

fig0,ax0=plt.subplots(4)
fig0.show()
ax0[0].plot(t,sig0,label='Input Signal', color='y')
ax0[0].legend()
ax0[0].set_ylabel("Amplitude")
ax0[1].plot(t,sig1,label='Delta Modulated Signal')
ax0[1].legend()
ax0[1].set_ylabel("Amplitude")

print('Binary Output')
print(tx)

ax0[2].plot(t,sig2,label='Receiver Output',color='b')
ax0[2].legend()
ax0[2].set_ylabel("Amplitude")
ax0[3].plot(t,sig3,label='LPF Output',color='r')
ax0[3].legend()
ax0[3].set_ylabel("Amplitude")

ax0[3].set_xlabel("Time")
