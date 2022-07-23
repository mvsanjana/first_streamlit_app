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
#st.multiselect("Pick some fruits: ",list(fruit_df_list.index),['Watermelon','Strawberries'])
selected_fruit_list=st.multiselect("Pick some fruits: ",list(fruit_df_list.index),['Watermelon','Strawberries'])
fruits_to_show=fruit_df_list.loc[selected_fruit_list]
#st.dataframe(fruit_df_list)
st.dataframe(fruits_to_show)

#New section to display fruityvice API response
st.write('#')
st.header('Fruityvice Fruit Advice!!🍎🤗')
import requests as rqs
fruityvice_response = rqs.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)  #Gives Response Code: <Response [200]> instead of watermelon data
st.text(fruityvice_response.json())

#Display in a more beautified format on streamlit
#Take the json version and normalize it (Means, convert semi-structured json data to flat table; keys act as columns, values as rows
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#Output as a table on the screen
streamlit.dataframe(fruityvice_normalized)
