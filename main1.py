import streamlit as st
import seaborn as sns
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
