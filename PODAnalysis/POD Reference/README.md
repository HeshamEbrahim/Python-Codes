# POD
implementation of the proper orthogonal decomposition

input:

in commend line:
N   is the number of snapshots
M   is the number of modes

required files:
snapshots (i.e. of velocity, pressure, etc.)
averaged field (i.e. of the same physical quantity)

data files should be in .csv format

snapshots file named as [file\_prefix].[file\_number].[file\_suffix],
where [file\_prefix] and [file\_suffix] are specified in the script, [file\_number] is a int in range(N)

averaged file name is in the line of data\_ave = np.genfromtxt...

data to be employed for POD is specified in var\_names

output:
    POD_coef.csv    containing eigenvalues and first M mode eigenvectors
    POD_mode.csv    containing the corresponding modes arranged relative to the snapshot coordinates
