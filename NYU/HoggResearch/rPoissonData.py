import numpy as np
import matplotlib.pyplot as plt
import math
import random
import sys

#input of data from argparse

args = sys.argv

print(args[1])
print(args[2])

gamma = float(args[1])
dt = float(args[2])

n = gamma * dt
print("Ideal photon count: " + str(n))


# Generates k value for 
kTest = np.random.poisson(n, 1)
print("Generated k value: " + str(kTest))
print("Gamma calculated from chosen k: " + str(kTest/dt))

#generate fake set of data making k time data points between 0 and dt
tData = np.zeros(kTest)
for i in range(1, kTest):
    tData[i] = random.random() * dt
print(tData)

#plot for generated data of photons
tDataY = np.zeros(kTest)
plt.plot(tData, tDataY, 'or', markersize=3)
plt.title('Random photon data from poisson distribution')
plt.xlabel('time (sec)')
plt.text(tData[0], 0.05, r'Gamma = ' + str(gamma) + r'(photons/sec)')
plt.text(tData[0], 0.04, r'Delta time = ' + str(dt) + r'(sec)')
plt.text(tData[0], 0.03, r'Chosen # of photons = ' + str(kTest))

plt.savefig('rPoissonData15x5.png')
plt.show()