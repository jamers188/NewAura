import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt
from PIL import Image
import gspread
from gspread_dataframe import set_with_dataframe
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import time

# Formatting the page
im = Image.open('r2s3.png')
st.set_page_config(page_title="Race to Hills 2024", page_icon=im)
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('racetosand.json', scope)
client = gspread.authorize(creds)
sh = client.open("Data")

today = dt.date.today()
finalen = dt.date(2024, 9, 7)
diff = finalen - today
diff_days = diff.days

# Title and logo layout
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

with col2:
    st.image('r2s3.png')

with col3:
    st.write(' ')

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

with col2:
    st.title('Race to Hills 2024')

with col3:
    st.write(' ')

st.divider()

# Tabs at the top and adding a divider
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ['🏆 Leaderboard', '📅 Spelschema', '💸 Böteskassa', '📸 Bilder', '⏱️ Countdown', 'Uppdatera leaderboard', 'Golf-id'])

st.divider()  # Divider under the tabs

# Function to get data
def get_leaderboard(num):
    df = pd.DataFrame(sh.get_worksheet(num).get_all_records())
    return df

def get_plotdata_boter(sheetname):
    df = pd.DataFrame(sh.worksheet(sheetname).get_all_records())
    return df

@st.cache_data
def get_data(sheetname):
    df = pd.DataFrame(sh.worksheet(sheetname).get_all_records())
    return df

df_comps = get_data('Spelschema')
df_boter = get_plotdata_boter('Böteskassa')
df_points = get_data('Poangsystem')
df_points.set_index('Antal spelare', inplace=True)
df_points_major = get_data('Poangsystem major')
df_points_major.set_index('Antal spelare', inplace=True)
df_plotdata = get_plotdata_boter('Leaderboard Utveckling')

num_worksheets = len(sh.worksheets()) - 1
df_leaderboard = get_leaderboard(num_worksheets)

# Leaderboard tab
tab1.header("Leaderboard 2024")
tab1.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal spelade tävlingar', 'Poäng']].sort_values('Poäng', ascending=False), hide_index=True, column_config={'Spelarbild': st.column_config.ImageColumn()})

tab1.subheader("Utveckling Leaderboard 2024")
tab1.line_chart(df_plotdata.sort_values('Poäng'), x='Deltävling', y='Poäng', color='Spelare', width=800, height=500)

tab1.divider()

tab1.header("Antal vinster under året:")
tab1.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal vinster']].sort_values('Antal vinster', ascending=False), hide_index=True, column_config={'Spelarbild': st.column_config.ImageColumn()})

tab1.divider()

tab1.header("Antal sistaplatser under året:")
tab1.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal förluster']].sort_values('Antal förluster', ascending=False), hide_index=True, column_config={'Spelarbild': st.column_config.ImageColumn()})

# Spelschema tab
tab2.header("Spelschema 2024")
tab2.dataframe(df_comps, use_container_width=True, hide_index=True, column_config={' ': st.column_config.ImageColumn()})

# Böteskassa tab
tab3.header("Böteskassa")
bot = df_boter.iloc[0, 1]
tab3.write('Böteskassan ligger för närvarande på: {:}kr'.format(bot))
tab3.divider()
tab3.subheader("Böteslista")
tab3.write("Har ej straffutrustning: 1000kr")
tab3.write("HIO/Albatross, resterande spelare: 100kr")
tab3.write("Kasta utrustning: 50kr/gång")
tab3.write("Kissa på banan: 50kr")
tab3.write("Tappa bort järnheadcovers: 50kr/styck")
tab3.write("Inte på golfbanan 30 min innan start: 50kr")
tab3.write("Biraboll: 20kr")
tab3.write("Streck/0 poäng: 10kr/streck")

# Bilder tab
tab4.image("bild1.jpg")
tab4.image("bild2.jpeg")
tab4.image("bild3.jpeg")
tab4.image("bild4.jpeg")
tab4.image("bild5.jpg")

# Countdown tab
tab5.header('Nedräkning till finalen')
tab5.write('Nu är det endast {:} dagar kvar till finalen. TAGGA!!'.format(diff_days))
tab5.image("beer.jpg")

# Uppdatera leaderboard tab
tab6.header("Här kan du uppdatera leaderboarden efter tävling")
comp = tab6.selectbox('Vilken deltävling?', ('', '1. LaGK HB', '2. LaGK EB', '3. St. Arild', '4. LaGK EB', '5. Sjöbo', '6. St Ibb'), index=None, key='tävling', placeholder=' ')
num_players = tab6.selectbox('Hur många spelare var med i deltävlingen?', ('', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'), index=None, key='antal', placeholder=' ')
players = tab6.multiselect('Vilka spelare var med?', (' ', 'Axel', 'Crille', 'Jojo', 'Frasse', 'Rantzow', 'Alvin', 'Benne', 'Löken', 'Sebbe', 'Dempa', 'Vigge'), key='spelare', placeholder='')
major_flag = tab6.selectbox('Var tävlingen en major?', ('', 'Ja', 'Nej'), index=None, key='major', placeholder=' ')
tab6.divider()

# Golf-id tab
tab7.header('Golf-id:')
tab7.write("Axel: 980512-009")
tab7.write("Rantzow: 990314-001")
tab7.write("Sebbe: 970920-028")
tab7.write("Frasse: 980422-030")
tab7.write("Benne: 980627-033")
tab7.write("Löken: 981226-002")
tab7.write("Dempa: 981124-006")
tab7.write("Jojo: 990920-005")
tab7.write("Alvin: 961029-001")
tab7.write("Vigge: 980703-003")
tab7.write("Crille: 970317-002")
