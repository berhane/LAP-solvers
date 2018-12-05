#!/usr/bin/env python3
#
# Tests the performance of linear assignment problem solvers for cost matrices
# of different sizes.  In particular, we'll be comparing
# 1) linear_sum_assignment - version provided in scipy
#    https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html
# 2) munkres - a Python implementation provided by Brian Clapper
#   https://github.com/bmc/munkres
# 3) hungarian - a wrapper to a C++ implementation Knuth's Hungarian algorithm provided by Harold Cooper
#   https://github.com/Hrldcpr/Hungarian
# 4) lap.lapjv - a wrapper to a C++ implementation of Jonker-Volgenant algorithm provided by Tomas Kazmar
#   https://github.com/gatagat/lap)
#
# They all formally have O(n^3) complexity, but their performance differs substantially based on
# their implementation.

import time
import argparse
import numpy as np
import munkres
from scipy.optimize import linear_sum_assignment
from scipy.optimize import curve_fit
import hungarian
import lap
import lapjv
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def main():

    # Parse arguments and provide usage information
    description = """
    Benchmarks the performance of linear assignment problem solvers for random cost matrices
    of different dimensions.
    """
    epilog = """
    The script  will produce the following:
    1) data of timing for LAP solving random cost matrices of dimensions 2^{min} - 2^{max}
    2) plot of timing for LAP solving random cost matrices of dimensions 2^{min} - 2^{max}
    """
    parser = argparse.ArgumentParser( description=description, formatter_class=argparse.RawDescriptionHelpFormatter,epilog=epilog)
    parser.add_argument('--min', metavar='min', nargs='?', type=int, default=8, \
           help='minimum dimension of cost matrix to solve. The default is 8 (2^3 x 2^3)')
    parser.add_argument('--max', metavar='max', nargs='?', type=int, default=4096, \
           help='maximum dimension of cost matrix to solve. The default is 4096 (2^12 x 2^12)')
    parser.add_argument('--ncyc', metavar='n_cycles', nargs='?', type=int, default=3, \
           help='number of times to solve cost matrices and average their timing. The default is 3 cycles')
    args = parser.parse_args()

    base = 2                                    # will build matrices of size base^n
    min = int(np.ceil(np.log2(args.min)))      # 2^min =  8x8 cost matrix
    max = int(np.ceil(np.log2(args.max)))      # 2^max
    # The size of the matrix to be solved is limited to 2^{limit['method']}
    # for each method to ensure quick termination of the benchmarking exercise.
    # unkres and Scipy are considerably slower, making it necessary to limit them to smaller
    # matrices

    # METHODS 
    methods = ["lap_lapjv", "lapjv_lapjv", "hungarian", "scipy", "munkres"]
    limit = {}
    limit['lap_lapjv'] = max
    limit['lapjv_lapjv'] = max
    limit['hungarian'] = max
    limit['scipy'] = 9
    limit['munkres'] = 7
    print("Solving matrices of sizes up to limit 2^{n} where n is " + str(limit))
    n_cycles = 3     # will run for n_cycles and average the timing information
    t_methods = ["t_" + i for i in methods]
    label_methods = ["label_" + i for i in methods]
    run_methods = ["run_" + i for i in methods]
    #print methods
    for i in range(len(methods)):
        t_methods[i] = np.empty((0,2),float)
        #print t_methods[i]
    for i in range(min,max):
        matrix_size = pow(base,i)
        print(str(matrix_size) + " x " + str(matrix_size))
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
                elif methods[method] == 'lap_lapjv' and i <= limit[methods[method]]:
                    temp_methods[method] += run_lap_lapjv(cost_matrix)
                    #print temp_methods[method]
                elif methods[method] == 'lapjv_lapjv' and i <= limit[methods[method]]:
                    temp_methods[method] += run_lapjv_lapjv(cost_matrix)
                    #print temp_methods[method]
                else:
                    pass

        # average the timing information from n_cycles
        for method in range(len(methods)):
            if temp_methods[method] != 0:   # to make sure there is timing information
                t_methods[method] = np.append(t_methods[method], np.array([[matrix_size, temp_methods[method]/n_cycles]]), axis=0)

    # print timing information to screen
    np.set_printoptions(suppress=True,precision=5)
    print('%10s '  % ("Matrix size"), end=" ")
    x=t_methods[0][:,[0]]
    x=x.flatten()
    print(x)
    for method in range(len(methods)):
        print('%10s '  % ( methods[method]),end=" ")
        y=t_methods[method][:,[1]]
        y=y.flatten()
        print(y)

    # generate plot
    fig, ax = plt.subplots()
    for method in range(len(methods)):
        plt.scatter(t_methods[method][:,[0]],t_methods[method][:,[1]],label=methods[method])
        plt.loglog(t_methods[method][:,[0]],t_methods[method][:,[1]],basex=2,basey=10)

    plt.grid(True,which="both")
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    plt.xlabel('Matrix dimension (2^n)', fontsize=18)
    plt.ylabel('Real time to solution (seconds)',fontsize=18)
    plt.title('Time to solve LAPs using different modules',fontsize=20)
    plt.legend(fontsize=14)
    plt.show()

# Solve LAP using different methods
#LAP.LAPJV
def run_lap_lapjv(matrix):
    t_start=time.time()
    cost, x, y = lap.lapjv(matrix)
    #print x
    t_end=time.time()
    return t_end-t_start

#LAPJV.LAPJV
def run_lapjv_lapjv(matrix):
    t_start=time.time()
    x, y, _ = lapjv.lapjv(matrix)
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
