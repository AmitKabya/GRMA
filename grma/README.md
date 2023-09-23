# GRMA - Graph-based Matching Algorithm

GRMA is a Python package for finding HLA (Human Leukocyte Antigen) matches using a graph-based approach. The matching is based on Grim's imputation.

## Example Usage

To use GRMA, follow these steps:

1. **Build Donors Graph**: Create a Donors Graph, which represents your HLA search space object.

    ```python
    from grma.matching import BuildDonorsGraph
    
    donors_file = 'data.txt'  # Path to your donors data
    results_directory = './results_directory'  # Directory to save results
    
    BuildDonorsGraph(donors_file, results_directory)
    ```

2. **Impute Patients' Genotypes**: Impute your patient's genotypes using Grim's algorithm. You can use the default settings or customize them by providing a Grim configuration file.

    ```python
    from grma.matching import GetResultPatients

    grim_config_file = 'minimal-configuration.json'  # Path to Grim configuration file
    donors_graph_file = 'data/donors_graph.pkl'  # Path to the Donors Graph pickle file
    result_directory = './result_dir'  # Directory to save results
    cutoff = 100  # Maximum number of matches to return
    threshold = 0.1  # Minimal score value for a valid match
    
    GetResultPatients(grim_config_file, donors_graph_file, result_directory, cutof=cutoff, threshold=threshold)
    ```
- grim_config_file: Example at "minimal-configuration.json" (need to add some files: freq_file, imputation_in_file). 
- donors_graph_file: Path to the Donors Graph pickle file.
- result_directory: Directory to save results.
- Threshold: Minimal score value for a valid match. Default is 0.1.
- Cutoff: Maximum number of matches to return. Default is 50.


## Building The Donors' Graph

The Donors' Graph is a representation of your HLA search space. It's implemented as a List of Lists (LOL) structure for improved time and memory efficiency. It's recommended to save the graph in a pickle file.

Before building the Donors' Graph, ensure that all donors' HLAs have been imputed using Grim and the imputation files are saved under the same directory.

## Imputing Patients' Genotypes

The `GetResultPatients` function applies both Grim and GRMA algorithms. It requires a path to a Grim configuration file with algorithm settings and a path to the data files. The Grim configuration file cannot be ignored, as Grim will use default settings otherwise.




## Requirements

- Python 3.x
- Pandas
- Numpy
- Cython
- tqdm
- setuptools
- cython
- networkx
- toml==0.10.2
- py-graph-imputation>=0.0.3



