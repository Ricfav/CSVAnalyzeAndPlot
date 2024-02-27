import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import mpld3
import streamlit.components.v1 as components

# Function to load CSV file into Pandas DataFrame with a specific separator, skip first two rows, and skip blank lines
# coded by R. Favetti - Rev 0.0
def load_data(file):
    return pd.read_csv(file,
                       sep=';',
                       skiprows=2,
                       skip_blank_lines=True,
                       parse_dates=[0],
                       dayfirst=True,
                       index_col=0)

# Function to plot selected column
def plot_column(data, selected_columns, width=800, height=600, legend_location='upper left'):
    fig, ax = plt.subplots(figsize=(width/100, height/100))
    plt.subplots_adjust(right=0.65)

    for column in selected_columns:
        ax.plot(data.index, data[column], label=f'{column}')

    ax.set_title('Original Values Plot')
    ax.set_xlabel('Datetime')
    ax.set_ylabel('Original Values')
    ax.legend(loc=legend_location, bbox_to_anchor=(1.05, 1), borderpad=0.2, prop={'size': 1.5 * width / 100})

    fig_html_original = mpld3.fig_to_html(fig)
    components.html(fig_html_original, height=height*1.1, width=width*1.1)

# Function to plot selected column with normalized values
def plot_column_normalized(data, selected_columns, width=800, height=600, legend_location='upper left'):
    fig1, ax1 = plt.subplots(figsize=(width/100, height/100))
    plt.subplots_adjust(right=0.65)

    for column in selected_columns:
        # Calculate normalized values
        normalized_values = (data[column] - data[column].min()) / (data[column].max() - data[column].min())
        ax1.plot(data.index, normalized_values, label=f'{column}')

    ax1.set_title('Normalized Values Plot')
    ax1.set_xlabel('Datetime')
    ax1.set_ylabel('Normalized Values')
    ax1.legend(loc=legend_location, bbox_to_anchor=(1.05, 1), borderpad=0.2, prop={'size': 1.5 * width / 100})

    fig_html_normalized = mpld3.fig_to_html(fig1)
    components.html(fig_html_normalized, height=height*1.1, width=width*1.1)

# Streamlit app
def main():
    st.title('CSV File Explorer and Plotter')

    # File selection
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read data from CSV file
        st.header('Dataframe view')
        data = load_data(uploaded_file)
        st.dataframe(data)
        st.header('Summary info')
        st.dataframe(data.describe())

        st.header('Plot')
        # Dropdown for selecting columns
        selected_columns = st.multiselect('Select columns', data.columns)

        # Options for width, height, and legend location
        st.sidebar.header('Plot Options')
        width = st.sidebar.slider('Width', min_value=100, max_value=1000, value=800)
        height = st.sidebar.slider('Height', min_value=100, max_value=1000, value=600)

        # Button to trigger the plot
        if st.button('Plot Original'):
            # Plot the selected columns with original values
            plot_column(data, selected_columns, width, height)

        if st.button('Plot Normalized'):
            # Plot the selected columns with normalized values
            plot_column_normalized(data, selected_columns, width, height)

    st.write("  \n   \n   \n   Version 0.0 - for info contact R. Favetti (riccardo.favetti@ariston.com)")

if __name__ == "__main__":
    st.set_option('deprecation.showPyplotGlobalUse', False)
    main()
