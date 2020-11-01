import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

#------------------------------MODULATION---------------------------------
#time-frequency axis defination
fs=1000
T=1/fs
L=5001   # Keep this odd for ease of Mathematics
t=np.linspace(0,L-1,L)*T

#INPUT Signal
f0=1
sig0=(1+np.sin(2*np.pi*f0*t))/2 #sample and hold circuit    
    
#Quantization
q=8
sig1=np.array(np.round(sig0*q))
sig1=np.int_(sig1)

#Binary Encoding and binary to serial converter
v=4 # code word length
tx=np.empty(L,dtype=object)#contains parallel output

for i in range(L):
    tx[i]=np.binary_repr(sig1[i], width=v)


#------------------------------DEMODULATION---------------------------------
#Serial to Binary converter and Binary Decoder
sig2=np.empty(L,dtype=object)#contain decoded output
  
for i in range(L):
    sig2[i]=int(tx[i],2)
    
sig2=sig2/q
    
#Low Pass Filter
cutoff=f0
fs=fs
order=5
nyq = 0.5 * fs
normal_cutoff = cutoff / nyq

b, a = butter(order, normal_cutoff, btype='low', analog=False)
sig3 = 1-lfilter(b, a, sig2)

fig0,ax0=plt.subplots(4)
fig0.show()
ax0[0].plot(t,sig0,label='Input Signal', color='y')
ax0[0].grid()
ax0[0].legend()
ax0[0].set_title("Signal")                      
ax0[0].set_ylabel("Amplitude")

ax0[1].plot(t,np.abs(sig1/q),label='Quatization Signal', color='r')
ax0[1].legend()
ax0[1].set_ylabel("Amplitude")

print('Binary Serial Output')
print(tx)

ax0[2].plot(t,sig2,label='Binary Decoded Output')
ax0[2].legend()
ax0[2].set_ylabel("Amplitude")

ax0[3].plot(t,sig3,label='Low Pass filtered Output')
ax0[3].legend()
ax0[3].set_ylabel("Amplitude")
ax0[3].set_xlabel("Time")
