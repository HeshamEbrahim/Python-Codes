import numpy as np
import matplotlib.pyplot as plt

# Load the data in
CdX_B = np.genfromtxt('Base-DX.csv', delimiter=',',skip_header=True)
CdX_F = np.genfromtxt('Front-DX.csv', delimiter=',',skip_header=True)

# Car Base
# Split y coordinates
Y = CdX_B[:,1] < 0.7965
yNew = CdX_B[Y,0:4]

# #  Split z coordinates
Z = yNew[:,2] > 0.234
zNew = yNew[Z,0:4]
X = ((zNew[:,2] > 0.6) | (zNew[:,0] > -0.4))
xNew = zNew[X,0:4]

saveData = np.savetxt("CdX-B.csv", xNew, delimiter=",")

# Car Forebody
# Split y coordinates
Y_F = CdX_F[:,1] < 0.7965
yNew_F = CdX_F[Y_F,0:4]

#  Split z coordinates
Z_F = yNew_F[:,2] > 0.2332
zNew_F = yNew_F[Z_F,0:4]
X_F = (((zNew_F[:,0] < -4) | (zNew_F[:,2] > 0.6)) | ((zNew_F[:,0] < -4) | (zNew_F[:,2] > 0.6)))
xNew_F = zNew_F[X_F,0:4]

saveData = np.savetxt("CdX-F.csv", xNew_F, delimiter=",")