
# This file has several code blocks that are connected to each other. Some of them are independent from others
# since I used this file as a collection of code blocks.
# As long as you have the first two files, I think the code will work on your device.

# The first code block gives the books with the most illustrations (top 1%).
"""
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files into DataFrames
# These two files were obtained from Iiro.
estc_metadata_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/Luxury Books/estc_metadata.csv'
illustration_metadata_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/Luxury Books/illustration_metadata.csv'

# 'ecco_id' column value will be processed as string to make sure that the 0s at the beginning will be there.
estc_df = pd.read_csv(estc_metadata_path, dtype={'ecco_id': str})
illustration_df = pd.read_csv(illustration_metadata_path, dtype={'ecco_id': str})

# Count the number of unique estc_id values for each work_id
work_id_counts = estc_df.groupby('work_id')['estc_id'].nunique().reset_index()
work_id_counts.columns = ['work_id', 'unique_estc_id_count']

# Sort the work_id based on the count of unique estc_id values in descending order
sorted_work_id_counts = work_id_counts.sort_values(by='unique_estc_id_count', ascending=False)

# Calculate the number of work_id entries in the top 1%
top_1_percent_count = int(len(sorted_work_id_counts) * 0.01)

# Select the top 1% of work_id entries
top_1_percent_work_ids = sorted_work_id_counts.head(top_1_percent_count)['work_id']

# Filter the original DataFrame to include only rows where work_id is in the top 1% list
filtered_estc_df = estc_df[estc_df['work_id'].isin(top_1_percent_work_ids)]

# Extract the unique ecco_id values from the filtered DataFrame
unique_ecco_ids = filtered_estc_df['ecco_id'].unique()

# Filter the illustration DataFrame to include only rows where ecco_id is in the unique_ecco_ids list
filtered_illustration_df = illustration_df[illustration_df['ecco_id'].isin(unique_ecco_ids)]

# Select the required columns to merge from the estc_metadata DataFrame
columns_to_merge = ["ecco_id", "estc_id", "topic", "pages", "format", "publication_place", "publication_country", "work_id", "ocr_median_quality"]

# Merge the filtered illustration DataFrame with the filtered estc_metadata DataFrame
merged_final_df = pd.merge(filtered_illustration_df, filtered_estc_df[columns_to_merge], on='ecco_id', how='left')

# Save the merged DataFrame to a new TSV file
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/filtered_top_1_illustration_metadata.tsv'
merged_final_df.to_csv(output_file_path, sep='\t', index=False)

print(f"Filtered illustration metadata with additional columns has been saved to {output_file_path}")
"""





import pandas as pd

# Load the main DataFrame
main_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/filtered_top_1_illustration_metadata.tsv'
main_df = pd.read_csv(main_file_path, delimiter='\t', dtype={'ecco_id': str}) # For each file, 'ecco_id' column values will be processed as string.

# Load the supplementary DataFrame
supplementary_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/Luxury Books/ecco_titles_and_publication_year.csv'
supplementary_df = pd.read_csv(supplementary_file_path, quotechar='"', skipinitialspace=True, dtype={'ecco_id': str})

# Strip and confirm columns
main_df.columns = main_df.columns.str.strip()
supplementary_df.columns = supplementary_df.columns.str.strip()

print("Main DataFrame Columns:", main_df.columns)
print("Supplementary DataFrame Columns:", supplementary_df.columns)

# Ensure 'ecco_id' columns exist
if 'ecco_id' in main_df.columns and 'ecco_id' in supplementary_df.columns:
    print("Both DataFrames contain 'ecco_id'. Proceeding with merge.")
else:
    print("Missing 'ecco_id' in one of the DataFrames.")

# Attempt to merge
try:
    merged_df = pd.merge(main_df, supplementary_df, on='ecco_id', how='left')
    print("Merge successful.")
except Exception as e:
    print("Merge failed:", str(e))

# Save the resulting DataFrame to a new TSV file
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/revised_top_1_percent_work_ids.tsv'
merged_df.to_csv(output_file_path, sep='\t', index=False)
print(f"Merged data with publication_year and full_title has been saved to {output_file_path}")
"""
"""
import pandas as pd

# Load the main data file
main_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/filtered_top_1_illustration_metadata.tsv'
main_df = pd.read_csv(main_file_path, delimiter='\t', dtype={'ecco_id': str})  # Ensure ecco_id is read as string

# Load the ecco-titles data file
ecco_titles_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/Luxury Books/ecco_titles_and_publication_year.csv'
ecco_titles_df = pd.read_csv(ecco_titles_path)
ecco_titles_df['ecco_id'] = ecco_titles_df['ecco_id'].astype(str)  # Convert ecco_id to string if it's not already

print(main_df['ecco_id'].head())
print(ecco_titles_df[['ecco_id', 'publication_year', 'ecco_full_title']].head())

