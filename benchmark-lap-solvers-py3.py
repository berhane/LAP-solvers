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
#   https://github.com/gatagat/lap
# 5) lapjv.lapjv - a wrapper to a C++ implementation of Jonker-Volgenant algorithm re-written for Python 3 by source{d}
#    https://github.com/src-d/lapjv
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
import inspect

def func_name():
   print(inspect.stack()[0][1])

def main():

    # METHODS being benchmarked -- Add new METHOD[S] here
    methods = ["lap_lapjv", "lapjv_lapjv", "hungarian", "scipy", "munkres"]
    min = int(np.floor(np.log2(args.min)))      # 2^min =  8x8 cost matrix
    max = int(np.ceil(np.log2(args.max)))      # 2^max
    ncyc = int(args.ncyc)                      # number of cycle

    #ncyc = 3     # will run for ncyc and average the timing information

    # LIMITS - add limit for new METHOD[S] here
    # The size of the matrix to be solved is limited to 2^{limit['method']}
    # for each method to ensure quick termination of the benchmarking exercise.
    # unkres and Scipy are considerably slower, making it necessary to limit them to smaller
    # matrices
    limit = {}
    limit['munkres'] = 7
    limit['scipy'] = 9
    limit['hungarian'] = max
    limit['lap_lapjv'] = max
    limit['lapjv_lapjv'] = max
    print("Solving matrices of sizes up to limit 2^{n} where n is " + str(limit))

    # arrays to store data
    t_methods = ["t_" + i for i in methods]
    for i in range(len(methods)):
        t_methods[i] = np.empty((0,2),float)
    label_methods = ["label_" + i for i in methods]
    run_methods = ["run_" + i for i in methods]

    base = 2                          # will build matrices of size base^n and solve them

    #for matrices of size 2^{min} - 2^{max}
    for i in range(min,max):
        matrix_size = pow(base,i)
        #print(("\n" +  str(matrix_size) + " x " + str(matrix_size) + " ... cycle ") ,end=" ")
        print(("\n" +  str(matrix_size) + " x " + str(matrix_size) + " ... cycle "))
        temp_methods = np.zeros(len(methods),float)
        #Generate n_cyc random matrices and solve them using different methods
        for j in range(ncyc):
            #cost_matrix = matrix_size*np.random.random((matrix_size, matrix_size))
            cost_matrix = np.random.random((matrix_size, matrix_size))
            #print((str(j) + " "), end=" ")
            print("Cycle ", (str(j) + " "))
            #print("\n")
            #print(cost_matrix)
            for method in range(len(methods)):
                #print '%20s\t' %(methods[method])
                if methods[method] == 'munkres' and i <= limit[methods[method]]:
                    temp_methods[method] += run_munkres(cost_matrix, args.printcost)
                    #print temp_methods[method]
                elif methods[method] == 'scipy' and i <= limit[methods[method]]:
                    real_time = run_scipy(cost_matrix, args.printcost)
                    temp_methods[method] += real_time
                    #print temp_methods[method]
                elif methods[method] == 'hungarian' and i <= limit[methods[method]]:
                    temp_methods[method] += run_hungarian(cost_matrix, args.printcost)
                    #print temp_methods[method]
                elif methods[method] == 'lap_lapjv' and i <= limit[methods[method]]:
                    temp_methods[method] += run_lap_lapjv(cost_matrix, args.printcost)
                    #print temp_methods[method]
                elif methods[method] == 'lapjv_lapjv' and i <= limit[methods[method]]:
                    temp_methods[method] += run_lapjv_lapjv(cost_matrix, args.printcost)
                    #print temp_methods[method]
                    # If you want to benchmark a new METHOD, add another ELIF statement here
                else:
                    pass

        # average the timing information from n_cyc cycles
        for method in range(len(methods)):
            if temp_methods[method] != 0:   # to make sure there is timing information
                t_methods[method] = np.append(t_methods[method], np.array([[matrix_size, temp_methods[method]/ncyc]]), axis=0)

    # print timing information to screen
    dimensions=t_methods[0][:,[0]]
    dimensions=dimensions.flatten()
    print("\n")
    print("%12s "  % ("Matrix_size"), end=" ")
    np.set_printoptions(suppress=True,precision=5,linewidth=100)
    for i in range(len(dimensions)):
        print('%6d '  % (dimensions[i]), end=" ")
    print(" ")

    np.set_printoptions(suppress=True,precision=5,linewidth=100)
    for method in range(len(methods)):
        print('%12s '  % ( methods[method]), end=" ")
        timings=t_methods[method][:,[1]]
        timings=timings.flatten()
        print(timings)

    # generate a plot (by default), unless 'no plot' option is selection
    if args.noplot:
        pass
    else:
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
#LAPJV
def run_lap_lapjv(matrix, printlowestcost):
    t_start=time.time()
    lowest_cost, row_ind, column_ind = lap.lapjv(matrix)
    t_end=time.time()

    if printlowestcost:
        #func_name()
        print("%18s    %5.3f" % ("lap_lapjv_cost", lowest_cost))

        if args.verbose:
            '''
            #print(" row_ind = ", row_ind)
            #print(" col_ind = ", column_ind)
            print(" lap_lapjv cost = ", cost)
            '''
            lowest_cost = 0.00
            for i in range(len(row_ind)):
                lowest_cost += matrix[i,row_ind[i]]
                print(" ", lowest_cost)

    del row_ind; del column_ind
    return t_end-t_start

