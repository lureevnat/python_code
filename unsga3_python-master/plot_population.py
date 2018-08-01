import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_population(opt, popObj):

    #figure(opt.fig);
    #hold all;
    plt.hold(True)
    if opt["M"]==2:
        #plot(popObj(:,1),popObj(:,2),'o','MarkerEdgeColor',opt.Color{randi(size(opt.Color,2))},'MarkerFaceColor',opt.Color{randi(size(opt.Color,2))});
        plt.plot(popObj[:][0],popObj[:][1] , 'ro')
    elif opt["M"]==3:
        #plot3(popObj(:,1),popObj(:,2),popObj(:,3),'o','MarkerEdgeColor',opt.Color{randi(size(opt.Color,2))},'MarkerFaceColor',opt.Color{randi(size(opt.Color,2))});
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(popObj[:,0],popObj[:,1],popObj[:,2],c="r",marker="o")

    #xlim([0 1])
    #ylim([0 2])
    #drawnow;
    plt.show()
