import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("Building a restaurant, aren't we?")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(fru):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fru)
    return pandas.json_normalize(fruityvice_response.json())
       

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        streamlit.write('The user entered ', fruit_choice)
        streamlit.dataframe(get_fruityvice_data(fruit_choice))
        
except URLError:
    streamlit.error()

def get_fruit_load_list(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * from fruit_load_list")
        return cur.fetchall()

if streamlit.button("Get fruit load list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.header("The fruit load list contains:")
    streamlit.dataframe(get_fruit_load_list(my_cnx))
    my_cnx.close()

def insert_row_snowflake(conn, fruit):
    with conn.cursor() as cur:
        cur.execute(f"insert into fruit_load_list values ('{fruit}')")
        return "Thanks for adding " + fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add')
if streamlit.button("Add to the fruit list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.text(insert_row_snowflake(my_cnx, add_my_fruit))
    my_cnx.close()

