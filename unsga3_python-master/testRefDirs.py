import initweight
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

objCount = 3;
pointCount = 9;
D = np.transpose(initweight.initweight(objCount, pointCount))


if objCount == 2:
    pass
    #you need to write below
    plt.plot(D[:,0],D[:,1], 'ro')
    #scatter(D(:,1), D(:,2));
elif objCount == 3:
    pass
    #you need to write below
    #scatter3(D(:,1), D(:,2), D(:,3));
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.scatter(D[:,0],D[:,1],D[:,2],c="r",marker="o")


else:
    pass

plt.show()
