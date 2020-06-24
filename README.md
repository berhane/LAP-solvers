# Purpose

The script benchmarks the performance of Python3 linear assignment problem solvers for random cost matrices of different sizes.  These solvers are:

* **linear_sum_assignment** - a Python implementation of the Hungarian algorithm provided in SciPy
  * https://github.com/scipy/scipy/
* **munkres** - a Python implementation of the Hungarian algorithm provided by Brian Clapper
  * https://github.com/bmc/munkres
* **hungarian** - a wrapper to a C++ implementation Knuth's Hungarian algorithm provided by Harold Cooper
  * does not work with Python 3.6 and 3.7 
  * https://github.com/Hrldcpr/Hungarian
* **lap.lapjv** - a wrapper to a C++ implementation of Jonker-Volgenant algorithm provided by Tomas Kazmar
  * https://github.com/gatagat/lap
  In addition, these two solvers are added for Python3
* **lapjv.lapjv** - a wrapper to a C++ implementation of Jonker-Volgenant algorithm re-written for Python 3 and optimized to take advantage of AVX2 instruction sets by Vadim Markovtsev at src{d}.
  * Please see the [blog post here](https://blog.sourced.tech/post/lapjv/)
  * https://github.com/src-d/lapjv  
* **lapsolver** - implementation for dense matrices based on shortest path augmentation by Christoph Heindl.
  * Please note that Christioph has also done a [benchmark of LAP solvers](https://github.com/cheind/py-lapsolver/tree/master/lapsolver/benchmarks)
  * https://github.com/cheind/py-lapsolver      
* **laptools.clap** - new python implementation
  * https://github.com/jdmoorman/laptools      

They all formally have O(n<sup>3</sup>) complexity, but their performance differs substantially based on their implementation and the size of the matrix they are trying to solve. The solvers can be classified based on some unique characteristics.

|  Module                             | Python or C/C++/Cython  | Algorithm     |
|-------------------------------------|:-----------------------:|:--------------|
|scipy.optimize.linear_sum_assignment | Python(<v1.4)/C++(=>v1.4))  | Hungarian     |
|munkres.Munkres                      |          Python         | Hungarian     |
|laptools.clap                        |          Python         | ?     |
|hungarian.lap                        |          C++            | Hungarian     |
|lap.lapjv                            |          C++            | Jonker-Volgenant     |
|lapjv.lapjv                          |          C++            | Jonker-Volgenant     |
|lapsolver.solve_dense                |          C++            | shortest augmenting path     |

The purpose of this benchmarking exercise is to see which implementation performs best for a given matrix size. My interest is to use this information to improve the performance of [Arbalign](https://github.com/berhane/arbalign) and expand its use.

# Contents
The repo contains the following:
* `benchmark-lap-solvers.py` - a Python3 script comparing four/six implementations
* `benchmark-lap-solvers-py3.ipynb` - a Jupyter notebook comparing four/six implementations. It has
  been tested using Python 3.6 and 3.7.

# Usage
It's simple once you have installed the necessary packages.

```
Usage: benchmark-lap-solvers.py [-h] [-c] [-v] [-np] [-sp] [--min [min]]
                                    [--max [max]] [--ncyc [ncyc]]

    Benchmarks the performance of linear assignment problem solvers for
    random cost matrices of different dimensions.


optional arguments:
  -h, --help       show this help message and exit
  -c, --printcost  Print the minimum cost. The default is false, i.e. will not
                   print the minimum cost
  -v, --verbose    Determines verbosity. The default is minimal printing, i.e.
                   not verbose
  -np, --noplot    Do not plot data using matplotlib. The default is to save
                   plot of the data in PNG format, but not open the plot GUI
  -sp, --showplot  Show plot of data using matplotlib. The default is to save
                   plot of the data in PNG format, but not open the plot GUI
  --min [min]      minimum dimension of cost matrix to solve. The default is 8
                   (2^3 x 2^3)
  --max [max]      maximum dimension of cost matrix to solve. The default is
                   4096 (2^12 x 2^12)
  --ncyc [ncyc]    number of times to solve cost matrices and average their
                   timing. The default is 3 cycles

    The script  will produce the following:
    1) data of timing for LAP solving random cost matrices of
    dimensions 2^{min} - 2^{max}
    2) plot of timing for LAP solving random cost matrices of
    dimensions 2^{min} - 2^{max}
```

## Examples
| command   |      execution    |  note     |
|----------|:-------------:|:-------|
| `python3 ./benchmark-lap-solvers.py` | `python3 ./benchmark-lap-solvers.py --ncyc 3 --min 8 --max 4096` | default |
| `python3 ./benchmark-lap-solvers.py --min 2 --max 512` | `python3 ./benchmark-lap-solvers.py --ncyc 3 --min 2 --max 512` | default, except it looks at small matrices only |
| `python3 ./benchmark-lap-solvers.py -np` | `python3 ./benchmark-lap-solvers.py --ncyc 3 --min 8 --max 4096 -np` | default, except plotting is suppressed |
| `python3 ./benchmark-lap-solvers.py --printcost` | `python3 ./benchmark-lap-solvers.py --ncyc 3 --min 8 --max 4096 --printcost` | default, except it prints lowest cost for each method |

If you want to add other solvers to the list, it should be easy to figure out what parts to update in the scripts.

# Requirements
* `numpy` module. If you don't have it already, you can install it using `pip3` or `conda`. Most of the packages should be available in the default Conda channels/repos, but you may have to search a little harder for others.
  * `pip3 install numpy`
  * `conda install numpy`
* `matplotlib` module
  * `pip3 install   matplotlib`
  * `conda install matplotlib`
* scipy module (install version 1.4+ with Python 3.5+ for a fast C++ implementation)
  * `pip3 install  scipy==1.4`
  * `conda install scipy`
* `munkres` module by Brian Clapper.
   * `pip3 install munkres`
   * `conda install munkres`
* `hungarian` module by Harold Cooper (does not work with Python 3.5+)
  * `pip3 install   hungarian`
  * `conda install -c psi4 hungarian`
* `lap` module by Tomas Kozmar.
  * `pip3 install lap`
  * `conda install lap`
* `lapjv` module by src{d} for Python3
  * `pip3 install lapjv`
* `lapsolver` module by Christoph Heindl
    * `pip3 install lapsolver`
    * `conda install -c loopbio lapsolver `
* `laptoools` module by jdomoorman
    * `pip3 install laptools` (Python 3.5+)

# Output
The script will produce output similar to what's shown below. Some things to note are:
* The timings here corresponds to an average of three Python 3.5.6 runs on CentOS 7 machine with 2.4 GHz Intel Xeon Gold 6148 processor and 192GB of RAM
* The random matrices are filled with floating point numbers ranging from 0 to the size (# of rows or columns) of the matrix. They are generated using numpy: `cost_matrix = matrix_size * np.random.random((matrix_size, matrix_size))`

<!--
## Python2
* Data of timing for solving LAP of random cost matrices of sizes 2<sup>min</sup> x 2<sup>min</sup>  to 2<sup>max</sup> x 2<sup>max</sup>.
<pre>
Solving matrices of sizes up to limit 2^{n} where n is {'munkres': 7, 'scipy': 9, 'hungarian': 13, 'lap.lapjv': 13}
8 x 8
16 x 16
32 x 32
64 x 64
128 x 128
256 x 256
512 x 512
1024 x 1024
2048 x 2048
4096 x 4096
Matrix size  [   8      16       32      64     128     256     512     1024    2048   4096]
     lapjv  [0.00007 0.00003 0.00004 0.00008 0.00022 0.00149 0.00574 0.03733 0.22209  1.14318]
 hungarian  [0.00001 0.00001 0.00002 0.00011 0.00066 0.00472 0.03157 0.21561 1.71368 14.11281]
     scipy  [0.0004  0.00044 0.00086 0.00353 0.01809 0.10358 1.01071]
   munkres  [0.00033 0.00091 0.00445 0.03216 0.25957]
   Figure saved to file timings-LAPs-py2-8-8192.png
</pre>
* plot of timing for LAP solving random cost matrices of sizes 2<sup>min</sup> x 2<sup>min</sup>  to 2<sup>max</sup> x 2<sup>max</sup>, where *min* and *max* are limited to smaller numbers for `munkres` and `scipy` in the interest of time.
![alt text](images/figure-py2.png "Python2 benchmark test")
If requested via the `--printcost` flag, it will also print the minimum cost for each random cost matrix by each implementation. This test ensures that the methods are making consistent/correct assignments.
<pre>
8 x 8 ... cycle
('Cycle ', '0 ')
    lap_lapjv_cost    10.649
    Hungarian_cost    10.649
        Scipy_cost    10.649
      Munkres_cost    10.649
('Cycle ', '1 ')
    lap_lapjv_cost    10.399
    Hungarian_cost    10.399
        Scipy_cost    10.399
      Munkres_cost    10.399
('Cycle ', '2 ')
    lap_lapjv_cost    7.654
    Hungarian_cost    7.654
        Scipy_cost    7.654
      Munkres_cost    7.654
.
.
.
2048 x 2048 ... cycle
('Cycle ', '0 ')
    lap_lapjv_cost    3388.642
    Hungarian_cost    3388.642
('Cycle ', '1 ')
    lap_lapjv_cost    3269.750
    Hungarian_cost    3269.750
('Cycle ', '2 ')
    lap_lapjv_cost    3424.101
    Hungarian_cost    3424.101      
</pre>
-->

* Data of timing for solving LAP of random cost matrices of sizes 2<sup>min</sup> x 2<sup>min</sup>  to 2<sup>max</sup> x 2<sup>max</sup>.
<pre>
Solving matrices of sizes up to 2^{n} where n is {'lapsolver': 15, 'lap_lapjv': 15, 'munkres': 7, 'hungarian': 12, 'lapjv_lapjv': 15, 'scipy': 15}

8 x 8 ... 

Cycle  0   lapjv_lapjv  lap_lapjv  scipy  lapsolver  hungarian  munkres
Cycle  1   lapjv_lapjv  lap_lapjv  scipy  lapsolver  hungarian  munkres
Cycle  2   lapjv_lapjv  lap_lapjv  scipy  lapsolver  hungarian  munkres

.
.
.

16384 x 16384 ... 

Cycle  0   lapjv_lapjv  lap_lapjv  scipy  lapsolver  
Cycle  1   lapjv_lapjv  lap_lapjv  scipy  lapsolver  
Cycle  2   lapjv_lapjv  lap_lapjv  scipy  lapsolver 


Package Versions for the current run
Python -  3.5.6 |Anaconda, Inc.| (default, Aug 26 2018, 21:41:56) 
[GCC 7.3.0]
lap  -  0.4.0
scipy  -  1.4.0
lapsolver  -  1.0.2
munkres  -  1.0.12


Matrix_size  [  8        16       32       64       128      256      512      1024     2048     4096      8192     16384
lapjv_lapjv  [  0.00001  0.00001  0.00002  0.00004  0.00011  0.00066  0.00659  0.02742  0.13955  0.74462   3.05277  14.64501]
lap_lapjv    [  0.00005  0.00003  0.00004  0.00006  0.00018  0.00104  0.00795  0.03303  0.15438  1.92253   7.41732  50.84391]
scipy        [  0.00006  0.00005  0.00008  0.00018  0.00067  0.0025   0.01355  0.06346  0.34247  1.88682   9.30888  52.81564]
lapsolver    [  0.00002  0.00001  0.00003  0.0001   0.00038  0.00214  0.01347  0.07315  0.40603  2.47342   12.3546  77.90600]
hungarian    [  0.00001  0.00001  0.00004  0.00013  0.00071  0.00429  0.03393  0.24279  1.87886  15.30685  ]
munkres      [  0.00049  0.00384  0.04524  0.34832  3.26252  ]

Figure saved to file timing-LAPs-py3-8-32768.png

<!--
### Timing from runs prior to scipy improvements
Matrix_size       8        16      32       64      128      256      512     1024     2048       4096       8192     16384
  lap_lapjv  [ 0.0003   0.00005  0.00009  0.00013  0.00037  0.00224  0.00581  0.0702   0.24894  1.47379    9.61785   63.22643]
lapjv_lapjv  [ 0.00006  0.00001  0.00003  0.00006  0.00031  0.00231  0.00625  0.0755   0.29286  1.24798    5.49919   23.89383]
  lapsolver  [ 0.00003  0.00003  0.00007  0.00018  0.00064  0.00262  0.01298  0.07445  0.33587  2.33581   11.88771   67.10397]
  hungarian  [ 0.00001  0.00002  0.00004  0.00013  0.00085  0.00503  0.03316  0.22956  1.63596 15.02935  127.19425 1025.16906]
      scipy  [ 0.00088  0.00208  0.00881  0.02201  0.10714  0.58886  4.38091]
    munkres  [ 0.00075  0.00596  0.09011  0.66533  7.30088]
  Figure saved to file timings-LAPs-py3-8-16384.png
-->
</pre>


* plot of timing for LAP solving random cost matrices of sizes 2<sup>min</sup> x 2<sup>min</sup>  to 2<sup>max</sup> x 2<sup>max</sup>, where *min* and *max* are limited to smaller numbers for `munkres` and `scipy` in the interest of time.

![alt text](images/figure-py3.png "Python3 benchmark test")

If requested via the `--printcost` flag, it will also print the minimum cost for each random cost matrix by each implementation. This test ensures that the methods are making consistent/correct assignments.

# Takeaways

1. `scipy==1.4` is much faster than previous versions and it is competitive with the other implementations, especially for larger matrices. This is a great development since it probably gets used more than the other implementations by virtue of scipy's popularity.
2. `munkres` is much slower than `hungarian`, `lapsolver`, `scipy`, `lap.lapjv`, and `lapjv.lapjv` for all matrix sizes
3. `hungarian` performs well for smaller matrices. For anything larger than 256x256, `lapsolver`, `lap.lapjv` and `lapjv.lapjv` are about an order of magnitude faster than `hungarian`
4. `lap.lapjv` is am implementation intended to solve dense matrices. Its sparse matrix solver analog named `lap.lapmod` is more efficient for larger sparse matrices. Both are implemented in the `lap` module.
5. `lapjv.lapjv` has the best performance virtually for all matrix sizes.
6. For the purposes of improving [Arbalign](https://github.com/berhane/arbalign), `hungarian` remains a good choice for most molecular systems I'm interested in which don't have more than 100x100 distance matrices the same type to solve. However, if the tool is to be applied to larger molecules such as proteins and DNA, it would be worthwhile to use `lapjv.lapjv`, `lapsolver`, `lap.lapjv` or `lap.lapmod`
