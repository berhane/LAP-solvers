The data types for the random matrix elements could potentially be exploited to solve the linear
assignment problem more quickly.

The generated random matrix has floating point elements between 0 and 1, which are multiplied by the size of the matrix (`matrix_size`).
``cost_matrix1 = matrix_size * np.random.random((matrix_size, matrix_size))``

Then the data type is recast.
``cost_matrix=cost_matrix1.astype(np._DTYPE_)``

The data types supported by NumPy are listed below.

where `__DTYPE__` is

|`__DTYPE__` 	 | Description | Tested ? |
|:-----------:|------------------|:----------|
|intc | 	Identical to C int (normally int32 or int64) |  |
|int8  |	Byte (-128 to 127) |  |
|int16 |	Integer (-32768 to 32767) | tested |
|int32 |	Integer (-2147483648 to 2147483647) | tested |
|int64 |	Integer (-9223372036854775808 to 9223372036854775807) | tested |
|uint8 |	Unsigned integer (0 to 255) | tested  |
|uint16 |	Unsigned integer (0 to 65535) | tested  |
|uint32 | 	Unsigned integer (0 to 4294967295) |tested   |
|uint64 | 	Unsigned integer (0 to 18446744073709551615) |tested |
|float  |	Shorthand for float64. | tested/default |
|float16 |	Half precision float: sign bit, 5 bits exponent, 10 bits mantissa |tested  |
|float32 |	Single precision float: sign bit, 8 bits exponent, 23 bits mantissa | tested |
|float64 |	Double precision float: sign bit, 11 bits exponent, 52 bits mantissa | tested/default |

The tested modules are:

|  Module                             | Python or C/C++/Cython  | Algorithm     |
|-------------------------------------|:-----------------------:|:--------------|
|scipy.optimize.linear_sum_assignment |          Python         | Hungarian     |
|munkres.Munkres                      |          Python         | Hungarian     |
|hungarian.lap                        |          C++            | Hungarian     |
|lap.lapjv                            |          C++            | Jonker-Volgenant     |
|lapjv.lapjv                          |          C++            | Jonker-Volgenant     |
|lapsolver.solve_dense                |          C++            | shortest augmenting path     |

# Takeaways
The figures in this directory show that using smaller data types
* degrades the performance of Python LAP solvers (`munkres`, `SciPy`)
* has virtually no effect on the performance of C/C++-based solvers

These findings are likely machine-dependent. For the record, these tests were run using Python 3.7.1 on a 2013 MacPro with a 3.5 GHz Intel Xeon E5-1650v2 processor and 32GB of RAM.
