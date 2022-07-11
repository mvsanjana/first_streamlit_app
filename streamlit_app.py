import streamlit as st

st.title('Sanjana\'s Sweet Corner🍯')

#Dessert
st.header('Today\'s Dessert Menu🍨')

st.text('🍦Vanilla Ice Cream\t\t\t\t\tRs. 20')
st.text('🍧Shaved Ice\t\t\t\t\t\tRs. 25')
st.text('🍰Strawberry Cake\t\t\t\t\tRs. 55')
st.text('🎂Chocolate Cake\t\t\t\t\tRs. 65')
st.text('🍪Choco-chip Cookies\t\t\t\t\tRs. 30')
st.text('🍩Choco glazed Doughnut\t\t\t\t\tRs. 20')
st.text('🧁Chocolate Cupcake with Strawberry frosting\t\tRs. 35')
st.text('🥧Apple Pie\t\t\t\t\t\tRs. 35')

#Fruit
import pandas as pd
st.write('#')
st.header('Build your own Fruit Smoothie🍎')
fruit_df_list=pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include 
fruit_df_list=fruit_df_list.set_index('Fruit')
#st.multiselect("Pick some fruits: ",list(fruit_df_list.index))
st.multiselect("Pick some fruits: ",list(fruit_df_list.index),['Mango','Strawberries'])
st.dataframe(fruit_df_list)
