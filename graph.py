import matplotlib.pyplot as plt
import numpy as np
import sys

filename = sys.argv[1]

x, y, z = np.loadtxt(filename, delimiter=',', unpack=True)
plt.plot(x,y, label=u'G\xe6rings temp!')
plt.plot(x,z, label=u'k\xf8levands temp!')
plt.xlabel('Time')
plt.ylabel('Temp')
plt.title('Maesk temperatur\nCheck it out')
plt.legend()
plt.show()

#import numpy as np
#import matplotlib.pyplot as plt
#
#data = np.loadtxt('mash0010fermentation.log', delimiter=',', unpack=True)
#for column in data.T:
#  plt.plot(data[:,0], column)
#
#plt.show()
