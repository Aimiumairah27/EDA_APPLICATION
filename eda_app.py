import streamlit as st  
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# Page configuration
st.set_page_config(page_title="Complete EDA Application", page_icon="📊", layout="wide")

# Heading
st.title("📊 Complete EDA Application")
st.markdown("📂 Easily upload your dataset and start analyzing it right away!")

# File uploader
uploaded_file = st.file_uploader(
    "📂 Choose Your Data File",
    type=["csv", "xlsx", "xls", "txt", "json", "xml"],
    key="eda_upload_unique"
)

df = None  # initialize df

if uploaded_file is not None:
    try:
        uploaded_file.seek(0)  # reset file pointer

        # Load CSV or Excel safely
        if uploaded_file.name.endswith(".csv"):
            if uploaded_file.size == 0:
                st.warning("⚠️ Uploaded CSV is empty. Please upload a valid dataset.")
            else:
                try:
                    df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
                except UnicodeDecodeError:
                    df = pd.read_csv(uploaded_file, encoding='latin1')
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("⚠️ Unsupported file type.")

        # Check if df is empty
        if df is None or df.empty:
            st.warning("⚠️ Dataset kosong atau tiada baris. Sila upload fail lain.")
        else:
            st.success(f"File loaded successfully! Shape: {df.shape}")

            # 🧾 Data Preview
            st.subheader("🧾 Data Preview")
            st.dataframe(df.head())

            # 📊 Dataset Information
            st.subheader("📊 Dataset Information")
            st.write("Total Columns:", len(df.columns))
            st.write("Missing Values:", df.isnull().sum().sum())
            st.write("Duplicate Rows:", df.duplicated().sum())
            st.write("Column Data Types:")
            st.write(df.dtypes)

            # Visualization Playground
            st.subheader("Visualization Playground")
            numeric_cols = df.select_dtypes(include='number').columns.tolist()
            categorical_cols = df.select_dtypes(exclude='number').columns.tolist()

            if categorical_cols and numeric_cols:
                x_col = st.selectbox("Select X-axis Column (Categorical Preferred)", categorical_cols, key="x_col")
                y_col = st.selectbox("Select Y-axis Column (Numeric Only)", numeric_cols, key="y_col")
                color = st.color_picker("Pick a color for the chart", "#FF6347")
                chart_type = st.radio("Select Chart Type", ["Bar Chart", "Scatter Plot"], key="chart_type")

                if st.button("Generate Chart", key="generate_chart"):
                    fig, ax = plt.subplots()
                    if chart_type == "Bar Chart":
                        ax.bar(df[x_col], df[y_col], color=color)
                    else:
                        ax.scatter(df[x_col], df[y_col], color=color)
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                    ax.set_title(chart_type)
                    st.pyplot(fig)
            else:
                st.warning("Not enough numeric or categorical columns for chart plotting.")

            # 🔥 Distribution Analysis (Histogram)
            st.subheader("📊 Distribution Analysis (Histogram)")
            if numeric_cols:
                hist_col = st.selectbox("Select a numeric column for histogram", numeric_cols, key="hist_col")
                bins = st.slider("Number of bins", min_value=5, max_value=50, value=10, key="bins_slider")
                if st.button("Plot Histogram", key="plot_hist"):
                    fig, ax = plt.subplots()
                    ax.hist(df[hist_col], bins=bins, color="#1f77b4")
                    ax.set_title(f"Histogram of {hist_col}")
                    st.pyplot(fig)
            else:
                st.warning("No numeric columns available for histogram.")

            # 🔥 Correlation Heatmap
            st.subheader("🔥 Correlation Heatmap")
            numeric_df = df.select_dtypes(include='number')

            if len(numeric_df.columns) > 1:
                if st.button("Generate Correlation Heatmap", key="corr_heatmap"):
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
                    st.pyplot(fig)
            else:
                st.warning("Not enough numeric columns available for correlation heatmap.")

    except pd.errors.EmptyDataError:
        st.error("⚠️ File kosong. Sila upload fail sah.")
    except Exception as e:
        st.error(f"⚠️ Error reading the file: {e}")
else:
    st.info("📁 Please upload a data file to start exploring and visualizing your dataset.")
