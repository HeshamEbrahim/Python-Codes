import numpy as np
import matplotlib.pyplot as plt

path1 = "D:\\Documents\\Northumbria University\\PhD Research\\CFD\\Ahmed Model\\Platoon\\IDDES\\1L\\Extracted Data\\xL=0.0625_Leader\\State "
path2 = "D:\\Documents\\Northumbria University\\PhD Research\\CFD\\Ahmed Model\\Platoon\\IDDES\\1L\\Extracted Data\\xL=0.125_Leader\\State "
path3 = "D:\\Documents\\Northumbria University\\PhD Research\\CFD\\Ahmed Model\\Platoon\\IDDES\\1L\\Extracted Data\\xL=0.0625_Follower_Ahead\\State "
path4 = "D:\\Documents\\Northumbria University\\PhD Research\\CFD\\Ahmed Model\\Platoon\\IDDES\\1L\\Extracted Data\\xL=0.0625_Follower\\State "
path5 = "D:\\Documents\\Northumbria University\\PhD Research\\CFD\\Ahmed Model\\Platoon\\IDDES\\1L\\Extracted Data\\xL=0.125_Follower\\State "

files = 480
for i in range(0, files):

    i = i+1
    # Convert Number to String
    NumtoStr = str(i)

    # Load the data in
    xSplit = np.genfromtxt('State '+NumtoStr+'.csv', delimiter=',',skip_header=True)

    # Split x=-0.06525
    X = xSplit[:,4] == -0.06525
    x00625_Leader = xSplit[X,0:7]

    # Split x=-0.1305
    X = xSplit[:,4] == -0.1305
    x0125_Leader = xSplit[X,0:7]

    # Split x=-0.97875
    X = xSplit[:,4] == -0.97875
    x00625_Follower_Ahead = xSplit[X,0:7]

    # Split x=-2.15325
    X = xSplit[:,4] == -2.15325
    x00625_Follower = xSplit[X,0:7]

    # Split x=-2.2185
    X = xSplit[:,4] == -2.2185
    x0125_Follower = xSplit[X,0:7]

    print("iteration: ", i,":",files)
    saveData = np.savetxt(path1+NumtoStr+".csv", x00625_Leader, delimiter=",", header="U Mean, U0, U1, U2, X, Y, Z", comments='')
    saveData = np.savetxt(path2+NumtoStr+".csv", x0125_Leader, delimiter=",", header="U Mean, U0, U1, U2, X, Y, Z", comments='')
    saveData = np.savetxt(path3+NumtoStr+".csv", x00625_Follower_Ahead, delimiter=",", header="U Mean, U0, U1, U2, X, Y, Z", comments='')
    saveData = np.savetxt(path4+NumtoStr+".csv", x00625_Follower, delimiter=",", header="U Mean, U0, U1, U2, X, Y, Z", comments='')
    saveData = np.savetxt(path5+NumtoStr+".csv", x0125_Follower, delimiter=",", header="U Mean, U0, U1, U2, X, Y, Z", comments='')