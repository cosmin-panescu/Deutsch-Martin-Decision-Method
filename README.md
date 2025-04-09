
### Documentation for the Deutsch-Martin Method Project

**Author:** Cosmin Vasile Panescu

**Project Type:** Academic (University Project)

**Programming Language:** Python

**Dependencies:** NumPy, Pandas, OpenPyxl


### Introduction 

This repository contains an implementation of the Deutsch-Martin method, a specialized decision-making algorithm, written in Python. The project was developed as part of a university coursework to assist in ranking and optimizing decision alternatives based on multiple criteria.

### What is the Deutsch-Martin Method? 

The Deutsch-Martin method, also known as the moments method, is a decision-making technique used for ordering and categorizing decision-making alternatives. It iteratively calculates row and column moments to optimize the arrangement of alternatives and criteria until convergence is achieved. This method is particularly useful in multi-criteria decision-making (MCDM) scenarios.



### Features

1. **File Input Support**
- Reads data from Excel (.xlsx, .xls) and CSV files.
- Automatically detects the number of variants and criteria.
- Supports custom delimiters for CSV files.
2. **Manual Input Support**
- Allows users to manually input the number of variants and criteria.
- Enables direct entry of values for alternatives and criteria.
3. **Decision Optimization**
- Normalizes the input data matrix to ensure uniformity across criteria.
- Iteratively calculates row and column moments, optimizing their order for decision-making.
- Converges to a rank-ordered optimal arrangement of decision alternatives.


### Use Cases

This Python script can be used in scenarios such as:

- Decision-making in business or managerial contexts, based on performance indicators.
- Academic research in operational research or decision sciences.
- Multi-criteria analysis for selecting the best option among competing alternatives.


    
### Installation

Before running the script, ensure you have Python installed. Install the necessary Python libraries by running the following command:

```bash
  pip install numpy pandas openpyxl
```

### Usage Instructions
**Running the script**

- Save the script as **script.py**.
- Execute the script using the command:
```bash
  python script.py
```

**Input formats**

Ensure your file follows this format:

- **First column**: Names of the decision alternatives (variants).
- **First row**: Names of the criteria.
- **Remaining cells**: Values representing how each alternative scores according to each criterion


### Workflow and Algorithm Overview

1. **Input Data:**
- Choose between manual input or file-based input.
- Read and preprocess the data into a NumPy matrix.
2. **Matrix Normalization**
- Calculate the range (max - min) for each criterion.
- Normalize the input matrix by scaling values between 0 and 1.
3. **Moment Calculation**
- Compute row moments (ML) and column moments (MC) to determine priority rankings.
- Reorder rows and columns based on moment values.
4. **Iteration and Convergence**
- Repeat the moment calculation and reordering until no further changes occur in row or column order.
- Limit iterations to avoid infinite loops.
5. **Output the Optimal Ranking**
- Display the final ranking of decision alternatives.


### Error Handling

The script includes robust error handling for:
- Invalid or missing file paths.
- Unsupported file formats (only .xlsx, .xls, and .csv are supported).
- Malformed input data or incorrect file structure.
If errors occur during file reading or data processing, the script prompts you to retry or exit.


### Future Improvements
1. Add support for additional file formats (e.g., JSON, XML).
2. Include visualization options (e.g., charts for ranking trends).
