from __future__ import division
from __future__ import print_function
import numpy as np
import os
from glob import glob
from numpy import linalg as LA
import matplotlib.pyplot as plt
from pylab import *

folder = 'D:\\Documents\\Northumbria University\\PhD Research\\CFD\Ahmed Model\\Isolation\\Unsteady DES\\Velocity field at centreline\\'
files = os.listdir(folder) # number of files
nmodes = 30 # Number of Modes
file_suffix = 'csv'
var_names = ['Ui', 'Uj', 'Uk']

# velocity mean
mean = np.genfromtxt('D:\\Documents\\Northumbria University\\PhD Research\\CFD\Ahmed Model\\Isolation\\Unsteady DES\\Velocity field at centreline\\Mean.csv',usecols=(0,1,2,3,4,5,6),skip_header=1,delimiter=',')
u_mean,v_mean = mean[:,1],mean[:,2]

# compose covariance matrix
os.chdir(folder)
index=0
for vel_file in range(len(files)):
        vel_file = folder+files[vel_file]
        print(vel_file)
        if index==0:
                data=np.genfromtxt(vel_file,usecols=(0,1,2,3,4,5,6),skip_header=1,delimiter=',')
                x,y,u,v=data[:,4],data[:,5],data[:,1],data[:,2]
                U=u_mean
                V=v_mean
                    
        else:
                data=np.genfromtxt(vel_file,usecols=(0,1,2,3,4,5,6),skip_header=1,delimiter=',')
                x,y,u,v=data[:,4],data[:,5],data[:,1],data[:,2]
                u,v=u-u_mean,v-v_mean
                U=np.vstack((U,u))
                V=np.vstack((V,v))
    
        index+=1  

U=np.hstack((U,V))
# saveData = np.savetxt("U.csv", U, delimiter=",")

# eigen decomposition (autocovariance matrix)
# R(X,X') = U_T * U - squares the matrix 'C' and correlates U&U U&V V&V
R=np.dot(U,np.transpose(U))

# Compute e=eigenvalues and v=eigenvectors 
e, v=LA.eig(R)
# Sort in eigenvalues in ascending order
idx = np.argsort(e)[::-1] 

# denominator for discrete-to-norm
eig = np.real(e)[idx]
sigma = np.sqrt(eig)

# rearrange eigenvector matrix in ascending order
# v = fliplr(v[:,idx])
v = (v[:,idx])

# Basis for constructing POD modes
modes = np.zeros([len(U[1,:]), nmodes], order='F')
POD_coeff = np.zeros([len(U[1,:]), nmodes], order='F')
U_reconstructed = np.zeros([len(U[1,:]), nmodes], order='F')

for i in range(len(files)):
    for j in range(nmodes):
        modes[:,j] += (U[j,:]*v[i,j])/sigma[j]
    energy = np.transpose(e)

# save the modes
for j in range(nmodes):
    file_name = '.'.join(['POD_mode', '{:d}'.format(j), file_suffix])
    np.savetxt(file_name, modes[:,j].reshape(u_mean.size,2), fmt='%12.6e'
    , delimiter=',', header=','.join(var_names)
    , comments='')

# coefficients, eigenvalues, sigma, and the Vij of the first X modes
data = np.concatenate((eig.reshape((-1,1)), sigma.reshape((-1,1)), v[:,:nmodes]),axis=1)

var_names = [ 'V{:d}'.format(i) for i in range(nmodes) ]
var_names.insert(0, 'sigma')
var_names.insert(0, 'eigval')

np.savetxt('POD_coef.csv',
           data,
           fmt = '%12.6e',
           delimiter = ',',
           header = ','.join(var_names),
           comments = ''
          )

x = np.linspace(0, len(e),len(e))
plt.subplot()
plt.semilogx(x, energy, 'ro')
plt.semilogy(x, energy, 'ro')
plt.xlabel('POD Modes')
plt.ylabel('Energy')
plt.show()

# POD Reconstruction