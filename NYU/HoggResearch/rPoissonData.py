import numpy as np
import matplotlib.pyplot as plt
import math
import random
import sys


# input of data from argparse
# args = initial gamma, dt, d/dt gamma, random generator seed
args = sys.argv

gamma = float(args[1])
dt = float(args[2])

n = gamma * dt
print("Ideal photon count: " + str(n))


# Generates k value for
random.seed(args[3])
kTest = np.random.poisson(n, 1)
print("Generated k value: " + str(kTest))
print("Gamma calculated from chosen k: " + str(kTest/dt))

# generate fake set of data making k time data points between 0 and dt
# usses a different seed each time but is based on the seed passed in args
tData = np.zeros(kTest)
for i in range(1, kTest):
    random.seed(args[3]*i)
    tData[i] = random.random() * dt
print(tData)

# plot for generated data of photons
tDataY = np.zeros(kTest)

plt.figure(1)
plt.subplot(211)
plt.plot(tData, tDataY, 'or', markersize=3)
plt.title('Random photon data from poisson distribution')
plt.xlabel('time (sec)')
plt.text(tData[0], 0.05, r'Gamma = ' + str(gamma) + r'(photons/sec)')
plt.text(tData[0], 0.04, r'Delta time = ' + str(dt) + r'(sec)')
plt.text(tData[0], 0.03, r'Random generator seed = ' + str(args[3]))
plt.text(tData[0], 0.02, r'Chosen # of photons = ' + str(kTest))

plt.subplot(212)
plt.hist(tData, bins = dt, facecolor='green')
plt.xlabel('time(sec)')
plt.ylabel('# of photons per sec')

plt.savefig('rPoissonData15x5.png')
plt.show()