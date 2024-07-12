# This code visualizes the proportion of illustration types.

import pandas as pd
import matplotlib.pyplot as plt

# Load the TSV file
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/final_data_with_counts.tsv'
data = pd.read_csv(file_path, delimiter='\t')

# Calculate counts and proportions
counts = data['visual_type_verbal'].value_counts()
total_entries = data['visual_type_verbal'].count()
proportions = counts / total_entries * 100

# Creating subplots for both frequency and proportion in a single figure for better comparison
fig, axs = plt.subplots(2, 1, figsize=(10, 12))  # Increase the vertical size of the figure

# Frequency plot
counts.plot(kind='bar', color='skyblue', ax=axs[0])
axs[0].set_title('Frequency of Visual Type Verbal for the top 1% works with the most editions', pad=20)  # Increase padding for the title
axs[0].set_xlabel('Visual Type Verbal')
axs[0].set_ylabel('Frequency')
axs[0].tick_params(axis='x', labelrotation=45)

# Proportion plot
proportions.plot(kind='bar', color='plum', ax=axs[1])
axs[1].set_title('Proportion of Visual Type Verbal for the top 1% works with the most editions', pad=20)  # Increase padding for the title
axs[1].set_xlabel('Visual Type Verbal')
axs[1].set_ylabel('Percentage (%)')
axs[1].tick_params(axis='x', labelrotation=45)

plt.tight_layout()  # Adjust the layout to make more space
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Correct the file path if necessary
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/final_data_with_counts.tsv'

# Load the TSV file
data = pd.read_csv(file_path, delimiter='\t')

# Grouping by 'estc_id' to calculate the count of each topic per unique ESTC ID
topic_counts = data.groupby('topic')['estc_id'].nunique()

# Calculate the proportion of each topic across unique ESTC IDs
total_estc_ids = data['estc_id'].nunique()
topic_proportions = (topic_counts / total_estc_ids) * 100

# Plotting the proportions of topics
fig, ax = plt.subplots(figsize=(10, 5))
topic_proportions.plot(kind='bar', color='skyblue', ax=ax)
plt.title('Proportion of Genres Across ESTC IDs')
plt.xlabel('Genre')
plt.ylabel('Proportion (%)')
plt.xticks(rotation=45)
plt.ylim(0, 100)  # Ensure the y-axis goes from 0 to 100 for percentage representation
plt.tight_layout()

# Saving the figure to a file
plt.savefig('/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/genre_proportions_plot.png')

# Close the figure
plt.close(fig)


# Drop duplicates to consider each estc_id only once per topic
data_unique = data.drop_duplicates(subset=['estc_id', 'topic'])

# Group by 'topic' and sum 'estc_id_count'
topic_grouped = data_unique.groupby('topic')['estc_id_count'].sum()

# Normalize the sums to get proportions
total_estc_id_count = topic_grouped.sum()
topic_proportions = (topic_grouped / total_estc_id_count) * 100

# Plotting the proportions
fig, ax = plt.subplots()
topic_proportions.plot(kind='bar', color='teal', ax=ax)
ax.set_title('Proportion of illustrations by genre')
ax.set_xlabel('Genre')
ax.set_ylabel('Proportion (%)')
plt.xticks(rotation=45)
plt.tight_layout()

# Ensure the save directory exists or modify to a correct path
plt.savefig('/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/proportion_of_estc_id_count_by_topic.png')

# Close the plot to free up memory
plt.close()