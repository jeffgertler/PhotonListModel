import numpy as np
import matplotlib.pyplot as plt
import sys
import random as random


''' returns the brightness of the the star when eclipsed
	d: horizontal distance between them (accounts for negative distance)
	R: radius of planet
	r: radius of star (assumes r<R)
	o: vertical offset of centers of the circles
	B_st: star brightness (assumed constant over visible area
	B_bg: average background brightness
'''
def eclipse_brightness(d, R, r, o, B_st, B_bg):
	d = np.sqrt(d**2+o**2)
	if(d<=(R-r)): return B_bg*np.pi*R**2
	
	d1 = (d**2-r**2+R**2)/(2*d)
	d2=d-d1
	
	A1=R**2 *np.arccos(d1/R)-d1*np.sqrt(R**2-d1**2)
	A2=r**2 *np.arccos(d2/r)-d2*np.sqrt(r**2-d2**2)
	return (np.pi*r**2 - (A1+A2))*B_st + B_bg*np.pi*R**2

args = sys.argv

t0 = float(args[1])
v = float(args[2])
R = float(args[3])
r = float(args[4])
o = float(args[5])
B_st = float(args[6])
B_bg = float(args[7])
seed = int(args[8])

bin_size = 1./(B_st+B_bg)*.0001

dt = (R+r)/v
t = np.arange(t0-dt, t0+dt, bin_size)

d = (t-t0)*v
b = np.zeros(len(d))
for i in range(len(d)): b[i] = eclipse_brightness(d[i], R, r, o, B_st, B_bg)

tData = np.array([])
data_probability = 1
for i in range(0, len(t)):
    if(random.random() <= b[i]*bin_size): 
    	tData =np.append(tData, t[i])
    	data_probability = data_probability*b[i]*bin_size
    else: data_probability = data_probability*(1-b[i]*bin_size)

print data_probability

plt.figure(1)
plt.subplot(211)
plt.plot(t, b)

plt.subplot(212)
plt.hist(tData, bins = len(tData)/10)


plt.show()

