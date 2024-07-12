# This file includes a bunch of connected codes to create new files such as subset files.
"""import pandas as pd

# Load the dataset
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/final_data_with_roles.csv'
data = pd.read_csv(file_path)

# Calculate the count of each visual_type_verbal per ecco_id
visual_type_counts = data.groupby(['ecco_id', 'visual_type_verbal']).size().reset_index(name='count')

# Calculate total counts per ecco_id
total_counts = data.groupby('ecco_id').size().reset_index(name='total_count')

# Merge the counts with the total counts
visual_type_counts = visual_type_counts.merge(total_counts, on='ecco_id')

# Calculate proportions
visual_type_counts['proportion'] = visual_type_counts['count'] / visual_type_counts['total_count']

# Pivot the data to get each visual_type_verbal as a column
pivot_table = visual_type_counts.pivot(index='ecco_id', columns='visual_type_verbal', values='proportion')

# Reset index to flatten the DataFrame
pivot_table.reset_index(inplace=True)

# Merge the pivot table back with the original data
final_data = data.merge(pivot_table, on='ecco_id', how='left')

# Fill NaN values with 0 for any visual_type_verbal that might not be present in all groups
final_data.fillna(0, inplace=True)

# Optionally, save to a new CSV
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/modified_final_data_with_visual_types.tsv'
final_data.to_csv(output_file_path, sep='\t', index=False)

print("Data has been successfully saved to:", output_file_path)
"""

"""
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/final_data_with_roles.csv'
data = pd.read_csv(file_path, dtype={'ecco_id': str})

import pandas as pd
# Filter out entries where 'pages' is less than 3
data_filtered = data[data['pages'] >= 10]

# Drop duplicates based on 'ecco_id' within each 'topic' to ensure each ecco_id is considered only once per genre
data_unique = data_filtered.drop_duplicates(subset=['topic', 'ecco_id'])

# Group by topic and apply a function to determine the top 25% in each group
def top_25_percent(group):
    # Calculate the 75th percentile within the group
    cutoff = group['pages_ecco_id_proportion'].quantile(0.90)
    # Return only the rows where the proportion is above the 75th percentile
    return group[group['pages_ecco_id_proportion'] >= cutoff]

# Apply the function to each group
top_25_by_topic = data_unique.groupby('topic').apply(top_25_percent)

# Since groupby().apply() returns a multi-index DataFrame, let's reset the index
top_25_by_topic.reset_index(drop=True, inplace=True)

# Display or save the top 25% ecco_ids by topic
print(top_25_by_topic[['ecco_id', 'topic', 'pages_ecco_id_proportion']])

# Optionally, save to CSV
top_25_by_topic.to_csv('/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/top_10_percent_by_topic.csv', index=False)


import pandas as pd

# Load the dataset
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/top_10_percent_by_topic.csv'
data = pd.read_csv(file_path)

# Columns to be removed
columns_to_drop = ['page', 'visual_type', 'score', 'image_name', 'image_coordinates', 'visual_type_verbal']

# Drop the specified columns
data = data.drop(columns=columns_to_drop)

# Save the modified DataFrame back to a new CSV file
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/modified_top_10_percent_by_topic.csv'
data.to_csv(output_file_path, index=False)

print("Data has been successfully saved to:", output_file_path)
"""


"""
import pandas as pd

# Load the main DataFrame
main_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/Luxury Books/illustration_metadata_deduplicated.csv'
main_df = pd.read_csv(main_file_path, dtype={'ecco_id': str})

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
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/revised_illustration_metadata_deduplicated.tsv'
merged_df.to_csv(output_file_path, sep='\t', index=False)
print(f"Merged data with publication_year and full_title has been saved to {output_file_path}")


import pandas as pd

# Load the TSV file into a DataFrame
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/revised_illustration_metadata_deduplicated.tsv'
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
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/rrevised_illustration_metadata_deduplicated.tsv'
df.to_csv(output_file_path, sep='\t', index=False)

print(f"Data with ecco_id and estc_id counts has been saved to {output_file_path}")"""