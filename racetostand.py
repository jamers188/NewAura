import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt
from PIL import Image
#from streamlit_gsheets import GSheetsConnection
import gspread
from gspread_dataframe import set_with_dataframe
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import time

# Formattering av sidan
im = Image.open('r2s3.png')
st.set_page_config(page_title="Race to Hills 2024", page_icon = im)
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('racetosand.json', scope)
client = gspread.authorize(creds)
sh = client.open("Data")


today = dt.date.today()
finalen = dt.date(2024, 9, 7)
diff = finalen - today
diff_days = diff.days

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

# selection = st.radio("Välkommen till en liten samlingssida för Race to Hills 2024! Välj bland nedan menyer:", ('Bilder', 'Leaderboard', 'Spelschema', 'Böteskassa', 'Countdown'), horizontal=True)
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['🏆 Leaderboard', '📅 Spelschema', '💸 Böteskassa', '📸 Bilder', '⏱️ Countdown', 'Uppdatera leaderboard', 'Golf-id'])


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

num_worksheets = len(sh.worksheets())-1
df_leaderboard = get_leaderboard(num_worksheets)

# Leaderboardtab
tab1.header("Leaderboard 2024")
tab1.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal spelade tävlingar', 'Poäng']].sort_values('Poäng', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})

tab1.subheader("Utveckling Leaderboard 2024")
tab1.line_chart(df_plotdata.sort_values('Poäng'), x='Deltävling', y='Poäng', color='Spelare', width=800, height=500)

tab1.divider()

tab1.header("Antal vinster under året:")
tab1.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal vinster']].sort_values('Antal vinster', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})

tab1.divider()

tab1.header("Antal sistaplatser under året:")
tab1.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal förluster']].sort_values('Antal förluster', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})

# Spelschematab
tab2.header("Spelschema 2024")
tab2.dataframe(df_comps, use_container_width=True, hide_index=True, column_config={' ':st.column_config.ImageColumn()}) 

# Böteskassatab
tab3.header("Böteskassa")
bot = df_boter.iloc[0,1]
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

#Bildtab
tab4.image("bild1.jpg")
tab4.image("bild2.jpeg")
tab4.image("bild3.jpeg")
tab4.image("bild4.jpeg")
tab4.image("bild5.jpg")

#Countdowntab
tab5.header('Nedräkning till finalen')
tab5.write('Nu är det endast {:} dagar kvar till finalen. TAGGA!!'.format(diff_days))
tab5.image("beer.jpg")


#Uppdatera leaderboard
tab6.header("Här kan du uppdatera leaderboarden efter tävling")
comp = tab6.selectbox('Vilken deltävling?', ('','1. LaGK HB', '2. LaGK EB', '3. St. Arild', '4. LaGK EB', '5. Sjöbo', '6. St Ibb'),index=None, key='tävling', placeholder=' ')
num_players = tab6.selectbox('Hur många spelare var med i deltävlingen?', ('','3', '4', '5', '6', '7', '8', '9', '10', '11', '12'),index=None, key='antal', placeholder=' ')
players = tab6.multiselect('Vilka spelare var med?', (' ','Axel', 'Crille', 'Jojo', 'Frasse', 'Rantzow', 'Alvin', 'Benne', 'Löken', 'Sebbe', 'Dempa', 'Vigge'), key='spelare', placeholder='')
major_flag = tab6.selectbox('Var tävlingen en major?', ('','Ja', 'Nej'), index=None, key='major', placeholder=' ')
tab6.divider()

alla_spelare = ['Axel', 'Jojo', 'Benne', 'Rantzow', 'Crille', 'Löken', 'Alvin', 'Vigge', 'Frasse', 'Sebbe', 'Dempa']

