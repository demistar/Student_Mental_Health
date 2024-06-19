import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

st.snow()
# Title of the Streamlit app
st.title("`Student Mental Health Analysis`")
st.markdown("---")
st.subheader(":clap:`About`")
st.write("""
Our Streamlit web app for `student mental health analysis` provides a user-friendly platform designed to support students' well-being. 
Leveraging data analytics and visualization, the app allows students to anonymously input their mental health metrics and receive 
instant feedback on their mental well-being. The app features interactive charts and insights that help identify patterns and potential 
areas of concern, offering valuable resources and recommendations tailored to individual needs. By promoting awareness and understanding 
of mental health, our app aims to create a supportive environment that fosters emotional and psychological resilience among students.
""")
st.markdown("---")

# Sidebar for uploading the dataset
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the dataset
    df = pd.read_csv(uploaded_file)
    st.success(":wave: `Welcome, Your Data is successfully imported !!!`")
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
    
    # Identify numeric columns for sliders
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if 'Age' in numeric_columns:
        age_filter = st.sidebar.slider("Age", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))
    if 'CGPA' in numeric_columns:
        cgpa_filter = st.sidebar.slider("CGPA", float(df["CGPA"].min()), float(df["CGPA"].max()), (float(df["CGPA"].min()), float(df["CGPA"].max())))
    if 'Stress_Level' in numeric_columns:
        stress_level_filter = st.sidebar.slider("Stress Level", int(df["Stress_Level"].min()), int(df["Stress_Level"].max()), (int(df["Stress_Level"].min()), int(df["Stress_Level"].max())))
    if 'Depression_Score' in numeric_columns:
        depression_level_filter = st.sidebar.slider("Depression Score", int(df["Depression_Score"].min()), int(df["Depression_Score"].max()), (int(df["Depression_Score"].min()), int(df["Depression_Score"].max())))

    # Apply filters if numeric columns exist
    if 'Age' in numeric_columns:
        filtered_df = filtered_df[(filtered_df["Age"] >= age_filter[0]) & (filtered_df["Age"] <= age_filter[1])]
    if 'CGPA' in numeric_columns:
        filtered_df = filtered_df[(filtered_df["CGPA"] >= cgpa_filter[0]) & (filtered_df["CGPA"] <= cgpa_filter[1])]
    if 'Stress_Level' in numeric_columns:
        filtered_df = filtered_df[(filtered_df["Stress_Level"] >= stress_level_filter[0]) & (filtered_df["Stress_Level"] <= stress_level_filter[1])]
    if 'Depression_Score' in numeric_columns:
        filtered_df = filtered_df[(filtered_df["Depression_Score"] >= depression_level_filter[0]) & (filtered_df["Depression_Score"] <= depression_level_filter[1])]

    # Display the filtered dataframe based on inputs
    st.write("## Filtered Data Based on Inputs")
    st.write(filtered_df)

    # Display statistics for the filtered data
    st.write("## Statistics of Filtered Data")
    st.write(filtered_df.describe())
    
    # Plot options
    plot_types = ["Histogram", "Scatter Plot", "Bar Chart", "Box Plot", "Violin Plot", "Pair Plot", "Heatmap"]
    selected_plot = st.sidebar.selectbox("Select the type of plot", plot_types)
    
    # Handle non-numeric columns for plots
    le = LabelEncoder()
    encoded_df = filtered_df.copy()
    for column in filtered_df.select_dtypes(include=['object']).columns:
        encoded_df[column] = le.fit_transform(filtered_df[column])
    
    # Select columns for plotting
    if selected_plot in ["Histogram", "Bar Chart", "Box Plot", "Violin Plot"]:
        selected_column = st.sidebar.selectbox("Select column for plotting", columns)
    elif selected_plot == "Scatter Plot":
        x_column = st.sidebar.selectbox("Select X-axis column", columns)
        y_column = st.sidebar.selectbox("Select Y-axis column", columns)
    elif selected_plot == "Pair Plot":
        pair_columns = st.sidebar.multiselect("Select columns for pair plot", columns, default=columns[:2])
    elif selected_plot == "Heatmap":
        heatmap_columns = st.sidebar.multiselect("Select columns for heatmap", columns, default=columns)
    
    # Generate plots based on selection
    st.write("## Plot")
    if selected_plot == "Histogram" and selected_column in encoded_df.columns:
        fig, ax = plt.subplots()
        sns.histplot(encoded_df[selected_column], kde=True, ax=ax, color="skyblue")
        ax.set_title(f'Histogram of {selected_column}')
        st.pyplot(fig)
    
    elif selected_plot == "Scatter Plot" and x_column in encoded_df.columns and y_column in encoded_df.columns:
        fig, ax = plt.subplots()
        sns.scatterplot(x=encoded_df[x_column], y=encoded_df[y_column], ax=ax, color="coral")
        ax.set_title(f'Scatter Plot of {x_column} vs {y_column}')
        st.pyplot(fig)
    
    elif selected_plot == "Bar Chart" and selected_column in encoded_df.columns:
        fig, ax = plt.subplots()
        sns.countplot(x=encoded_df[selected_column], ax=ax, palette="viridis")
        ax.set_title(f'Bar Chart of {selected_column}')
        st.pyplot(fig)

    elif selected_plot == "Box Plot" and selected_column in encoded_df.columns:
        fig, ax = plt.subplots()
        sns.boxplot(x=encoded_df[selected_column], ax=ax, palette="pastel")
        ax.set_title(f'Box Plot of {selected_column}')
        st.pyplot(fig)

    elif selected_plot == "Violin Plot" and selected_column in encoded_df.columns:
        fig, ax = plt.subplots()
        sns.violinplot(x=encoded_df[selected_column], ax=ax, palette="muted")
        ax.set_title(f'Violin Plot of {selected_column}')
        st.pyplot(fig)

    elif selected_plot == "Pair Plot" and all(col in encoded_df.columns for col in pair_columns):
        fig = sns.pairplot(encoded_df[pair_columns], palette="husl")
        st.pyplot(fig)

    elif selected_plot == "Heatmap" and all(col in encoded_df.columns for col in heatmap_columns):
        fig, ax = plt.subplots()
        sns.heatmap(encoded_df[heatmap_columns].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title('Heatmap of Correlations')
        st.pyplot(fig)