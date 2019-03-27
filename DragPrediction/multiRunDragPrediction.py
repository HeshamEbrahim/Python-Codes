import numpy as np
import matplotlib.pyplot as plt
import Functions as funct
from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import differential_evolution

# Load data
files = ['NL2VP_0.5L.csv','NL2VP_0.5T.csv','NL2VP_0.75L.csv','NL2VP_0.75T.csv','NL2VP_1L.csv','NL2VP_1T.csv']

# Variables
Area = 0.0885*0.11167
CD_F = [0.0315, 0.0721, 0.0295, 0.0572, 0.0292, 0.0466]
CD_R = [0.0396, 0.0895, 0.0622, 0.0871, 0.074, 0.087]
caseArray = []

# Set cases in an Array
for i, ind in enumerate(files):

    # Load the data in
    cp_data = np.genfromtxt(ind, delimiter=',',skip_header=True)     

    # Extract and Split Cp 
    front = cp_data[:,0] < -2 
    CpFront = cp_data[front,3]
    CpRear = cp_data[~front,3]
    normalFront = cp_data[front,4]
    normalRear = cp_data[~front,4]
    # Populate initial coefficients
    coefs0 = np.ones((np.size(CpFront)+np.size(CpRear),1)).flatten()

    # Add data into caseArray
    Case = [[CpFront], [CpRear], [normalFront], [normalRear], [coefs0]]
    caseArray.append(Case)  

coefs0 = np.hstack(caseArray[:5])
coefs0 = np.hstack(coefs0[4])

# Fitness Function
def Fitness(Coefs, Area, knownF, knownR):
    return (((knownF[0]-funct.ForceF1(Coefs, caseArray, Area))**2)+((knownR[0]-funct.ForceR1(Coefs, caseArray, Area))**2)+
    ((knownF[2]-funct.ForceF2(Coefs, caseArray, Area))**2)+((knownR[2]-funct.ForceR2(Coefs, caseArray, Area))**2)+
    ((knownF[4]-funct.ForceF3(Coefs, caseArray, Area))**2)+((knownR[4]-funct.ForceR3(Coefs, caseArray, Area))**2))

# print(Fitness(Coefs, Area, knownF, knownR))


# Solution bounds
ub = np.full((1,np.size(coefs0)), 1.3).flatten() 
lb = np.full((1,np.size(coefs0)), 0.5).flatten()
bounds = Bounds(lb,ub)

boundaries = ((1.2,-1.2),)*(len(coefs0)) # boundaries for genetic algorithm

# minimise function
res = minimize(Fitness, coefs0, method='TNC', options={'accuracy' : 1e-20, 'xtol' : 1e-20,'ftol' : 1e-20, 'disp' : True}, args=(Area,CD_F,CD_R), bounds=bounds)

# genetic algorithm (differential evolution)
# res = differential_evolution(Fitness, bounds=boundaries, args=(CpFront,CpRear,Area,normalFront,normalRear,CD_F,CD_R), strategy='best1bin', maxiter=10, popsize=15, tol=0.5, mutation=(0.5,1),
#                             recombination= 0.7, disp=True)

# print result
# print('ForceF= ', ForceF1(res.x, CpFront, Area, normalFront), '  %Diff=', (CD_F[0]-ForceF1(res.x, CpFront, Area, normalFront))/CD_F[0]*100)
# print('ForceR= ', ForceR(res.x, CpFront, CpRear, Area, normalRear), '  %Diff=', (CD_R-ForceR(res.x, CpFront, CpRear, Area, normalRear))/CD_R*100)

# # plots
# x1 = np.linspace(0, np.size(CpFront), num=np.size(CpFront))
# plt.subplot(221)
# plt.plot(x1, CpFront*normalFront*coefs0[0:np.size(CpFront)].flatten() , '-', label='Ref', linewidth=2, color='r')
# plt.plot(x1, CpFront*normalFront*res.x[0:np.size(CpFront)].flatten() , '-')
# plt.xlabel("Point Number")
# plt.ylabel("Cp")
# plt.legend()

# x2 = np.linspace(0, np.size(CpRear), num=np.size(CpRear))
# plt.subplot(222)
# plt.plot(x2, CpRear*normalRear*coefs0[0:np.size(CpRear)].flatten(), '-', label='Ref', linewidth=2, color='r')
# plt.plot(x2, CpRear*normalRear*res.x[np.size(CpFront):np.size(coefs0)].flatten() , '-')
# plt.xlabel("Point Number")
# plt.ylabel("Cp")
# plt.legend()

# plt.subplot(212)
# plt.plot(res.x, 'o', markersize=4, label='coefs')
# plt.xlabel("Coefficient No.")
# plt.ylabel("Scaling")
# plt.show()

# saveData = np.savetxt("test.csv", res.x, delimiter=",")

