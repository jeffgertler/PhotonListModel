import numpy as np
import matplotlib.pyplot as plt
import math
import random
import sys


# input of data from argparse
# args = initial gamma, dt, change in gamma (d/dt gamma, random generator seed
args = sys.argv

gamma = float(args[1])
dt = float(args[2])
dGamma = float(args[3])
seed = float(args[4])


n = gamma * dt
print("Ideal photon count: " + str(n))

'''
# Generates k value for
kTest = np.random.poisson(n, 1)
print("Generated k value: " + str(kTest))
print("Gamma calculated from chosen k: " + str(kTest/dt))

# generate fake set of data making k time data points between 0 and dt
# usses a different seed each time but is based on the seed passed in args
tData = np.zeros(kTest)
for i in range(1, kTest):
    random.seed(seed*i)
    tData[i] = random.random() * dt
print(tData)
'''


# Finds an ideal photon count through Riemann sum for each second and generates 
# a number of photons based on a Poisson distribution. Then creates photon data  
# based on the random seed
tData = np.array([])
for i in range(0, int(dt)):
    idealPNum = int(gamma + (i+.5)*dGamma)
    expPNum = np.random.poisson(idealPNum, 1)
    for j in range(0, expPNum):
        random.seed(seed*j*i)
        tData = np.append(tData, random.random() + i)
print(tData)


# plot for generated data of photons
tDataY = np.zeros(len(tData))

plt.figure(1)
plt.subplot(211)
plt.plot(tData, tDataY, 'or', markersize=3)
plt.title('Random photon data from poisson distribution')
plt.xlabel('time (sec)')
plt.text(tData[0], 0.05, r'Gamma = ' + str(gamma) + r'(photons/sec)')
plt.text(tData[0], 0.04, r'Delta time = ' + str(dt) + r'(sec)')
plt.text(tData[0], 0.03, r'Random generator seed = ' + str(seed))
plt.text(tData[0], 0.02, r'Chosen # of photons = ' + str(len(tData)))

plt.subplot(212)
plt.hist(tData, bins = dt, range = (0, np.round(tData.max()+.5)), facecolor='green')

# plot line of the gamma value at all times
step = np.arange(0, dt + 1, 1)
plt.plot(step, gamma + float(dGamma) * step, 'r')

plt.xlabel('time(sec)')
plt.ylabel('# of photons per sec')



plt.savefig('linearData-1.png')
plt.show()