if major_flag == 'Nej':
    df_to_plot = pd.DataFrame(columns=['Spelare', 'Poäng', 'Deltävling'])
    num_players_str = num_players
    if len(players) != int(num_players):
        tab6.write("Något är fel... Antal spelare stämmer inte överrens med de spelare du sagt är med i tävlingen")
    else:
        tot_points = []
        for spelare in alla_spelare:
            if spelare in players:
                placering = tab6.number_input("Vilken placering fick {:}?".format(spelare), 1, int(num_players), "min", 1, key='placering{:}'.format(spelare))
                placering = str(placering)
                points = df_points.loc[int(num_players), placering]
                points = float(points)
                tidigare_points = df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Poäng']
                tidigare_points = float(tidigare_points)
                ny_points = tidigare_points+points
                tidigare_comps = df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal spelade tävlingar']
                tidigare_comps = int(tidigare_comps)
                ny_comps = tidigare_comps + 1
                df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Poäng'] = ny_points
                df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal spelade tävlingar'] = ny_comps
                if placering == num_players_str:
                    tidigare_loss = df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal förluster'] 
                    ny_loss = int(tidigare_loss) + 1
                    df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal förluster'] = ny_loss
                if placering == '1':
                    tidigare_wins = df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal vinster'] 
                    ny_wins = int(tidigare_wins) + 1
                    df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal vinster'] = ny_wins

                info = [spelare, ny_points, comp]
                df_to_plot.loc[len(df_to_plot)] = info
                # df_to_plot = df_to_plot.append(pd.DataFrame(info, columns=['Spelare', 'Poäng', 'Deltävling'], ignore_index=True))

            else:   
                tidigare_points = df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Poäng']
                tidigare_points = float(tidigare_points)
                info = [spelare, tidigare_points, comp]
                df_to_plot.loc[len(df_to_plot)] = info
        time.sleep(10)
        
        tab6.subheader("Uppdaterad Leaderboard:")
        tab6.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal spelade tävlingar', 'Poäng']].sort_values('Poäng', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})
        
        tab6.divider()
   
        def clear_box():
            global df_leaderboard
            global df_plotdata
            global df_to_plot
            df_plotdata = pd.concat([df_plotdata, df_to_plot], axis=0)
            worksheet = sh.add_worksheet(title=comp, rows=100, cols=20)
            worksheet.update([df_leaderboard.columns.values.tolist()] + df_leaderboard.values.tolist())
            worksheet_plot = sh.worksheet('Leaderboard Utveckling')
            worksheet_plot.clear()
            worksheet_plot.update([df_plotdata.columns.values.tolist()] + df_plotdata.values.tolist())
            tab6.write("Leaderboard uppdaterad")

            st.session_state['tävling'] = ""
            st.session_state['antal'] = ""
            st.session_state['spelare'] = " "
            st.session_state['major'] = ""

        upd = tab6.button("Uppdatera Leaderboard", type='primary', on_click=clear_box)



if major_flag == 'Ja':
    df_to_plot = pd.DataFrame(columns=['Spelare', 'Poäng', 'Deltävling'])
    num_players_str = num_players
    if len(players) != int(num_players):
        tab6.write("Något är fel... Antal spelare stämmer inte överrens med de spelare du sagt är med i tävlingen")
    else:
        tot_points = []
        for spelare in alla_spelare:
            if spelare in players:
                placering = tab6.number_input("Vilken placering fick {:}?".format(spelare), 1, int(num_players), "min", 1, key='placering{:}'.format(spelare))
                placering = str(placering)
                points = df_points_major.loc[int(num_players), placering]
                points = float(points)
                tidigare_points = df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Poäng']
                tidigare_points = float(tidigare_points)
                ny_points = tidigare_points+points
                tidigare_comps = df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal spelade tävlingar']
                tidigare_comps = int(tidigare_comps)
                ny_comps = tidigare_comps + 1
                df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Poäng'] = ny_points
                df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal spelade tävlingar'] = ny_comps
                if placering == num_players_str:
                    tidigare_loss = df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal förluster'] 
                    ny_loss = int(tidigare_loss) + 1
                    df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal förluster'] = ny_loss
                if placering == '1':
                    tidigare_wins = df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal vinster'] 
                    ny_wins = int(tidigare_wins) + 1
                    df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Antal vinster'] = ny_wins

                info = [spelare, ny_points, comp]
                df_to_plot.loc[len(df_to_plot)] = info

            else:   
                tidigare_points = df_leaderboard.loc[df_leaderboard['Spelarnamn'] == spelare, 'Poäng']
                tidigare_points = float(tidigare_points)
                info = [spelare, tidigare_points, comp]
                df_to_plot.loc[len(df_to_plot)] = info

        time.sleep(10)
        tab6.subheader("Uppdaterad Leaderboard:")
        tab6.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal spelade tävlingar', 'Poäng']].sort_values('Poäng', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})
        
        tab6.divider()
   
        def clear_box():
            global df_leaderboard
            global df_plotdata
            global df_to_plot
            df_plotdata = pd.concat([df_plotdata, df_to_plot], axis=0)
            worksheet = sh.add_worksheet(title=comp, rows=100, cols=20)
            worksheet.update([df_leaderboard.columns.values.tolist()] + df_leaderboard.values.tolist())
            # worksheet_plot = sh.add_worksheet(title='test', rows=100, cols=20)
            worksheet_plot = sh.worksheet('Leaderboard Utveckling')
            worksheet_plot.clear()
            worksheet_plot.update([df_plotdata.columns.values.tolist()] + df_plotdata.values.tolist())
            tab6.write("Leaderboard uppdaterad")

            st.session_state['tävling'] = ""
            st.session_state['antal'] = ""
            st.session_state['spelare'] = " "
            st.session_state['major'] = ""
        upd = tab6.button("Uppdatera Leaderboard", type='primary', on_click=clear_box)

else:
    tab6.empty()


# Allas golf-id
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
