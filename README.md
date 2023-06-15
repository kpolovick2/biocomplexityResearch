This repo is the research base of a small group of researchers at the Biocomplexity Research Institute of the University of Virginia.
It contains research about and surrounding the minimum descriptor problem for multiple clusters.
This repo uses Gurobi, a mathematical solver, to solve the minimum descriptor problem for singular and multiple clusters through integer linear programming.

There are multiple important directories, however the main directories that should be viewed are as follows:
- data_parsing
  - code to parse input from properly formatted real world datasets
- polynomial_add
  novel, original heuristic algorithms for calculating minimum descriptors
- UCI datasets
  - datasets found in the UCI machine learning repository, [click here](https://archive.ics.uci.edu/) to learn more
- synthetic data generation
  - generators for synthetic datasets
- test_txt_files
  - testing datasets for the multiple cluster minimum descriptor problem (some handwritten, some programmatically generated)

There are two main solvers for this project - ILP_gurobi_generalized_concise.py and ILP_linear.py.
These two solvers have been thoroughly tested and were the fastest two solvers implemented in Gurobi.

Within the polynomial_add directory, we explore heuristic algorithms for adding tags to items and recomputing the minimum descriptor of one singular cluster.
There were multiple reductions written to show that there these algorithms are somewhat accurate heuristics.
This particular heuristic algorithm was chosen because it can be parallelized in mass using a GPU or multithreading for hardware acceleration,
making it significantly faster than integer linear programming.

As suggested by multiple proofs, it appears that any and all adjustments to the tags of a cluster are hard problems, meaning they cannot be accurately solved in polynomial time.
These results are in the process of being confirmed, and heuristics for these changes are being developed currently.
