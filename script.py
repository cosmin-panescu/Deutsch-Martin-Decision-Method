import numpy as np
import pandas as pd
import os

def deutsch_martin_method():
    print("Method of moments (Deutsch-Martin)")
    
    input_method = input("Enter data manually or import from a file (manual / file): ").lower()

    # import data from file 
    if input_method == 'file':
        while True:
            file_path = input("Enter the file name (Excel or CSV) + extension: ")
            if os.path.exists(file_path):
                try:
                    # extract file extension
                    file_extension = os.path.splitext(file_path)[1].lower()
                    
                    # read data based on file type
                    if file_extension in ['.xlsx', '.xls']:
                        df = pd.read_excel(file_path, index_col=0)
                    elif file_extension == '.csv':
                        delimiter = input("Enter the delimiter for the CSV file (default ','): ") or ','
                        df = pd.read_csv(file_path, index_col=0, delimiter=delimiter)
                    else:
                        print(f"The extension {file_extension} is not supported. Please use Excel or CSV files.")
                        retry = input("Try again? (y/n): ").lower()
                        if retry != 'y':
                            return
                        continue
                    
                    # extract number of variants and criteria
                    num_variants = df.shape[0]
                    num_criteria = df.shape[1]
                    
                    # variants and criteria names
                    variants = list(df.index)
                    criteria = list(df.columns)
                    
                    # convert to numpy array
                    matrix = df.to_numpy()
                    
                    print(f"{num_variants} variants and {num_criteria} criteria have been detected.")
                    break
                except Exception as e:
                    print(f"Error reading the file: {e}")
                    retry = input("Try again? (y/n): ").lower()
                    if retry != 'y':
                        return
            else:
                print(f"The file '{file_path}' does not exist in the current directory.")
                retry = input("Try again? (y/n): ").lower()
                if retry != 'y':
                    return
    else:
        # manual input
        num_variants = int(input("Number of variants: "))
        num_criteria = int(input("Number of criteria: "))
        matrix = np.zeros((num_variants, num_criteria))
        
        variants = []
        criteria = []
        
        print("\nEnter the names of the variants:")
        for i in range(num_variants):
            var_name = input(f"Name of variant {i+1}: ") or f"V{i+1}"
            variants.append(var_name)
            
        print("\nEnter the names of the criteria:")
        for j in range(num_criteria):
            crit_name = input(f"Name of criterion {j+1}: ") or f"C{j+1}"
            criteria.append(crit_name)

        print("\nValues for each variant and criterion:")
        for i in range(num_variants):
            print(f"\nFor variant {variants[i]}:")
            for j in range(num_criteria):
                matrix[i, j] = float(input(f"  Value for criterion {criteria[j]}: "))

    
    # Step 1: Normalize the matrix
    max_min = np.max(matrix, axis=0) - np.min(matrix, axis=0)
    normalized = np.zeros((num_variants, num_criteria))
    for j in range(num_criteria):
        if max_min[j] != 0:
            normalized[:, j] = (matrix[:, j] - np.min(matrix[:, j])) / max_min[j]
    
    print("\nNormalized consequences matrix:")
    for i in range(num_variants):
        print(f"{variants[i]}: {normalized[i]}")
    
    # function to calculate moments
    def calculate_moments(mat, labels, axis=0):
        moments = np.zeros(len(labels))
        for idx in range(len(labels)):
            if axis == 0:  # line moments
                numerator = sum(mat[idx, j] * (j + 1) for j in range(mat.shape[1]))
                denominator = sum(mat[idx, j] for j in range(mat.shape[1]))
                prefix = "ML"
            else:  # column moments
                numerator = sum(mat[i, idx] * (i + 1) for i in range(mat.shape[0]))
                denominator = sum(mat[i, idx] for i in range(mat.shape[0]))
                prefix = "MC"
                
            moments[idx] = numerator / denominator if denominator != 0 else 0
            print(f"{prefix}({labels[idx]}) = {moments[idx]:.4f}")
        return moments
    
   # Iterative process of the Deutsch-Martin method
    current_matrix = normalized.copy()
    current_variants = variants.copy()
    current_criteria = criteria.copy()
    
    iteration = 1
    converged = False
    
    while not converged:
        print(f"\n--- Iteration {iteration} ---")
        
        # Calculate row moments
        print("\nCalculating row moments:")
        ml = calculate_moments(current_matrix, current_variants, axis=0)
        
        # line sorting
        ml_indices = np.argsort(ml)
        new_matrix = current_matrix[ml_indices]
        new_variants = [current_variants[i] for i in ml_indices]
        
        # Check if the order of the rows has changed
        lines_changed = not (np.array_equal(current_matrix, new_matrix) and current_variants == new_variants)
        
        if lines_changed:
            print(f"\nSorting rows (iteration {iteration}):")
            for i in range(num_variants):
                print(f"{new_variants[i]}: {new_matrix[i]}")
                
            current_matrix = new_matrix.copy()
            current_variants = new_variants.copy()
        else:
            print("\nNo further row reordering is possible.")
        
        # calculate column moments
        print("\nCalcularea momentelor de coloana:")
        mc = calculate_moments(current_matrix, current_criteria, axis=1)
        
        # column sorting
        mc_indices = np.argsort(mc)
        new_matrix = current_matrix[:, mc_indices]
        new_criteria = [current_criteria[i] for i in mc_indices]
        
        # Check if the order of the columns has changed
        columns_changed = not (np.array_equal(current_matrix, new_matrix) and current_criteria == new_criteria)
        
        if columns_changed:
            print(f"\nSorting columns (iteration {iteration}):")
            for i in range(num_variants):
                print(f"{current_variants[i]}: {new_matrix[i]}")
                
            current_matrix = new_matrix.copy()
            current_criteria = new_criteria.copy()
        else:
            print("\nNo further column reordering is possible.")
        
        # verify convergence
        if not (lines_changed or columns_changed):
            print("\nNo further reordering is possible.")
            converged = True
        else:
            iteration += 1
            if iteration > 10:  # limit of iterations to prevent infinite loops
                print("\nThe maximum iteration limit has been reached.")
                converged = True
    
    # Final result
    print("\nThe OPTIMAL ranking of decision variants:")
    for i in range(num_variants):
        print(f"{i+1}. {current_variants[i]}")

if __name__ == "__main__":
    deutsch_martin_method()
