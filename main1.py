import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
st.markdown("""

# Title



## Subtitle

- bullet1
- bullet2
- bullet3


> Amazing Quote
""")
st.radio("what kind of data would ypu like to see",['economic date','stock data'])

df=sns.load_dataset("penguins")
plot_choice = st.radio("choose what would you like to see",['economic data','stock data']) # telling the user to pick
fig, axe = plt.subplots() # creat a new figure, get the axes object
sns.scatterplot(data=df,x= "flipper_length_mm", y= "bill_length_mm", hue="species", ax = axe)
st.pyplot(fig)

