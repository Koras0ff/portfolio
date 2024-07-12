# Bible based illustration proportion plot can be drawn via this code.

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/filtered_holy_bible_illustrations.tsv'
data = pd.read_csv(file_path, sep='\t', dtype={'ecco_id': str})

# Creating a DataFrame
df = pd.DataFrame(data)


# Group by 'ecco_id', then apply a lambda function to sort each group by 'pages_ecco_id_proportion' and take the top 10
top10_per_ecco_id = df.groupby('ecco_id').apply(lambda x: x.nlargest(10, 'pages_ecco_id_proportion'))

# Reset index to clean up the DataFrame
top10_per_ecco_id.reset_index(drop=True, inplace=True)

# Print the result
print(top10_per_ecco_id)

# Calculating the proportion of each unique value in the 'visual_type_verbal' column
value_counts = df['visual_type_verbal'].value_counts(normalize=True)

# Creating a bar chart
value_counts.plot(kind='bar', color='skyblue')

# Adding titles and labels
plt.title('Proportions of Visual Types')
plt.xlabel('Visual Type Verbal')
plt.ylabel('Proportion')
plt.xticks(rotation=45)  # Rotates labels to avoid overlap

# Display the plot
plt.show()

