import numpy as np

# Functions
def ForceF1(Coefs, caseArray, Area):
    CpF = np.hstack(caseArray[0][0])
    NF = np.hstack(caseArray[0][2])
    Coefs = np.hstack(caseArray[0][4])

    CoefsF = np.hstack(Coefs[0:np.size(CpF)])
    return np.sum(CpF*CoefsF*Area*NF)

def ForceF2(Coefs, caseArray, Area):
    CpF = np.hstack(caseArray[2][0])
    NF = np.hstack(caseArray[2][2])
    Coefs = np.hstack(caseArray[2][4])

    CoefsF = np.hstack(Coefs[0:np.size(CpF)])
    return np.sum(CpF*CoefsF*Area*NF)
 
def ForceF3(Coefs, caseArray, Area):
    CpF = np.hstack(caseArray[4][0])
    NF = np.hstack(caseArray[4][2])
    Coefs = np.hstack(caseArray[4][4])

    CoefsF = np.hstack(Coefs[0:np.size(CpF)])
    return np.sum(CpF*CoefsF*Area*NF)

def ForceR1(Coefs, caseArray, Area):
    CpF = np.hstack(caseArray[0][0])
    CpR = np.hstack(caseArray[0][1])
    NR = np.hstack(caseArray[0][3])
    Coefs = np.hstack(caseArray[0][4])

    CoefsR = np.hstack(Coefs[np.size(CpF):np.size(Coefs)])
    return np.sum(CpR*CoefsR*Area*NR)

def ForceR2(Coefs, caseArray, Area):
    CpF = np.hstack(caseArray[2][0])
    CpR = np.hstack(caseArray[2][1])
    NR = np.hstack(caseArray[2][3])
    Coefs = np.hstack(caseArray[2][4])

    CoefsR = np.hstack(Coefs[np.size(CpF):np.size(Coefs)])
    return np.sum(CpR*CoefsR*Area*NR)

def ForceR3(Coefs, caseArray, Area):
    CpF = np.hstack(caseArray[4][0])
    CpR = np.hstack(caseArray[4][1])
    NR = np.hstack(caseArray[4][3])
    Coefs = np.hstack(caseArray[4][4])

    CoefsR = np.hstack(Coefs[np.size(CpF):np.size(Coefs)])
    return np.sum(CpR*CoefsR*Area*NR)