import streamlit as st
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import Economic_data as e
import stock_data as s
fred_key = '25af470e22d07300c84e19895ed91600'



#################### the project :
st.markdown("""

# Economic Data


## Here you can extract and download a veriety of economic data 

- For better results type letters only 



""")
st.title("search your economic data")


# User inputs search term
search_term = st.text_input("Enter a keyword to search for economic data::(GDP,CPI, nonfarm payrol...)", "")



if search_term:
    matching_series = e.get_matching_series(search_term, fred_key)

    if matching_series:
        # Display matching options
        option = st.selectbox("Select the data you want :", [f"{id_}: {note}" for id_, note in matching_series if len(id_) < 15])

        if option:
            # Extract the selected series ID
            selected_id = option.split(":")[0]

            # Fetch and display data for the selected series
            start_data_date = '2000-01-01'
            df = e.get_series_data(selected_id, start_data_date, fred_key)

            if df is not None:
                st.write(f"Data for {selected_id}:")
                st.dataframe(df[['date', 'value','change_from_last']])

                # Optionally, download as CSV
                csv = df.to_csv(index=False)
                st.download_button("Download data as CSV", data=csv, file_name=f"{selected_id}.csv")

                kind_of_graph = ['total value graph', 'presentage change graph']
                type_ = ['value','change_from_last']
                sign =["","%"]
                plot_choice = st.radio("choose what would you like to see",kind_of_graph)
                #plot_choice = st.radio("choose what would you like to see",['total value graph', 'presentage change graph'])  # telling the user to pick
                fig, axe = plt.subplots()  # creat a new figure, get the axes object
                for pick, typ,sig in zip(kind_of_graph,type_,sign):

                    if plot_choice == pick:
                        sns.lineplot(data=df, x="date", y=typ, ax=axe)
                        plt.xticks(ticks=df['date'][::4],rotation=90,fontsize=5)
                        plt.yticks(fontsize=6)
                        st.pyplot(fig)
                        plot_choice2 = st.radio("Any specific value to fetch? "
                                                "(its better to display the presentage change and not the absolut value) "
                                                ,['Max value', 'Min value','Average value','median value','pick a specific date'])
                        if plot_choice2 == 'Min value':
                            min_val = df[typ].min()
                            st.text(f'{min_val}{sig}')
                        if plot_choice2 == 'Max value':
                            max_val = df[typ].max()
                            st.text(f'{max_val}{sig}')
                        if plot_choice2 == 'Average value':
                            average_val = df[typ].mean()
                            st.text(f'{average_val}{sig}')
                        if plot_choice2 == 'median value':
                            median_val = df[typ].median()
                            st.text(f'{median_val}{sig}')
                    #if plot_choice2 == 'Min value':
                     #   st.text(df['value'].min())
                    #if plot_choice2 == 'Max value':
                     #   st.text(df['value'].max())
                    #if plot_choice2 == 'Average value':
                    #    st.text(df['value'].mean())
                    #if plot_choice2 == 'median value':
                    #    st.text(df['value'].median())

                        if plot_choice2 == 'pick a specific date': # to display a specific date
                            selected_year = st.selectbox("Select Year:", sorted(df['year'].unique()))
                            selected_month = st.selectbox("Select Month:", sorted(df['month'].unique()))
                            specific_date = df[(df['year'] == selected_year) & (df['month'] == selected_month)]
                            if not specific_date.empty:
                                st.write("Values for the selected date range:")
                                st.write(specific_date[['date', typ]])
                            else:
                                st.write("No data available for the selected month and year.")

                #if plot_choice == 'presentage change graph':
                 #   sns.lineplot(data=df, x="date", y='change_from_last', ax=axe)
                 #   plt.xticks(ticks=df['date'][::4],rotation=90,fontsize=5)
                 #   plt.yticks(fontsize=6)
                 #   st.pyplot(fig)
                 #   plot_choice2 = st.radio("Any specific value to fetch? "
                  #                          "(its better to display the presentage change and not the absolut value) ",
                  #                          ['Max value', 'Min value', 'Average value','median value','pick a specific date'])
                   # if plot_choice2 == 'Min value':
                   #     min_val = df['change_from_last'].min()
                   #     st.text(f'{min_val}%')
                   # if plot_choice2 == 'Max value':
                   #     max_val = df['change_from_last'].max()
                   #     st.text(f'{max_val}%')
                   # if plot_choice2 == 'Average value':
                   #     average_val = df['change_from_last'].mean()
                   #     st.text(f'{average_val}%')
                   # if plot_choice2 == 'median value':
                   #     median_val = df['change_from_last'].median()
                   #     st.text(f'{median_val}%')

                    #if plot_choice2 == 'pick a specific date':
                     #   selected_year = st.selectbox("Select Year:", sorted(df['year'].unique()))
                      #  selected_month = st.selectbox("Select Month:", sorted(df['month'].unique()))
                       # specific_date = df[(df['year'] == selected_year) & (df['month'] == selected_month)]
                        #if not specific_date.empty:
                         #   st.write("Values for the selected date range:")
                          #  st.write(specific_date[['date', 'change_from_last']])
                        #else:
                        #    st.write("No data available for the selected month and year.")

st.title('Stock data')
search_stock = st.text_input("Enter the ticker of the stock you are looking for :", "")
if search_stock:
    stock_price = s.last_quot_stock_data(search_stock.upper()) #getting the last day closing price
    st.write(stock_price)
    # for history data
    historical_data = s.history_stock_data(search_stock)
    select_year = st.selectbox("select year for the stock data :", [year for year in range(2000,2025)])
    select_month = st.selectbox("select month for the stock data :", [month for month in range(1, 13)])
    select_day = st.selectbox("select day for the stock data :", [day for day in range(1, 32)])
    certain_date = historical_data[(historical_data['year'] == select_year) & (historical_data['month'] == select_month) & (historical_data['day'] == select_day)]
    if not certain_date.empty :
        st.dataframe(certain_date[['Date','Open', 'High', 'Low', 'Close', 'Volume']])
    else:
        st.write("No data available for the selected date.")
    #choose_dates =

