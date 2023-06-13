import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import io

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))


if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")

    show_relevant_stats = st.checkbox("Relevant Statistics", key="enabled")

    if show_df:
      st.table(df)
    
    if show_relevant_stats:
      categorical_vars = 0
      numerical_vars = 0
      bool_vars = 0
      date_vars = 0

      st.header("    Data Frame Dimension")
      rel1, rel2 = st.columns(2)
      rel1.metric("# Rows", df.shape[0])
      rel2.metric("# Columns", df.shape[1])


      for col in df.columns:
        if df[col].dtype == 'object':
            categorical_vars += 1
        elif df[col].dtype in ['int64', 'float64']:
            numerical_vars += 1
        elif df[col].dtype == 'bool':
            bool_vars += 1
        elif df[col].dtype == 'datetime64[ns]':
            date_vars += 1

      st.header("Variables")
      rel3, rel4, rel5, rel6 = st.columns(4)
      rel3.metric("# Categorical", categorical_vars)
      rel4.metric("# Numerical", numerical_vars)
      rel5.metric("# Boolean", bool_vars)
      rel6.metric("# Date", date_vars)

    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool", "Date"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value = 0.45)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      ax.hist(df[numerical_column], bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )

      st.header("Five Number Summary For the Numerical Column", numerical_column)
      col1, col2, col3, col4= st.columns(4)
      col1.metric("Count", int(df[numerical_column].describe()[0]))
      col2.metric("Mean", round(df[numerical_column].describe()[1],2))
      col3.metric("Standard Deviation", round(df[numerical_column].describe()[2], 2))
      col4.metric("Minimum", df[numerical_column].describe()[3])

      col5, col6, col7, col8 = st.columns(4)
      col5.metric("25th Percentile", df[numerical_column].describe()[4])
      col6.metric("50th Percentile", df[numerical_column].describe()[5])
      col7.metric("75th Percentile", df[numerical_column].describe()[6])
      col8.metric("Maximum", df[numerical_column].describe()[7])

    elif column_type =="Categorical":
      df = pd.DataFrame(df)
      categorical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include="object").columns)
      
      # Barplot
      df_cat = df[categorical_column].value_counts().reset_index()
      df_cat.columns = [categorical_column, "Frequency"]
      choose_color = st.color_picker('Pick a Color', "#CD5C5C")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value = 0.45)

      bar_bins_title = st.text_input('Set Title', 'Barplot')
      bar_xtitle = st.text_input('Set x-axis Title', categorical_column)

      fig, ax = plt.subplots()
      ax.bar(df_cat[categorical_column], height = df_cat["Frequency"], 
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(bar_bins_title)
      ax.set_xlabel(bar_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )

      total_frequency = df_cat['Frequency'].sum()
      df_cat['Proportion'] = df_cat['Frequency'] / total_frequency

      st.header("Table of Proportions for Category", categorical_column)
      st.table(df_cat)
      