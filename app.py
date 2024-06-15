import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.snow()
# Title of the Streamlit app
st.title("`Student Mental Health Analysis`")
st.markdown("---")
st.subheader(":clap:`About`")
st.write("""
This app ...
That App ...
""")
st.markdown("---")

# Sidebar for uploading the dataset
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the dataset
    df = pd.read_csv(uploaded_file)
    st.success(":wave: `Welcome, Your Data is succesfully imported`")
    st.balloons()
    
    # Display the dataset
    st.write("## Dataset")
    st.write(df.head())

    # Sidebar for selecting columns to display
    st.sidebar.header("Select Columns")
    
    # List of columns to choose from
    columns = df.columns.tolist()
    selected_columns = st.sidebar.multiselect("Select the columns you want to display", columns, default=columns)
    
    # Filtered dataframe
    filtered_df = df[selected_columns]
    
    # Display the filtered dataframe
    st.write("## Filtered Data")
    st.write(filtered_df)

    # Sidebar for input sliders
    st.sidebar.header("Input Filters")
    
    # Input sliders for numeric columns
    age_filter = st.sidebar.slider("Age", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))
    cgpa_filter = st.sidebar.slider("CGPA", float(df["CGPA"].min()), float(df["CGPA"].max()), (float(df["CGPA"].min()), float(df["CGPA"].max())))
    stress_level_filter = st.sidebar.slider("Stress_Level", int(df["Stress_Level"].min()), int(df["Stress_Level"].max()), (int(df["Stress_Level"].min()), int(df["Stress_Level"].max())))
    depression_level_filter = st.sidebar.slider("Depression_Score", int(df["Depression_Score"].min()), int(df["Depression_Score"].max()), (int(df["Depression_Score"].min()), int(df["Depression_Score"].max())))
    
    # Filter the dataframe based on slider values
    filtered_df = df[
        (df["Age"] >= age_filter[0]) & (df["Age"] <= age_filter[1]) &
        (df["CGPA"] >= cgpa_filter[0]) & (df["CGPA"] <= cgpa_filter[1]) &
        (df["Stress_Level"] >= stress_level_filter[0]) & (df["Stress_Level"] <= stress_level_filter[1]) &
        (df["Depression_Score"] >= depression_level_filter[0]) & (df["Depression_Score"] <= depression_level_filter[1])
    ]
    
    # Display the filtered dataframe based on inputs
    st.write("## Filtered Data Based on Inputs")
    st.write(filtered_df)

    # Display statistics for the filtered data
    st.write("## Statistics of Filtered Data")
    st.write(filtered_df.describe())
    
    # Plot options
    plot_types = ["Histogram", "Scatter Plot", "Bar Chart"]
    selected_plot = st.sidebar.selectbox("Select the type of plot", plot_types)
    
    # Select columns for plotting
    if selected_plot in ["Histogram", "Bar Chart"]:
        selected_column = st.sidebar.selectbox("Select column for plotting", columns)
    elif selected_plot == "Scatter Plot":
        x_column = st.sidebar.selectbox("Select X-axis column", columns)
        y_column = st.sidebar.selectbox("Select Y-axis column", columns)
    
    # Generate plots based on selection
    st.write("## Plot")
    if selected_plot == "Histogram" and selected_column in df.columns:
        fig, ax = plt.subplots()
        sns.histplot(filtered_df[selected_column], kde=True, ax=ax)
        st.pyplot(fig)
    
    elif selected_plot == "Scatter Plot" and x_column in df.columns and y_column in df.columns:
        fig, ax = plt.subplots()
        sns.scatterplot(x=filtered_df[x_column], y=filtered_df[y_column], ax=ax)
        st.pyplot(fig)
    
    elif selected_plot == "Bar Chart" and selected_column in df.columns:
        fig, ax = plt.subplots()
        sns.countplot(x=filtered_df[selected_column], ax=ax)
        st.pyplot(fig)
