import pandas as pd
import seaborn as sns

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('08(02) - ACP_CPP_Compiled_Cleaned_for_analysis.csv')

# Specify the column indices for x and y values (0-indexed)
x_column_index = 2  # Third column (index 2)
y_column_index = 8  # Ninth column (index 8)

# Extract the x and y values from the DataFrame using column indices
x_values = df.iloc[:, x_column_index]
y_values = df.iloc[:, y_column_index]

# Convert the values to float with two decimal places
x_values = x_values.round(2)
y_values = y_values.round(2)

# Create the scatterplot using Seaborn
sns.scatterplot(x=x_values, y=y_values)

# Show the plot
import matplotlib.pyplot as plt
plt.show()
