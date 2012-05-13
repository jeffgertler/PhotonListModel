import numpy as np
import matplotlib.pyplot as plt
import sys


''' returns the brightness of the the star when eclipsed
	d: distance between them (accounts for negative distance)
	R: radius of planet
	r: radius of star (assumes r<R)
	o: offset of centers of the circles
	B_st: star brightness (assumed constant over visible area
	B_bg: average background brightness
'''
def eclipse_brightness(d, R, r, o, B_st, B_bg):
	d = np.sqrt(d**2+o**2)
	if(d<=(R-r)): return B_bg
	
	d1 = (d**2-r**2+R**2)/(2*d)
	d2=d-d1
	
	A1=R**2 *np.arccos(d1/R)-d1*np.sqrt(R**2-d1**2)
	A2=r**2 *np.arccos(d2/r)-d2*np.sqrt(r**2-d2**2)
	return (np.pi*r**2 - (A1+A2))*B_st + B_bg

args = sys.argv


R = float(args[1])
r = float(args[2])
o = float(args[3])
B_st = float(args[4])
B_bg = float(args[5])


d = np.arange(-5, 5, .01)
b = np.zeros(len(d))
for i in range(len(d)): b[i] = eclipse_brightness(d[i], R, r, o, B_st, B_bg)
plt.plot(d, b)
plt.show()

