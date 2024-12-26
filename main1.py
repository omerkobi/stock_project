import streamlit as st
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import Economic_data as e
fred_key = '25af470e22d07300c84e19895ed91600'



#################### the project :
st.markdown("""

# Economic Data


## Here you can extract and download a veriety of economic data 

- For better results type letters only 


> Amazing Quote
""")
st.title("search your economic data")
# User inputs search term
search_term = st.text_input("Enter a keyword to search for economic data::(GDP,CPI, nonfarm payrol...)", "")



if search_term:
    matching_series = e.get_matching_series(search_term, fred_key)

    if matching_series:
        # Display matching options
        option = st.selectbox("Select a matching series:", [f"{id_}: {note}" for id_, note in matching_series])

        if option:
            # Extract the selected series ID
            selected_id = option.split(":")[0]

            # Fetch and display data for the selected series
            start_data_date = '2000-01-01'
            df = e.get_series_data(selected_id, start_data_date, fred_key)

            if df is not None:
                st.write(f"Data for {selected_id}:")
                st.dataframe(df)

                # Optionally, download as CSV
                csv = df.to_csv(index=False)
                st.download_button("Download data as CSV", data=csv, file_name=f"{selected_id}.csv")
                plot_choice = st.radio("choose what would you like to see",['total value graph', 'presentage change graph'])  # telling the user to pick
                fig, axe = plt.subplots()  # creat a new figure, get the axes object
                if plot_choice == 'total value graph':
                    sns.lineplot(data=df, x="date", y="value", ax=axe)
                    plt.xticks(ticks=df['date'][::4],rotation=90,fontsize=5)
                    plt.yticks(fontsize=6)
                    st.pyplot(fig)
                    plot_choice2 = st.radio("Any specific value to fetch? "
                                            "(its better to display the presentage change and not the absolut value) ",['Max value', 'Min value','Average value'])
                    if plot_choice2 == 'Min value':
                        st.text(df['value'].min())
                    if plot_choice2 == 'Max value':
                        st.text(df['value'].max())
                    if plot_choice2 == 'Average value':
                        st.text(df['value'].mean())
                if plot_choice == 'presentage change graph':
                    sns.lineplot(data=df, x="date", y='change_from_last', ax=axe)
                    plt.xticks(ticks=df['date'][::4],rotation=90,fontsize=5)
                    plt.yticks(fontsize=6)
                    st.pyplot(fig)
                    plot_choice2 = st.radio("Any specific value to fetch? "
                                            "(its better to display the presentage change and not the absolut value) ",
                                            ['Max value', 'Min value', 'Average value','median value'])
                    if plot_choice2 == 'Min value':
                        min_val = df['change_from_last'].min()
                        st.text(f'{min_val}%')
                    if plot_choice2 == 'Max value':
                        max_val = df['change_from_last'].max()
                        st.text(f'{max_val}%')
                    if plot_choice2 == 'Average value':
                        average_val = df['change_from_last'].mean()
                        st.text(f'{average_val}%')
                    if plot_choice2 == 'median value':
                        median_val = df['change_from_last'].median()
                        st.text(f'{median_val}%')


