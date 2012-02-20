import numpy as np
import scipy
from scipy.special import gamma
import matplotlib.pyplot as plt
import math
import random


#input of data
gradient = input("True gradient: ") + 0.0
dt = input("Time interval: ") + 0.0
n = gradient * dt
print("Ideal photon count: " + str(n))

#array of possible k values. n*2 is a guess of upper bound unless n*2 > 150. 
#This gives a run time error b/c 155! was too big for python to handle.
if(n*2 > 150):
    k = np.arange(0.0, 150, 1.)
else:
    k = np.arange(0.0, round(n*2), 1.)

#array of probabilities for each k value using poisson

pbK2 = np.random.poisson(n, len(k))
pbK = np.zeros(len(k))
for i in range (0, len(k)):
    pbK[i] = (n**k[i]) * math.e**(-n) / scipy.special.gamma(k[i]+1)
    
#input chosen value of k for test. if random, a value of k is chosen randomly based on their probabilites
sInput = str(raw_input("For k value either 'c' for artificially chosen or 'r' for choice from probabilities: "))
if(sInput =='r'):
    r = random.random()
    sum = 0
    count = 0
    while(sum < r):
        sum += pbK[count]
        count+=1
    kTest = count
    print("K set as: " + str(count))
elif(sInput == 'c'):
    kTest = input("Pick a value for k (experimental photon count) from 0 to " + str(len(k)-1) + ": ")
print("Probability that k matches true photon count: " + str(pbK[kTest]))
print("Gradient due to chosen k: " + str(kTest/dt))

#generate fake set of data making k time data points between 0 and dt
tData = np.zeros(len(k))
for i in range(1, len(k)):
    tData[i] = random.random() * dt


#Generate and print the plot for k probabilities
plt.figure(1)
plt.subplot(211)

plt.plot(k, pbK, 'or', markersize=3)
plt.plot(k, pbK)

plt.xlabel('k value for # of photons')
plt.ylabel('Probability k is true photon #')

#plot for generated data of photons
plt.subplot(212)
tDataY = np.zeros(len(k))
plt.plot(tData, tDataY, 'or', markersize=3)
plt.xlabel('time of random photon hits based on k')

plt.show()

