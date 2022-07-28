import streamlit as st
import pandas as pd
import requests as rqs
import snowflake.connector
from urllib.erro import URLError

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
#import pandas as pd
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
#import requests as rqs
st.write('#')
st.header('Fruityvice Fruit Advice!!🍎🤗')
#fruityvice_response = rqs.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)  #Gives Response Code: <Response [200]> instead of watermelon data
#st.text(fruityvice_response.json())   #Displays in json format, not in the form of a table

#Display in a more beautified format on streamlit
#Take the json version and normalize it (Means, convert semi-structured json data to flat table; keys act as columns, values as rows
#fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#Output as a table on the screen
#st.dataframe(fruityvice_normalized)

#Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)
fruityvice_response = rqs.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#Take the json version and normalize it (Means, convert semi-structured json data to flat table; keys act as columns, values as rows
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#Output as a table on the screen
st.dataframe(fruityvice_normalized)

#Don't let execution past this point (Stop Snowflake execution). Only till Fruityvice part
st.stop()
#Test connection to Snowflake from Streamlit by querying Snowflake account details
#import snowflake.connector
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
st.text("Hello from Snowflake:")
st.text(my_data_row)

#Query data from Snowflake fruit_load_list
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
st.text("The fruit load list contains: ")
#st.text(my_data_row)
#st.dataframe(my_data_row)
st.dataframe(my_data_rows)

#Add another text box and display the fruit entered in the box
fruit_add = st.text_input('What fruit would you like to add?','Kiwi')
st.write('Thanks for adding ',fruit_add)

#Check if insertion from streamlit into fruit_load_list in Snowflake will work. Interact with all the text/selection boxes in the app
my_cur.execute("insert into fruit_load_list values('from streamlit')");    #This line will highlight issue with Control of Flow
