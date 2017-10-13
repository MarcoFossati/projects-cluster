import numpy as np
import itertools as IT
from numpy import dtype
import sys

cfgfile=str(sys.argv[1])

with open(cfgfile, 'r') as f:
    floats = []
    for each in f:
        floats.append(float(each.strip()))

h1=floats[0]
nl=floats[1]
nl=int(nl)
delta=floats[2]


h=[0]*(nl+1)
h[0]=h1
x1=[0]*(nl+1)
x1[0]=0
x2=[0.1]*(nl+1)
x2[0]=0.1

for i in range(1, nl):
    h[i]=h[i-1]+h[0]*delta**i
    x1[i]=0
    x2[i]=0.1

for i in h:
    print(i)

import matplotlib.pyplot as plt
plt.subplot(211)
for i in range(0,nl):
    plt.plot([x1[i], x2[i]],[h[i], h[i]],'k')
plt.plot([x1[0],x2[0]],[0,0],'k')
plt.plot(x1, h, 'k', x1, h, 'ro')
plt.plot(x2, h, 'k', x2, h, 'ro')
plt.axis([-0.02, 0.12, -h[-2]*0.1, h[-2]+h[-2]*0.1])

plt.subplot(212)
for i in range(0,nl):
    plt.plot(i, h[i], 'k', i, h[i], 'ro')
plt.axis([0, i, -h[-2]*0.1, h[-2]+h[-2]*0.1])

plt.show()
