import csv
import sys
import numpy as np
import random
from R2checking import *

polySum=[0]
for polynomialOrder in range(1,16):
    polySum.append(0.0)
    for runStep in range(1,26):
        polySum[polynomialOrder]+=getRsquared("EUR_USD_5M.csv",polynomialOrder)
        print(str(polynomialOrder)+":"+str(runStep))
for polynomialOrder in range(1,16):
    print("For polyOrder "+str(polynomialOrder)+":we have R2 of: "+str(polySum[polynomialOrder]/26))
