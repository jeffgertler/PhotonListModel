import numpy as np
import matplotlib.pyplot as plt
import sys
import random as random
import cProfile

''' 
Example input: run circleOverlap.py 0 1 10 .2 0 1 0 1234

returns the brightness of the the star when eclipsed
	t0: central time of the eclipse
	v: relative velocity of the planet
	R: radius of planet
	r: relative radius of star (assumes r<R)
	o: vertical offset of centers of the circles
	B_st: star brightness (assumed constant over visible area)
	B_bg: average background brightness
'''

# generates arrays of corresponding times and brightnesses of the eclipse
def eclipseCurve(t0, v, R, r_ratio, o, B_st, B_bg):
	r = R*r_ratio
	bin_size = 1./(B_st+B_bg)*.001
	dt = (R+r)/v
	t = np.arange(t0-dt, t0+dt, bin_size)
	
	d = np.sqrt(((t-t0)*v)**2+o**2)
	b = np.zeros(len(d))
	for i in range(len(d)):
		if(d[i]<=(R-r)): b[i] = B_bg*np.pi*R**2
		elif(d[i]>=(R+r)): b[i] = B_st*np.pi*r**2 + B_bg*np.pi*R**2
		else:
			d1 = (d[i]**2-r**2+R**2)/(2*d[i])
			d2=d[i]-d1
			A1=R**2 *np.arccos(d1/R)-d1*np.sqrt(R**2-d1**2)
			A2=r**2 *np.arccos(d2/r)-d2*np.sqrt(r**2-d2**2)
			
			b[i] = (np.pi*r**2 - (A1+A2))*B_st + B_bg*np.pi*R**2
	return t, b

# gives a specific brightness at a specific time durring the eclipse
def eclipsePoint(t_point, t0, v, R, r_ratio, o, B_st, B_bg):
	r = R*r_ratio
	d = np.sqrt(((t_point-t0)*v)**2+o**2)
	if(d<=(R-r)): return B_bg*np.pi*R**2
	elif(d>=(R+r)): return B_st*np.pi*r**2 + B_bg*np.pi*R**2
	else:
		d1 = (d**2-r**2+R**2)/(2*d)
		d2=d-d1
		A1=R**2 *np.arccos(d1/R)-d1*np.sqrt(R**2-d1**2)
		A2=r**2 *np.arccos(d2/r)-d2*np.sqrt(r**2-d2**2)
		return (np.pi*r**2 - (A1+A2))*B_st + B_bg*np.pi*R**2

# generates a set of photon times given the eclipse parameters
def listGenerator(t0, v, R, r_ratio, o, B_st, B_bg, seed):
	random.seed(seed)
	bin_size = 1./(B_st+B_bg)*.001
	t, b = eclipseCurve(t0, v, R, r_ratio, o, B_st, B_bg)
	tData = np.array([])
	for i in range(0, len(t)):
		if(random.random() <= b[i]*bin_size): tData = np.append(tData, t[i])
	return tData

# Calculates the probability of a set of photon times based on the eclipse parameters
def logProbabilityCalculator(tData, t, t0, v, R, r_ratio, o, B_st, B_bg):
	bin_size = 1./(B_st+B_bg)*.001
	log_probability = 0
	for i in range(0, len(t)):
		if(t[i] in tData): 
			log_probability -= np.log(eclipsePoint(t[i], t0, v, R, r_ratio, o, B_st, B_bg)*bin_size)
		else: log_probability -= np.log(1-eclipsePoint(t[i], t0, v, R, r_ratio, o, B_st, B_bg)*bin_size)
	return log_probability


def checkRadiusRatio(test_ratios, tData, t, t0, v, R, r_ratio, o, B_st, B_bg):
	test_probabilites = np.zeros(len(test_ratios))
	for i in range(len(test_ratios)):
		test_probabilites[i] = logProbabilityCalculator(tData, t, t0, v, R, test_ratios[i], o, B_st, B_bg)
	return test_probabilites

args = sys.argv

t0 = float(args[1])
v = float(args[2])
R = float(args[3])
r_ratio = float(args[4])
o = float(args[5])
B_st = float(args[6])
B_bg = float(args[7])
seed = int(args[8])


t, b = eclipseCurve(t0, v, R, r_ratio, o, B_st, B_bg)
tData = listGenerator(t0, v, R, r_ratio, o, B_st, B_bg, seed)

true_probability = logProbabilityCalculator(tData, t, t0, v, R, r_ratio, o, B_st, B_bg)
print true_probability

test_ratios = np.arange(0.2, 1.1, .2)
test_probabilites = checkRadiusRatio(test_ratios, tData, t, t0, v, R, r_ratio, o, B_st, B_bg)

#cProfile.run('listGenerator(t0, v, R, r_ratio, o, B_st, B_bg, seed)')
#cProfile.run('logProbabilityCalculator(tData, t0, v, R, r_ratio, o, B_st, B_bg)')
#cProfile.run('checkRadiusRatio(test_ratios, tData, t, t0, v, R, r_ratio, o, B_st, B_bg)')

plt.figure(1)
plt.subplot(311)
plt.plot(t, b)

plt.subplot(312)
plt.hist(tData, bins = int(2*(R+R*r_ratio)/v))

plt.subplot(313)
plt.plot(test_ratios, test_probabilites, 'o')
plt.axvline(r_ratio)
plt.xlabel('radius ratio')
plt.ylabel('log probability')

plt.show()
plt.savefig('eclipsePlot.png')

