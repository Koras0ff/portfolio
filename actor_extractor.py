# Actor information was extracted via this code.

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset with explicit delimiter
main_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/final_data_with_counts.tsv'
main_df = pd.read_csv(main_file_path, dtype={'ecco_id': str, 'image_id': str}, delimiter='\t', on_bad_lines='skip')

# Load the supplementary roles dataset
roles_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/Luxury Books/book_trade_actors.csv'
roles_df = pd.read_csv(roles_file_path)

# Check and print column names
print("Main DataFrame columns:", main_df.columns)
print("Roles DataFrame columns:", roles_df.columns)

# Ensure 'estc_id' column exists in both DataFrames and strip any whitespace from column names
main_df.columns = main_df.columns.str.strip()
roles_df.columns = roles_df.columns.str.strip()

# Rename the column to 'estc_id' if necessary
if 'estc_id' not in main_df.columns:
    print("'estc_id' column not found in main DataFrame, please check the column names.")
else:
    print("'estc_id' column found in main DataFrame.")

if 'estc_id' not in roles_df.columns:
    print("'estc_id' column not found in roles DataFrame, please check the column names.")
else:
    print("'estc_id' column found in roles DataFrame.")

# Create a combined column with both actor_id and actor_name_primary
roles_df['actor_combined'] = roles_df['actor_id'].astype(str) + "; " + roles_df['actor_name_primary']

# Pivot roles_df to have actor_combined under the respective role columns where role is True
pivot_roles_df = roles_df.melt(id_vars=['estc_id', 'actor_combined'], 
                               value_vars=['actor_role_publisher', 'actor_role_author', 
                                           'actor_role_bookseller', 'actor_role_printer', 
                                           'actor_role_engraver'],
                               var_name='role', value_name='is_role')
pivot_roles_df = pivot_roles_df[pivot_roles_df['is_role']]
pivot_roles_df.drop(columns='is_role', inplace=True)
pivot_roles_df['role'] = pivot_roles_df['role'].str.replace('actor_role_', '')

# Handle duplicate entries by grouping and aggregating actor_combined
pivot_roles_df = pivot_roles_df.groupby(['estc_id', 'role']).agg({'actor_combined': lambda x: '; '.join(x.astype(str))}).reset_index()

# Create a DataFrame with one column per role containing the actor_combined
role_actor_df = pivot_roles_df.pivot(index='estc_id', columns='role', values='actor_combined').reset_index()

# Merge the main DataFrame with the role_actor DataFrame on 'estc_id'
final_df = pd.merge(main_df, role_actor_df, on='estc_id', how='left')

# Save the resulting DataFrame to a new file
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/Luxury Books/final_data_with_roles.csv'
final_df.to_csv(output_file_path, index=False)

print(f"Data with roles has been saved to {output_file_path}")
