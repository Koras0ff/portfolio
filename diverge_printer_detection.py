# For the books with a printer, this code checks if there are some printers who used more ilustrations
# than a pre-defined threshold value, mean and overall standard deviation.

"""import pandas as pd

# Load the dataset
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/filtered_holy_bible_illustrations.tsv'
data = pd.read_csv(file_path, delimiter='\t')

# Ensure relevant columns are present
required_columns = ['ecco_id', 'pages_ecco_id_proportion', 'printer']
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"The column '{col}' is not found in the dataset.")

# Group by ecco_id to get unique ecco_id rows with the maximum pages_ecco_id_proportion
ecco_grouped = data.groupby('ecco_id').agg({
    'pages_ecco_id_proportion': 'max', 
    'printer': 'first'
}).reset_index()

# Group by publication_place to calculate average, median and count of unique ecco_id
place_stats = ecco_grouped.groupby('printer').agg({
    'pages_ecco_id_proportion': ['mean', 'median', 'std'],
    'ecco_id': 'count'
}).reset_index()

# Rename columns for clarity
place_stats.columns = ['printer', 'mean_pages_ecco_id_proportion', 'median_pages_ecco_id_proportion', 'std_pages_ecco_id_proportion', 'ecco_id_count']

# Calculate overall mean and standard deviation for the entire dataset
overall_mean = ecco_grouped['pages_ecco_id_proportion'].mean()
overall_std = ecco_grouped['pages_ecco_id_proportion'].std()

# Define threshold as mean + 1 standard deviation (or use 2 standard deviations for a stricter threshold)
threshold = overall_mean + overall_std

# Add a column to indicate whether each publication place's mean proportion is above the threshold
place_stats['above_threshold'] = place_stats['mean_pages_ecco_id_proportion'] > threshold

# Print the results
print(place_stats)
print(f"Overall Mean: {overall_mean}")
print(f"Overall Standard Deviation: {overall_std}")
print(f"Threshold (Mean + 1*Std): {threshold}")

# Optionally save the results to a CSV file
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/IndefiniteAnalysis/Data/publisher_bible_stats.csv'
place_stats.to_csv(output_file_path, index=False)

print(f"The results have been saved to {output_file_path}")
"""