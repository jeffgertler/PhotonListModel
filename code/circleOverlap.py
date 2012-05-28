import numpy as np
import matplotlib.pyplot as plt
import sys
import random as random


''' 
Example input: run circleOverlap.py 0 1 5 4 0 1 0 1234

returns the brightness of the the star when eclipsed
	d: horizontal distance between them (accounts for negative distance)
	R: radius of planet
	r: radius of star (assumes r<R)
	o: vertical offset of centers of the circles
	B_st: star brightness (assumed constant over visible area
	B_bg: average background brightness
'''

def eclipseCurve(t0, v, R, r, o, B_st, B_bg):
	bin_size = 1./(B_st+B_bg)*.0001
	dt = (R+r)/v
	t = np.arange(t0-dt, t0+dt, bin_size)
	
	d = (t-t0)*v
	b = np.zeros(len(d))
	for i in range(len(d)):
		d[i] = np.sqrt(d[i]**2+o**2)
		if(d[i]<=(R-r)): b[i] = B_bg*np.pi*R**2
		else:
			d1 = (d[i]**2-r**2+R**2)/(2*d[i])
			d2=d[i]-d1
			A1=R**2 *np.arccos(d1/R)-d1*np.sqrt(R**2-d1**2)
			A2=r**2 *np.arccos(d2/r)-d2*np.sqrt(r**2-d2**2)
			b[i] = (np.pi*r**2 - (A1+A2))*B_st + B_bg*np.pi*R**2
	return t, b

def listGenerator(t0, v, R, r, o, B_st, B_bg, seed):
	random.seed(seed)
	bin_size = 1./(B_st+B_bg)*.0001
	dt = (R+r)/v
	t = np.arange(t0-dt, t0+dt, bin_size)
	
	d = (t-t0)*v
	b = np.zeros(len(d))
	for i in range(len(d)):
		d[i] = np.sqrt(d[i]**2+o**2)
		if(d[i]<=(R-r)): b[i] = B_bg*np.pi*R**2
		else:
			d1 = (d[i]**2-r**2+R**2)/(2*d[i])
			d2=d[i]-d1
			A1=R**2 *np.arccos(d1/R)-d1*np.sqrt(R**2-d1**2)
			A2=r**2 *np.arccos(d2/r)-d2*np.sqrt(r**2-d2**2)
			b[i] = (np.pi*r**2 - (A1+A2))*B_st + B_bg*np.pi*R**2
			
	tData = np.array([])
	for i in range(0, len(t)):
		if(random.random() <= b[i]*bin_size): tData = np.append(tData, t[i])
	return tData

# 
def logProbabilityCalculator(t, tData, b, bin_size):
	log_probability = 0
	for i in range(0, len(t)):
		if t[i] in tData: log_probability = log_probability - np.log(b[i]*bin_size)
		else: log_probability = log_probability - np.log(1-b[i]*bin_size)
	return log_probability

args = sys.argv

t0 = float(args[1])
v = float(args[2])
R = float(args[3])
r = float(args[4])
o = float(args[5])
B_st = float(args[6])
B_bg = float(args[7])
seed = int(args[8])


t, b = eclipseCurve(t0, v, R, r, o, B_st, B_bg)
tData = listGenerator(t0, v, R, r, o, B_st, B_bg, seed)

bin_size = 1./(B_st+B_bg)*.0001
log_probability = logProbabilityCalculator(t, tData, b, bin_size)
print log_probability

plt.figure(1)
plt.subplot(211)
plt.plot(t, b)

plt.subplot(212)
plt.hist(tData, bins = len(tData)/10)


plt.show()