#LAPJV.LAPJV
def run_lapjv_lapjv(matrix, printlowestcost):
    t_start=time.time()
    row_ind, column_ind, _ = lapjv.lapjv(matrix)
    t_end=time.time()
    if printlowestcost:
        #func_name()
        lowest_cost=0.00
        for i in range(len(row_ind)):
            lowest_cost += matrix[i,row_ind[i]]
            if args.verbose:
                print(" ", lowest_cost)
        print("%18s    %5.3f" % ("lapjv_lapjv_cost", lowest_cost))

    del row_ind; del column_ind
    return t_end-t_start

#Hungarian
def run_hungarian(matrix, printlowestcost):
    t_start=time.time()
    hung_mat = np.copy(matrix)
    row_ind, column_ind = hungarian.lap(hung_mat)
    t_end=time.time()

    if printlowestcost:
        #func_name()        #func_name()
        lowest_cost=0.00
        for i in range(len(row_ind)):
            lowest_cost += matrix[i,row_ind[i]]
            if args.verbose:
                print(" ", lowest_cost)
        print("%18s    %5.3f" % ("Hungarian_cost", lowest_cost))

    del row_ind; del column_ind
    return t_end-t_start

#Scipy-linear_sum_assignment
def run_scipy(matrix, printlowestcost):
    t_start=time.time()
    row_ind, column_ind = linear_sum_assignment(matrix)
    t_end=time.time()

    if printlowestcost:
        #func_name()
        lowest_cost=0.00
        lowest_cost= matrix[row_ind, column_ind].sum()
        print("%18s    %5.3f" % ("Scipy_cost", lowest_cost))

    del row_ind; del column_ind
    return t_end-t_start

#Munkres
def run_munkres(matrix, printlowestcost):
    t_start=time.time()
    munk_mat = np.copy(matrix)
    m = munkres.Munkres()
    indices = m.compute(matrix)
    t_end=time.time()

    if printlowestcost:
        #func_name()
        columns = [x[1] for x in indices]
        lowest_cost=0.00
        for i in range(len(columns)):
            lowest_cost += munk_mat[i,columns[i]]
            if args.verbose:
                print(" ", lowest_cost)
        print("%18s    %5.3f" % ("Munkres_cost", lowest_cost))

    del indices
    return t_end-t_start

#NEW METHOD
#Add function run_METHOD to get timing for method that method

if __name__ == "__main__":
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
    parser.add_argument('-c', '--printcost', action='store_true', help='Print the minimum cost.\
           The default is false, i.e. will not print the minmum cost')
    parser.add_argument('-v', '--verbose', action='store_true', help='Determines verbosity. \
           The default is minimal printing, i.e. not verbose')
    parser.add_argument('-np', '--noplot', action='store_true', help='Plot data using matplotlib. \
           The default is true, i.e. generate plot')
    parser.add_argument('--min', metavar='min', nargs='?', type=int, default=8, \
           help='minimum dimension of cost matrix to solve. \
           The default is 8 (2^3 x 2^3)')
    parser.add_argument('--max', metavar='max', nargs='?', type=int, default=4096, \
           help='maximum dimension of cost matrix to solve. \
           The default is 4096 (2^12 x 2^12)')
    parser.add_argument('--ncyc', metavar='ncyc', nargs='?', type=int, default=3, \
           help='number of times to solve cost matrices and average their timing. \
           The default is 3 cycles')
    args = parser.parse_args()

    main()