# Ensure there are no leading or trailing spaces in column names and they are consistent
main_df.columns = main_df.columns.str.strip()
ecco_titles_df.columns = ecco_titles_df.columns.str.strip()

# Merge the main DataFrame with the ecco-titles DataFrame on 'ecco_id'
# Ensure that 'ecco_id' is the correct key and it is unique in both DataFrames
# Inner join to ensure only matched records are included
merged_df = pd.merge(main_df, ecco_titles_df[['ecco_id', 'publication_year', 'ecco_full_title']], on='ecco_id', how='inner')

# After merging
merged_df['publication_year'].isna().sum()
merged_df['ecco_full_title'].isna().sum()


# Save the merged DataFrame back to a CSV file
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/revised_top_1_percent_work_ids.tsv'
merged_df.to_csv(output_file_path, sep='\t', index=False)

print("Updated data with ecco titles has been saved to", output_file_path)




import pandas as pd

# Load the TSV file into a DataFrame
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/revised_top_1_percent_work_ids.tsv'
df = pd.read_csv(file_path, delimiter='\t', dtype={'ecco_id': str})

# Count the occurrences of each ecco_id
ecco_id_counts = df['ecco_id'].value_counts().reset_index()
ecco_id_counts.columns = ['ecco_id', 'ecco_id_count']

# Count the occurrences of each estc_id
estc_id_counts = df['estc_id'].value_counts().reset_index()
estc_id_counts.columns = ['estc_id', 'estc_id_count']

# Merge the counts back into the original DataFrame
df = pd.merge(df, ecco_id_counts, on='ecco_id', how='left')
df = pd.merge(df, estc_id_counts, on='estc_id', how='left')

# Calculate the proportion of pages by ecco_id_count
df['pages_ecco_id_proportion'] = (df['ecco_id_count'] / df['pages']) * 100

# Save the resulting DataFrame to a new TSV file
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/final_data_with_counts.tsv'
df.to_csv(output_file_path, sep='\t', index=False)

print(f"Data with ecco_id and estc_id counts has been saved to {output_file_path}")



# The code below extracts the Bible related rows from the main data.
import pandas as pd

# Load the TSV file into a DataFrame
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/final_data.csv'
df = pd.read_csv(file_path, dtype={'ecco_id': str})

# Strip any leading or trailing spaces from the column names
df.columns = df.columns.str.strip()

# Define the list of work_id values to filter
work_id_values = [
    "X-the holy bible, containing the old and new testaments",
    "X-the holy bible",
    "X-the holy bible, containing the old testament and the new: newly translated out of the original tongues, and with the",
    "X-the holy bible, containing the old testament and the new",
    "X-the holy bible, containing the old and new testaments: newly translated out of the original tongues: and with the former",
    "X-a curious hieroglyphick bible"
]

# Filter the DataFrame to include only rows where work_id is in the specified list
filtered_df = df[df['work_id'].isin(work_id_values)]

# Save the filtered DataFrame to a new TSV file
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/filtered_holy_bible_illustrations.tsv'
filtered_df.to_csv(output_file_path, sep='\t', index=False)

print(f"Filtered rows have been saved to {output_file_path}")



import pandas as pd

# Load the datasets
top_10_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/top_10_percent_by_topic.csv'
final_data_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/final_data.csv'

top_10_data = pd.read_csv(top_10_path)
final_data = pd.read_csv(final_data_path)

# Extract unique work_ids from top 10% dataset
top_10_work_ids = set(top_10_data['work_id'].unique())

# Filter final_data where work_id is in top_10_work_ids
filtered_final_data = final_data[final_data['work_id'].isin(top_10_work_ids)]

# Save the filtered data to a new CSV file
output_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/actor_analysis_final_data.csv'
filtered_final_data.to_csv(output_path, index=False)

print(f"Filtered data has been saved to {output_path}")



import pandas as pd

# Load the dataset
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/cleaned_actor_analysis_final_data.csv'
data = pd.read_csv(file_path)

# Convert ecco_id column to string type
data['ecco_id'] = data['ecco_id'].astype(str)

# Aggregate data to ensure each ecco_id has only one entry, taking the mean of pages_ecco_id_proportion
data_aggregated = data.groupby(['ecco_id', 'work_id']).agg({
    'pages_ecco_id_proportion': 'mean'
}).reset_index()

# Calculate variance, mean, and standard deviation of pages_ecco_id_proportion for each work_id
stats_data = data_aggregated.groupby('work_id')['pages_ecco_id_proportion'].agg(['var', 'mean', 'std']).reset_index()

# Rename the columns for clarity
stats_data.rename(columns={'var': 'variance_pages_ecco_id_proportion', 'mean': 'mean_pages_ecco_id_proportion', 'std': 'std_pages_ecco_id_proportion'}, inplace=True)

