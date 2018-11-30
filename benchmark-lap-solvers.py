#!/usr/bin/env python2.7
#
# Tests the performance of linear assignment problem solvers for cost matrices
# of different sizes.  In particular, we'll be comparing
# 1) linear_sum_assignment - version provided in scipy
# 2) munkres - a Python implementation provided by Brian Clapper (https://github.com/bmc/munkres)
# 3) hungarian - a wrapper to a C++ implementation Knuth's Hungarian \
#        algorithm provided by Harold Cooper at https://github.com/Hrldcpr/Hungarian
# 4) munkres - a Python implementation provided by Brian Clapper (https://github.com/bmc/munkres)
#
# They all formally have O(n^3) complexity, but their performance differs substantially based on
# their implementation.

import numpy as np
import time
import munkres
from scipy.optimize import linear_sum_assignment
from scipy.optimize import curve_fit
import hungarian
import lap
import matplotlib.pyplot as plt

def main():
    base = 2        # will build matrices of size base^n
    min = 5         # 2^min =  8x8 cost matrix
    max = 12         # 2^max       
    #The size of the matrix to be solved is limited to 2^{limit['method']}
    limit = {}
    limit['lapjv'] = max
    limit['hungarian'] = max
    limit['scipy'] = 9 
    limit['munkres'] = 7
    print limit
    n_cycles = 3     # will run for n_cycles and average the timing information
    methods = ["lapjv", "hungarian", "scipy", "munkres"]  
    t_methods = ["t_" + i for i in methods]  
    label_methods = ["label_" + i for i in methods]  
    run_methods = ["run_" + i for i in methods]  
    #print methods
    for i in range(len(methods)):
        #print i
        t_methods[i] = np.empty((0,2),float)
        #print t_methods[i]
    #t_methods[0] = np.append(t_methods[0], np.array([[10, 10]]), axis=0)
    #print t_methods[0]

    for i in range(min,max):
        matrix_size = pow(base,i)
        print matrix_size
        temp_methods = np.zeros(len(methods),float)
        for j in range(n_cycles):
            cost_matrix = np.random.random((matrix_size, matrix_size))
            #print "n_cycles = " + str(j)
            for method in range(len(methods)):
                #print '%20s\t' %(methods[method])
                if methods[method] == 'munkres' and i <= limit[methods[method]]:
                    temp_methods[method] += run_munkres(cost_matrix)
                    #print temp_methods[method] 
                elif methods[method] == 'scipy' and i <= limit[methods[method]]:
                    temp_methods[method] += run_scipy(cost_matrix)
                    #print temp_methods[method] 
                elif methods[method] == 'hungarian' and i <= limit[methods[method]]:
                    temp_methods[method] += run_hungarian(cost_matrix)
                    #print temp_methods[method] 
                elif methods[method] == 'lapjv' and i <= limit[methods[method]]:
                    temp_methods[method] += run_lapjv(cost_matrix)
                    #print temp_methods[method] 
                else: 
                    print ""

        for method in range(len(methods)):
            if temp_methods[method] != 0:   # to make sure there is timing information
                t_methods[method] = np.append(t_methods[method], np.array([[matrix_size, temp_methods[method]/n_cycles]]), axis=0)
                #print methods[method]
                #print t_methods[method]

    for method in range(len(methods)):
        print methods[method]
        print t_methods[method]
        x=t_methods[method][:,[0]]
        x=x.flatten()
        y=t_methods[method][:,[1]]
        y=y.flatten()
        popt, pcov = curve_fit(lambda t,a,b: a+b*t, np.log(x), np.log(y))
        label_methods[method] = str(methods[method]) + ' scaling = ' + str(round(popt[1],2))
        plt.scatter(t_methods[method][:,[0]],t_methods[method][:,[1]],label=label_methods[method])
        plt.loglog(t_methods[method][:,[0]],t_methods[method][:,[1]],basex=base,basey=10)
    
    plt.grid(True,which="both")
    plt.xlabel('Matrix size (2^n x 2^n)')
    plt.ylabel('Real time to solution (sec)')
    plt.title('Time to solve LAPs using different modules')
    plt.legend()
    plt.show()

# Solve LAP using different methods
#LAPJV
def run_lapjv(matrix):
    t_start=time.time()
    cost, x, y = lap.lapjv(matrix)
    #print x
    t_end=time.time()
    return t_end-t_start

#Hungarian
def run_hungarian(matrix):
    t_start=time.time()
    h, m = hungarian.lap(matrix)
    #print h
    t_end=time.time()
    return t_end-t_start

#Scipy-linear_sum_assignment
def run_scipy(matrix):
    t_start=time.time()
    s,n = linear_sum_assignment(matrix)
    #print n
    t_end=time.time()
    return t_end-t_start

#Munkres
def run_munkres(matrix):
    t_start=time.time()
    u = munkres.Munkres()
    perm = u.compute(matrix)
    #print perm
    t_end=time.time()
    return t_end-t_start

if __name__ == "__main__":
    main()
