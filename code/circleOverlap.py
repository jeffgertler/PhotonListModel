import numpy as np
import matplotlib.pyplot as plt


''' returns the brigtness of the the star when eclipsed
	R: radius of planet
	r: radius of star (assumes r<R)
	d: distance between them (accounts for negative distance)
	B: brightness
'''
def eclipse_brightness(R, r, d, B_st, B_bg):
	d = np.abs(d)
	if(d<=(R-r)): return B_bg
	
	d1 = (d**2-r**2+R**2)/(2*d)
	d2=d-d1
	
	A1=R**2 *np.arccos(d1/R)-d1*np.sqrt(R**2-d1**2)
	A2=r**2 *np.arccos(d2/r)-d2*np.sqrt(r**2-d2**2)
	return (np.pi*r**2 - (A1+A2))*B_st + B_bg


R = 1.5
r = 1
B_st = 2
B_bg = 1


d = np.arange(-5, 5, .01)
b = np.zeros(len(d))
for i in range(len(d)): b[i] = eclipse_brightness(R, r, d[i], B_st, B_bg)
plt.plot(d, b)
plt.show()

