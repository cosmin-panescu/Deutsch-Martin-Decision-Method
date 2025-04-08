import numpy as np
import pandas as pd
import os

def deutsch_martin_method():
    print("Metoda momentelor (Deutsch-Martin)")
    
    input_method = input("Introducere date manual sau import dintr-un fisier (manual / fisier): ").lower()

    # import din fisier 
    if input_method == 'fisier':
        while True:
            file_path = input("Introduceti numele fisierului (Excel sau CSV) + extensie: ")
            if os.path.exists(file_path):
                try:
                    # Determinare extensie fisier
                    file_extension = os.path.splitext(file_path)[1].lower()
                    
                    # Citire date in functie de extensie
                    if file_extension in ['.xlsx', '.xls']:
                        df = pd.read_excel(file_path, index_col=0)
                    elif file_extension == '.csv':
                        delimiter = input("Introduceti delimitatorul pentru fisierul CSV (implicit ','): ") or ','
                        df = pd.read_csv(file_path, index_col=0, delimiter=delimiter)
                    else:
                        print(f"Extensia {file_extension} nu este suportata. Folositi fisiere Excel sau CSV.")
                        retry = input("Incercati din nou? (d/n): ").lower()
                        if retry != 'd':
                            return
                        continue
                    
                    # extragerea nr de variante si criterii
                    num_variants = df.shape[0]
                    num_criteria = df.shape[1]
                    
                    # numele variantelor si criteriilor
                    variants = list(df.index)
                    criteria = list(df.columns)
                    
                    # convertire in matrice NumPy
                    matrix = df.to_numpy()
                    
                    print(f"S-au detectat {num_variants} variante si {num_criteria} criterii.")
                    break
                except Exception as e:
                    print(f"Eroare la citirea fisierului: {e}")
                    retry = input("Incercati din nou? (d/n): ").lower()
                    if retry != 'd':
                        return
            else:
                print(f"Fisierul '{file_path}' nu exista în directorul curent.")
                retry = input("Incercati din nou? (d/n): ").lower()
                if retry != 'd':
                    return
    else:
        # introducere date manual
        num_variants = int(input("Numarul de variante: "))
        num_criteria = int(input("Numarul de criterii: "))
        matrix = np.zeros((num_variants, num_criteria))
        
        variants = []
        criteria = []
        
        print("\nIntroduceti numele variantelor:")
        for i in range(num_variants):
            var_name = input(f"Numele variantei {i+1}: ") or f"V{i+1}"
            variants.append(var_name)
            
        print("\nIntroduceti numele criteriilor:")
        for j in range(num_criteria):
            crit_name = input(f"Numele criteriului {j+1}: ") or f"C{j+1}"
            criteria.append(crit_name)
        
        print("\nValorile pentru fiecare varianta si criteriu:")
        for i in range(num_variants):
            print(f"\nPentru varianta {variants[i]}:")
            for j in range(num_criteria):
                matrix[i, j] = float(input(f"  Valoarea pentru criteriul {criteria[j]}: "))
    
    # Pas 1: Normalizarea matricei consecintelor
    max_min = np.max(matrix, axis=0) - np.min(matrix, axis=0)
    normalized = np.zeros((num_variants, num_criteria))
    for j in range(num_criteria):
        if max_min[j] != 0:
            normalized[:, j] = (matrix[:, j] - np.min(matrix[:, j])) / max_min[j]
    
    print("\nMatricea consecintelor normalizata:")
    for i in range(num_variants):
        print(f"{variants[i]}: {normalized[i]}")
    
    # Functii pentru calculul momentelor
    def calculate_moments(mat, labels, axis=0):
        moments = np.zeros(len(labels))
        for idx in range(len(labels)):
            if axis == 0:  # momente de linie
                numerator = sum(mat[idx, j] * (j + 1) for j in range(mat.shape[1]))
                denominator = sum(mat[idx, j] for j in range(mat.shape[1]))
                prefix = "ML"
            else:  # momente de coloana
                numerator = sum(mat[i, idx] * (i + 1) for i in range(mat.shape[0]))
                denominator = sum(mat[i, idx] for i in range(mat.shape[0]))
                prefix = "MC"
                
            moments[idx] = numerator / denominator if denominator != 0 else 0
            print(f"{prefix}({labels[idx]}) = {moments[idx]:.4f}")
        return moments
    
    # Procesul iterativ al metodei Deutsch-Martin
    current_matrix = normalized.copy()
    current_variants = variants.copy()
    current_criteria = criteria.copy()
    
    iteration = 1
    converged = False
    
    while not converged:
        print(f"\n--- Iteratia {iteration} ---")
        
        # Calculare momente de linie
        print("\nCalcularea momentelor de linie:")
        ml = calculate_moments(current_matrix, current_variants, axis=0)
        
        # Ordonare linii
        ml_indices = np.argsort(ml)
        new_matrix = current_matrix[ml_indices]
        new_variants = [current_variants[i] for i in ml_indices]
        
        # Verificare daca ordinea liniilor s-a schimbat
        lines_changed = not (np.array_equal(current_matrix, new_matrix) and current_variants == new_variants)
        
        if lines_changed:
            print(f"\nOrdonarea liniilor (iteratia {iteration}):")
            for i in range(num_variants):
                print(f"{new_variants[i]}: {new_matrix[i]}")
                
            current_matrix = new_matrix.copy()
            current_variants = new_variants.copy()
        else:
            print("\nNu mai exista posibilitatea unor noi ordonari ale liniilor.")
        
        # Calculare momente de coloana
        print("\nCalcularea momentelor de coloana:")
        mc = calculate_moments(current_matrix, current_criteria, axis=1)
        
        # Ordonare coloane
        mc_indices = np.argsort(mc)
        new_matrix = current_matrix[:, mc_indices]
        new_criteria = [current_criteria[i] for i in mc_indices]
        
        # Verificare daca ordinea coloanelor s-a schimbat
        columns_changed = not (np.array_equal(current_matrix, new_matrix) and current_criteria == new_criteria)
        
        if columns_changed:
            print(f"\nOrdonarea coloanelor (iteratia {iteration}):")
            for i in range(num_variants):
                print(f"{current_variants[i]}: {new_matrix[i]}")
                
            current_matrix = new_matrix.copy()
            current_criteria = new_criteria.copy()
        else:
            print("\nNu mai exista posibilitatea unor noi ordonari ale coloanelor.")
        
        # Verificare convergenta
        if not (lines_changed or columns_changed):
            print("\nNu mai exista posibilitatea unor noi ordonari.")
            converged = True
        else:
            iteration += 1
            if iteration > 10:  # limita pt. evitare bucle infinite
                print("\nLimita maxima de iteratii a fost atinsa.")
                converged = True
    
    # Rezultat final
    print("\nClasamentul OPTIM al variantelor decizionale:")
    for i in range(num_variants):
        print(f"{i+1}. {current_variants[i]}")

if __name__ == "__main__":
    deutsch_martin_method()
