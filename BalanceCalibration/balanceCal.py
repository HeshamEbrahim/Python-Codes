import numpy as np
import matplotlib.pyplot as plt

# Load the data in
cal_data = np.genfromtxt('2ndorder_balance_cal.csv', delimiter=',',skip_header=True)
# cal_data = np.genfromtxt('balance_cal.csv', delimiter=',',skip_header=True)

# H = cal_data[:,:6]

# variables and loop for standard deviation analysis by removing rows
# arrSize = np.size(H, axis=0) #array size
# devData = []
# devDataFx = []
# devDataFy = []
# devDataFz = []
# devDataMx = []
# devDataMy = []
# devDataMz = []
# iteration = []
# for i in range(arrSize):

    # delete = np.delete(cal_data,i,0)

# Extract the loads and the voltages
H = cal_data[:,:6]
R = cal_data[:,6:]

    # H = delete[:,:6]
    # R = delete[:,6:]

# Create the elongated R matrix
Rp = np.append(R,R*R,axis=1)
Rp = np.append(Rp,np.repeat(R[:,0][:,np.newaxis],5,axis=1)*R[:,1:],axis=1)
Rp = np.append(Rp,np.repeat(R[:,1][:,np.newaxis],4,axis=1)*R[:,2:],axis=1)
Rp = np.append(Rp,np.repeat(R[:,2][:,np.newaxis],3,axis=1)*R[:,3:],axis=1)
Rp = np.append(Rp,np.repeat(R[:,3][:,np.newaxis],2,axis=1)*R[:,4:],axis=1)
Rp = np.append(Rp,(R[:,4]*R[:,5])[:,np.newaxis],axis=1)

# Compute the coefficient matrix
# R2 = np.matmul(R.transpose(),R)
R2 = np.matmul(Rp.transpose(),Rp)
R2inv = np.linalg.inv(R2)
# Rinv = np.matmul(R2inv,R.transpose())
Rinv = np.matmul(R2inv,Rp.transpose())
C = np.matmul(Rinv,H)

# Get the modelled loads
# Hp = np.matmul(R,C)
Hp = np.matmul(Rp,C)

saveData = np.savetxt("C.csv", C, delimiter=",")

# Compute error (standard deviation)
err = np.sqrt((np.sum((Hp-H)**2,axis=0))/(H.shape[0]-1))
err_norm = (err / np.array([120,60,240,28,44,24]))*100

#     devData.append([i,err[0],err[1],err[2],err[3],err[4],err[5]])
#     devDataFx.append(err[0])
#     devDataFy.append(err[1])
#     devDataFz.append(err[2])
#     devDataMx.append(err[3])
#     devDataMy.append(err[4])
#     devDataMz.append(err[5])
#     iteration.append(i)
    
# saveData = np.savetxt("err.csv", devData, delimiter=",")

# # single component error evaluation
# plt.subplot(321)
# plt.title('Fx err')
# plt.plot(iteration, devDataFx)
# plt.subplot(325)
# plt.title('Fy err')
# plt.plot(iteration, devDataFy)
# plt.subplot(323)
# plt.title('Fz err')
# plt.plot(iteration, devDataFz)
# plt.subplot(322)
# plt.title('Mx err')
# plt.plot(iteration, devDataMx)
# plt.subplot(324)
# plt.title('My err')
# plt.plot(iteration, devDataMy)
# plt.subplot(326)
# plt.title('Mz err')
# plt.plot(iteration, devDataMz)
# plt.tight_layout()
# plt.show()

# Plot the results
spv = [321, 323, 325, 322, 324, 326]
ttv = ["Fx","Fy","Fz","Mx","My","Mz"]
for i, ind in enumerate(spv):
    plt.subplot(ind)
    plt.scatter(H[:,i], Hp[:,i])
    plt.plot([0,np.max(H[:,i])],[0,np.max(H[:,i])],"k--")
    plt.title('{0} Err:{1:0.2f}%FS'.format(ttv[i],err_norm[i]))
    plt.grid()
    plt.xlabel("Model")
    plt.ylabel("Original")
plt.tight_layout()
plt.show()

