import streamlit as st
import pandas as pd
import requests as rqs
import snowflake.connector
from urllib.error import URLError

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

#Create the repeatable code block (Called function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = rqs.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

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
#fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
#st.write('The user entered ', fruit_choice)
#fruityvice_response = rqs.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#Take the json version and normalize it (Means, convert semi-structured json data to flat table; keys act as columns, values as rows
#fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#Output as a table on the screen
#st.dataframe(fruityvice_normalized)

#The below structure allows us to separate the code that is loaded once from the code that should be repeated each time a new value is entered. Thereby Control of flow
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
  else:
    #fruityvice_response = rqs.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    #fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    back_from_function =  get_fruityvice_data(fruit_choice)
    st.dataframe(back_from_function)
except URLError as e:
  st.error()

#Don't let execution past this point (Stop Snowflake execution). Only till Fruityvice part
#st.stop()
#Test connection to Snowflake from Streamlit by querying Snowflake account details
#import snowflake.connector
#my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#st.text("Hello from Snowflake:")
#st.text(my_data_row)

#Query data from Snowflake fruit_load_list
#my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("select * from fruit_load_list")
##my_data_row = my_cur.fetchone()
#my_data_rows = my_cur.fetchall()
#st.header("The fruit load list contains: ")
#st.text(my_data_row)
#st.dataframe(my_data_row)
#st.dataframe(my_data_rows)

st.header("The fruit load list contains: ")
#Snowflake related functions
def get_fruit_load_list(cnx):
  with cnx.cursor() as cur:
    cur.execute("select * from fruit_load_list")
    return cur.fetchall()
  
#Add a button to load the fruit
if st.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list(my_cnx)
  st.dataframe(my_data_rows)

#Don't let execution past this point (Stop Snowflake execution). Only till Fruityvice part
#st.stop()
#Add another text box and display the fruit entered in the box
#fruit_add = st.text_input('What fruit would you like to add?','Kiwi')
#st.write('Thanks for adding ',fruit_add)

#Check if insertion to fruit_load_list in Snowflake works. Interact with all the text/selection boxes in the app. This will highlight issue with Control of Flow.
#my_cur.execute("insert into fruit_load_list values('from streamlit')") #This will not go correctly bu just go with it for now

#Allow the end user to add a fruit to the list
def insert_new_row_snowflake(new_fruit, cnx):
  with cnx.cursor() as cur:
    #cur.execute("insert into fruit_load_list values('from streamlit')");
    cur.execute("insert into fruit_load_list values('"+new_fruit+"')");
    return "Thanks for adding "+new_fruit

#Add a button to insert row into snowflake
fruit_add = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  add_row = insert_new_row_snowflake(fruit_add, my_cnx)
  st.text(add_row)
