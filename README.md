# kmeans-demo

Tested with Python 3.x;

others interpreter versions may not run the code correctly

This zip file contains:

- a folder "Animations" containing animations to run on matlab using the "movie(x,10,1)" command after importing files to its workspace.
- a src folder containing python source codes.
- this read me! file.

Code organization:

the code is split into 2 modules, 
- inout.py: containing major functions
	- read/write data to files
	- calculate distances
	- generate random data
	- calculate center of gravity
	- calculate quality indexes
	- writing m-files: for 2D and 3D data sets
	  (to plot IRIS DATA modify the function as 
		described in its comments)
- The other is a main app for test cases:


there are two folders in the "src" folder:

- src/runs: containing Matlab plotters (for 2D & 3D plots) runnable m-files (generated with python code inout.write_matlab())
- src/data: containing data (observations and clusters and python outputted results)


The main application offers many options:

0- using an existing data file or generate a random set of data
1- predefine k number of clusters
2- apply or not the stop condition of the algorithm
3- the distance type (euclidian or manhattan)

all this in an interactive manner!


