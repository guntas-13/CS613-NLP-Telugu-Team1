import os
import pandas as pd

clean_csv_path = '../TeluguData/ROOTS_MKB.csv'
output_folder = '../TeluguData/ROOTS_MKB'

os.makedirs(output_folder, exist_ok=True)

clean_df = pd.read_csv(clean_csv_path)

for index, row in clean_df.iterrows():
    filename = f'{index + 1}.txt'
    file_path = os.path.join(output_folder, filename)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(row['text'])

print(f"All articles have been written to {output_folder}.")
