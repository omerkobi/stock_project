import streamlit as st
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import Economic_data as e
import stock_data as s
import pandas as pd
fred_key = st.secrets['fred_key']



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
                st.dataframe(df[['date', 'value','change_from_last','yearly_change']])

                # Optionally, download as CSV
                csv = df.to_csv(index=False)
                st.download_button("Download data as CSV", data=csv, file_name=f"{selected_id}.csv")

                kind_of_graph = ['total value graph', 'Quarterly percentage change','Yearly percentage change']
                type_ = ['value','change_from_last','yearly_change']
                sign =["","%","%"]
                plot_choice = st.radio("choose what would you like to see",kind_of_graph) # telling the user to pick
                for pick, typ,sig in zip(kind_of_graph,type_,sign): # iterate over the 3 list to display the desiered data

                    if plot_choice == pick:
                        graph_choice = st.radio("line graph or scatterplot ?",['line','scatter'])
                        if graph_choice == 'line':
                            fig, axe = plt.subplots()  # creat a new figure, get the axes object
                            sns.lineplot(data=df, x="date", y=typ, ax=axe)
                            plt.xticks(ticks=df['date'][::4],rotation=90,fontsize=5)
                            plt.yticks(fontsize=6)
                            st.pyplot(fig)
                        elif graph_choice == 'scatter':
                            fig = px.scatter(df,x= 'date', y=typ, title= 'Data by Date')
                            st.plotly_chart(fig)

                        plot_choice2 = st.radio("Any specific value to fetch? "
                                                "(its better to display the presentage change and not the absolut value) "
                                                ,['Max value', 'Min value','Average value','median value','pick a specific date'])
                        if plot_choice2 == 'Min value':
                            min_val = df[typ].min()
                            min_index = df[typ].idxmin()
                            min_date = df.at[min_index,'date']
                            st.text(f'the lowest reading is {min_val}{sig} at {min_date}')
                        elif plot_choice2 == 'Max value':
                            max_val = df[typ].max()
                            max_index = df[typ].idxmax()
                            max_date = df.at[max_index, 'date']
                            st.text(f'the highest reading is {max_val}{sig} at {max_date}')
                        elif plot_choice2 == 'Average value':
                            average_val = round(df[typ].mean(),2)
                            st.text(f'{average_val}{sig}')
                        elif plot_choice2 == 'median value':
                            median_val = df[typ].median()
                            st.text(f'{median_val}{sig}')


                        if plot_choice2 == 'pick a specific date': # to display a specific date
                            selected_year = st.selectbox("Select Year:", sorted(df['year'].unique()))
                            selected_month = st.selectbox("Select Month:", sorted(df['month'].unique()))
                            specific_date = df[(df['year'] == selected_year) & (df['month'] == selected_month)]
                            if not specific_date.empty:
                                st.write("Values for the selected date range:")
                                st.write(specific_date[['date', typ]])
                            else:
                                st.write("No data available for the selected month and year.")

    else:
        st.write("No data available for your search, try another keyword.")

###### Stock DATA : ###### this section is to provide a desire stock data
st.title('Stock data')
search_stock = st.text_input("Enter the ticker of the stock you are looking for :", "")
if search_stock:
    stock_price = s.last_quot_stock_data(search_stock.upper()) #getting the last day closing price
    #try:
    if stock_price is not None:
        curr_price = f"Current Price of {search_stock}: ${stock_price:.2f}"
        st.write(curr_price)
    else:
        st.write("no such TICKER exist")
    #except IndexError :
     #   st.error(f"No data found for stock: {search_stock.upper()}")
    # for history data
    historical_data = s.history_stock_data(search_stock) # getting a data fram with historical stock data
    select_year = st.selectbox("select year for the stock data :", [year for year in range(2000,2025)])
    select_month = st.selectbox("select month for the stock data :", [month for month in range(1, 13)])
    select_day = st.selectbox("select day for the stock data :", [day for day in range(1, 32)])
    certain_date = historical_data[(historical_data['year'] == select_year) & (historical_data['month'] == select_month) & (historical_data['day'] == select_day)]
    if not certain_date.empty :
        st.dataframe(certain_date[['Date','Open', 'High', 'Low', 'Close', 'Volume']])
    else:
        st.write("No data available for the selected date.")
    #choose_dates =
    correl= st.radio("would you like to check for correlation to other tickers?", ['Yes','No'])
    if correl == 'Yes':
        search_stock2 = st.text_input("Enter the ticker of the stock you would like to check correlation  :", "")
        if search_stock2:
            hist_for_corr = s.history_stock_data(search_stock2.upper())
            corelation = historical_data['Close'].corr(hist_for_corr['Close'])
            st.write(f"the correlation is : {corelation}")
            combined_df = pd.concat([historical_data[['Open','High', 'Low', 'Close']], hist_for_corr[['Open','High', 'Low', 'Close']]], axis=1)
            combined_df.columns = [f'Open{search_stock}', f'High{search_stock}', f'Low{search_stock}', f'Close{search_stock}', f'Open{search_stock2}', f'High{search_stock2}', f'Low{search_stock2}', f'Close{search_stock2}']
            correlation_matrix = combined_df.corr()
            plt.figure(figsize=(10, 8))  # Optional: Adjust figure size
            heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
            st.pyplot(plt)
else:
    st.write("such TICKER does not exist, the ticker needs to be 2-4 english letters. for example you can try : AAPL,MSFT,WFC,TSLA")