# Merge the stats back to the aggregated data to associate each ecco_id with these stats
data_with_stats = data_aggregated.merge(stats_data, on='work_id')

# Identify potential outliers: those whose pages_ecco_id_proportion is beyond 2 standard deviations from the mean
data_with_stats['is_outlier'] = data_with_stats.apply(lambda x: abs(x['pages_ecco_id_proportion'] - x['mean_pages_ecco_id_proportion']) > 2 * x['std_pages_ecco_id_proportion'], axis=1)

# Filter for potential outliers
potential_outliers = data_with_stats[data_with_stats['is_outlier']]

# Display and save potential outliers
print(potential_outliers[['ecco_id', 'work_id', 'pages_ecco_id_proportion', 'mean_pages_ecco_id_proportion', 'std_pages_ecco_id_proportion', 'variance_pages_ecco_id_proportion', 'is_outlier']])
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/potential_outliers.csv'
potential_outliers.to_csv(output_file_path, index=False)

print(f"Potential outliers saved to {output_file_path}")



import pandas as pd

# Load the potential outliers data
potential_outliers_file = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/potential_outliers.csv'
potential_outliers_data = pd.read_csv(potential_outliers_file)

# Load the additional data file
additional_data_file = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/final_data.csv'
additional_data = pd.read_csv(additional_data_file)

# Columns to add from the additional data
columns_to_add = ["ecco_id", "estc_id", "topic", "pages", "format", "publication_place", 
                  "publication_country", "work_id", "ocr_median_quality", "publication_year", 
                  "ecco_full_title", "copies_total", "copies_upgrade", "ecco_id_count", 
                  "estc_id_count", "decorative_initial", "factotum", "illustration_frontispiece", 
                  "illustration_other", "illustration_woodcut_or_engraving", "printers_ornament_device", 
                  "printers_ornament_headpiece", "printers_ornament_tailpiece", "author", 
                  "bookseller", "engraver", "printer", "publisher"]

# Merge the dataframes on 'ecco_id'
merged_data = pd.merge(potential_outliers_data, additional_data[columns_to_add], on='ecco_id', how='left')

# Drop duplicates based on 'ecco_id'
merged_data = merged_data.drop_duplicates(subset='ecco_id')

# Save the updated data to a new file
updated_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/potential_outliers_with_additional_info.csv'
merged_data.to_csv(updated_file_path, index=False)

print(f"Updated data with additional info saved to {updated_file_path}")



import pandas as pd
import os

# Define the file path
merged_data_file = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/potential_outliers_with_additional_info.csv'

# Check if the file exists
if not os.path.exists(merged_data_file):
    print(f"File not found: {merged_data_file}")
else:
    # Load the merged data file
    merged_data = pd.read_csv(merged_data_file)

    # Define columns to analyze for frequency
    columns_to_analyze = ["author", "bookseller", "engraver", "printer", "publisher"]

    # Function to get top 10 frequent values for a given column
    def get_top_frequent(df, column):
        # Convert column to string type
        df[column] = df[column].astype(str)
        # Split the strings by ';', explode the lists into rows, and get the value counts
        freq_series = df[column].str.split(';').explode().value_counts().head(10)
        return freq_series

    # Dictionary to store top 10 frequent values for each column
    top_frequent_values = {}

    # Calculate top 10 frequent values for each column
    for column in columns_to_analyze:
        top_frequent_values[column] = get_top_frequent(merged_data, column)

    # Convert the results to a DataFrame for better display
    top_frequent_df = pd.DataFrame(top_frequent_values)

    # Display the top frequent values
    print(top_frequent_df)

    # Save the results to a CSV file
    output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/top_frequent_values.csv'
    top_frequent_df.to_csv(output_file_path, index=True)
    print(f"Top frequent values saved to {output_file_path}")


import pandas as pd
import os

# Define the file path
data_file = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/final_data.csv'

# Check if the file exists
if not os.path.exists(data_file):
    print(f"File not found: {data_file}")
else:
    # Load the data file
    data = pd.read_csv(data_file)

    # Filter rows where 'work_id' contains 'homer' (case insensitive)
    filtered_data = data[data['work_id'].str.contains('homer', case=False, na=False)]

    # Display the filtered data
    print(filtered_data)

    # Save the filtered data to a new file
    output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/homer_work_id_filtered.csv'
    filtered_data.to_csv(output_file_path, index=False)
    print(f"Filtered data saved to {output_file_path}")



import pandas as pd

# Read the TSV file into a DataFrame
df = pd.read_csv('/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/top_10_percent_by_topic.tsv', sep='\t')

# Calculate the sum of the 'ecco_id_count' column
ecco_id_count_sum = df['ecco_id_count'].sum()

print("Sum of 'ecco_id_count':", ecco_id_count_sum)
