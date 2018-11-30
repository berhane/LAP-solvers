# Purpose

The script benchmarks the performance of four linear assignment problem solvers
for cost matrices of different sizes.  These solvers are:

* **linear_sum_assignment** - version provided in scipy
* **munkres** - a Python implementation provided by Brian Clapper (https://github.com/bmc/munkres)
* **hungarian** - a wrapper to a C++ implementation Knuth's Hungarian algorithm provided by Harold Cooper at https://github.com/Hrldcpr/Hungarian
* **munkres** - a Python implementation provided by Brian Clapper (https://github.com/bmc/munkres)

 They all formally have O(n^3) complexity, but their performance differs substantially based on
 their implementation.

ArbAlign is a small tool for optimally aligning two arbitrarily ordered isomers using the
Hungarian or Kuhn-Munkres algorithm. The final ordering of the two isomers should give the lowest
root mean-square distance (RMSD) between the two structures.

# Contents
The repo contains the following items:
* benchmark-lap-solvers.py - a Python script

# Usage
It's simple once you have installed the necessary packages.

Usage: `benchmark-lap-solvers.py`


# Requirements
## Python 2.7+
* Python Numpy module. If you don't have it already, you can install it using `pip`
 * `pip install numpy`
* Python Hungarian module by Harold Cooper
  * Hungarian: Munkres' Algorithm for the Linear Assignment Problem in Python (https://github.com/Hrldcpr/Hungarian)
  * This is a wrapper to a fast C++ implementation of the Kuhn-Munkres algorithm. The installation instructions are described clearly at https://github.com/Hrldcpr/Hungarian.
  * In short, one would need to go into the `hungarian` directory and
    * `python setup.py build`  
    * `python setup.py install`
    * You would either want to copy the file `build/lib-XXX/hungarian.so` into a location that's
      included in your `$PYTHONPATH` or whatever directory you are running ArbAlign from.
* Alternatively, you can use Brian Clapper's Munkres module or another similar module includeded in SciNumpy. This could require you to make small changes to the current script. We'll provide an version that uses SciNumpy's Munkres module at a later time.

## Other Tools Needed to Align by Atom Type or Connectivity
* OpenBabel - We use OpenBabel to convert Cartesian coordinates (XYZ) to formats containing atmm types including connectivity and hybridization information. It is necessary to use OpenBabel to convert the Cartesian coordinates to SYBYL Mol2 (sy2) and MNA (mna) formats.
* genTypes.csh - a small shell script which converts XYZ file to SYBYL Mol2 (sy2) format and recasts the atom label to contain atom type information.
* genConn.csh - a small shell script which converts XYZ file to NMA (nma) format and recasts the atom label to contain atom's bonding/connectivity information.


# Output
If the pairs of structures pass a sanity test, the tool will align them optimally and provide the
following information.
* The initial Kabsch RMSD,
* The Kuhn-Munkres reorderings for each atom and the corresponding RMSDs,
* The final Kabsch RMSD after the application of the Kuhn-Munkres algorithm, and
* The coordinates corresponding to the best alignment of the second structure with the first.

# Citation
If you find this tool useful for any publishable work, please cite the companion paper:

Berhane Temelso, Joel M. Mabey, Toshiro Kubota, Nana Appiah-padi, George C. Shields.  `J. Chem. Info. Model.` **2017**, 57 (5), 1045–1054

http://doi.org/10.1021/acs.jcim.6b00546
