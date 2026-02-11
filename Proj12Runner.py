import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Runner(list):
    def run(args : list):
        """
        This program performs the following:
        - Unpacks command line arguments including a data file and amount of rows to plot
        - Outputs a variety of results based on the contents of the dataset and the number of rows of data being plotted
        - Plots the data and displays an image of the plot to the screen
        """

        # Display arguments and certification to the command interface
        print("args =  " + str(args))
        certification = (
            "\nI certify that this program is my own work\n"
            "and is not the work of others. I agree\n"
            "not to share my solution with others.\nBruno Rosado Monagas\n"
        )
        print(certification)

        # Import the dataset and collapse unique rows
        dataset = pd.read_csv(args[0]).iloc[:, [0, 2, 3, 4]] # args 0 is the name of the file, .iloc[:, [0, 2, 3, 4] to select only columns of interest (Date, Syst, Dias, Pulse)

        # Convert date column from string to datetime object for proper grouping and sorting
        dataset['Date'] = pd.to_datetime(dataset['Date'], format='%d %b %Y')

        # Rename appropriate columns
        dataset_renamed_cols = dataset.rename(columns={'Systolic (mmHg)':'Syst', 'Diastolic (mmHg)':'Dias', 'Pulse (bpm)':'Pulse'})

        # Collapse columns by grouping by date and calculating mean
        dataset_renamed_cols_collapsed_rows = dataset_renamed_cols.groupby('Date').mean().reset_index()

        # Sort reverse chronologically to match original file
        dataset_renamed_cols_collapsed_rows_reverse_chronological = dataset_renamed_cols_collapsed_rows.sort_values(by='Date', ascending=False).reset_index(drop=True)

        # Display collapsed dataset unique rows and means to command interface
        print('Collapse the data into unique rows')
        print('Number of unique rows: ' + str(dataset_renamed_cols_collapsed_rows_reverse_chronological['Date'].nunique()))
        print('Mean values for columns of interest in unique rows')
        print(dataset_renamed_cols_collapsed_rows_reverse_chronological.iloc[:,1:].mean())


        # Extract the subset of rows based on input
        subset = dataset_renamed_cols_collapsed_rows_reverse_chronological.iloc[:int(args[1])] # select the amount of rows specified in the input (ex: 31 will select the first 31 rows (0-30)

        # Calculate the min and max data values
        numeric_cols = subset.iloc[:,1:] # select only columns with numeric values (Syst, Dias, Pulse)

        # Use .stack() to combine all three columns into one Series, then calc min and max
        overall_min = numeric_cols.stack().min()
        overall_max = numeric_cols.stack().max()

        # Calculate xticks
        xticks = int(args[1]) // 5

        # Display rows to plot to command interface, min, max, mean, and xticks
        print('\nNumber of rows to plot: ' + args[1])
        print('Minimum data value in rows to plot: ' + str(overall_min))
        print('Maximum data value in rows to plot: ' + str(overall_max))
        print('\nMean values for columns of interest in rows to plot')
        print(subset.iloc[:,1:].mean())
        print('Number of xticks: ' + str(xticks))

        # Create figure
        fig, ax = plt.subplots(1,1,
            facecolor='0.75',linewidth=3,edgecolor='Red')
        
        fig.suptitle('Bruno Rosado Monagas')

        # Sort subset into ascending chronological order to plot
        subset_chron = subset.sort_values(by='Date', ascending=True).reset_index(drop=True).set_index('Date')

        # Dynamically calculate the x-ticks
        subset_length = len(subset_chron)

        # Define the number of gaps/segments between the labels
        # If L=12, there are 11 segments
        num_segments = xticks - 1

        # Calculate the float distance (step size) between each index selection
        # Total index range (N-1) divided by the number of segments
        index_step = (subset_length - 1) / num_segments

        # Generate the exact indices: start at 0 and step by index_step
        # "+ 1" on the stop point ensures the final index is included (doesn't work with case 2??? 61 rows)
        tick_indices_float = np.arange(start=0, stop=subset_length + 1, step=index_step)

        # select the index positions and the date values, truncating to get integer indices
        tick_indices = np.trunc(tick_indices_float).astype(int)

        # For some reason when I ran this with the case of 61 rows, the index 60 would get truncated to 59
        # This didn't happen with any of the other cases, so I figured this if statement would be enough to
        # ensure the last index is always included
        if tick_indices[-1] != subset_length - 1:
            tick_indices[-1] = subset_length - 1

        # remove duplicates if any
        tick_indices = np.unique(tick_indices)

        tick_dates = subset_chron.index[tick_indices]

        # Plot the data
        subset_chron.plot(kind='line', grid=True, marker='o', markersize=4, ax=ax,
                         yticks=range(int(overall_min),int(overall_max)+1,10),
                         ylabel='Value',
                         xlabel='Date',
                         use_index=True, rot=90)
        # Apply x-ticks
        ax.set_xticks(mdates.date2num(tick_dates))

        # Format the tick labels to look like "YYYY-MM-DD"
        ax.set_xticklabels([date.strftime('%Y-%m-%d') for date in tick_dates])
        ax.legend(loc='center') # Center legend

        return ax