##

"Proper Orthogonal Decomposition using the Snapshot Method"

##

import numpy as np
from scipy import linalg
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('N', type=int, help='the number of snapshots')
parser.add_argument('M', type=int, help='the number of modes to be presented')
args = parser.parse_args()

file_number = args.N
mode_number = args.M

file_prefix = 'State '
file_suffix = '.csv'

filename = 'POD.dat'

var_names = ['U0', 'U1', 'U2']
var_coordinates = ['X', 'Y', 'Z']

# load the average data first
data_ave = np.genfromtxt('Mean.csv',
                         names=True,
                         delimiter=','
                        )

# get data size
data = np.empty((data_ave.size,len(var_names)))
data_len = data_ave.size*len(var_names)
data_bytesize = data_ave.dtype[0].itemsize
coordinates = np.empty((data_ave.size,len(var_coordinates)))

# memmap
fp = np.memmap(filename, 
               dtype=data_ave.dtype[0], 
               mode='w+', 
               shape=(data_len,file_number), 
               order='F')

# read and calculate perturbation, store in fp
for i in range(1,file_number):
    NumtoStr = str(i)
    file_name = file_prefix+NumtoStr+file_suffix
    data_ins = np.genfromtxt(file_name, names=True, delimiter=',')

    # u'(x,t) = U(x) - ui(x,t)
    for j, var in enumerate(var_names):
        data[:,j] = data_ins[var] - data_ave[var]
        
    fp[:,i-1] = data.flatten()

del fp

# get coordinates
for i, var in enumerate(var_coordinates):
    coordinates[:,i] = data_ave[var]

# compose the covariance matrix
matrix_cov = np.empty((file_number, file_number))

for i in range(file_number):
    data_i = np.memmap(filename,
                       dtype=data_ave.dtype[0],
                       mode='r+',
                       shape=(data_len,1),
                       order='F',
                       offset=i*data_len*data_bytesize
                      )
    
# R(X,X') = U_T * U - squares the matrix 'C' and correlates U&U U&V V&V
    matrix_cov[i,i] = np.sum( np.square(data_i) )
    
    for j in range(i+1,file_number):
        data_j = np.memmap(filename,
                           dtype=data_ave.dtype[0],
                           mode='r+',
                           shape=(data_len,1),
                           order='F',
                           offset=j*data_len*data_bytesize
                          )
        
        matrix_cov[i,j] = np.sum( np.multiply( data_i, data_j ) )
        matrix_cov[j,i] = matrix_cov[i,j]

# Compute e=eigenvalues and v=eigenvectors 
e, v = linalg.eig(matrix_cov)

# Sort in eigenvalues in ascending order
idx = np.argsort( e )[::-1]

# the matrix is symmetric, all eigenvalues are non-negative real
# denominator for discrete-to-norm
eig = np.real(e)[idx]
sigma = np.sqrt(eig)

v = v[:,idx]

# save modes
modes = np.zeros([data_len, mode_number], order='F')

for i in range(file_number):
    data = np.memmap(filename,
                     dtype=data_ave.dtype[0],
                     mode='r+',
                     shape=(data_len,1),
                     order='F',
                     offset=i*data_len*data_bytesize
                    ).flatten()

    # POD Modes = sum(Vn(i)*Un)/abs(sum(Vn(i)*Un))
    for j in range(mode_number):
        modes[:,j] = (modes[:,j]+data*v[i,j])
        
for j in range(mode_number):
    modes[:,j] /= sigma[j]

# save the modes
for j in range(mode_number):
    NumtoStr = str(j)
    file_name = 'POD_mode '+NumtoStr+'.txt'
    MODES = np.append(coordinates,modes[:,j].reshape(data_ave.size,len(var_names)), axis=1)

    np.savetxt(file_name,MODES,
               fmt='%12.6e',
               delimiter=',',
               header="X, Y, Z, U0, U1, U2",
               comments=''
              )

# coefficients, eigenvalues, sigma, and the Vij of the first X modes
data = np.concatenate((eig.reshape((-1,1)), sigma.reshape((-1,1)), v[:,:mode_number]),axis=1)

var_names = [ 'V{:d}'.format(i) for i in range(mode_number) ]
var_names.insert(0, 'sigma')
var_names.insert(0, 'eigval')

np.savetxt('POD_coef.csv',
           data,
           fmt = '%12.6e',
           delimiter = ',',
           header = ','.join(var_names),
           comments = ''
          )

