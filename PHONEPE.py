import streamlit as st
import pymysql 
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sqlalchemy import create_engine
import altair as alt

#streamlit page configure
st.set_page_config(page_title= "Phonepe_PulseExplorer | By DineshKumar",page_icon= "🔯",layout='wide',
    initial_sidebar_state="expanded",menu_items={'About': """# This app is created by Dinesh Kumar!"""})
#-- Connect The MySQL DATABASE--#
myconnection = pymysql.connect(host="127.0.0.1",user="root",passwd="*******",database="PHONE_PE")  # use your MySql password
engine = create_engine('mysql+pymysql://root:*********@localhost/PHONE_PE') # use your MySql password
# steamlit menu bar
selected = option_menu(None, ["HOME","TOPCHARTS","VISUALIZATION"], 
                    icons=["house","graph-up-arrow","bar-chart-line"],
                    default_index=0,
                    orientation="horizontal",
                    styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "2px", "--hover-color": "#0C9BEC"},
                            "icon": {"font-size": "30px"},
                            "container" : {"max-width": "6000px"},
                            "nav-link-selected": {"background-color": "#7616D2"}})
##--------------------------HOME PAGE----------------------##
if selected == "HOME":
    st.header(":violet[Welcome to the PhonePe Pulse Data Visualization and Exploration Tool!]")
    image = Image.open("C:\\Users\\dines\\Downloads\\phonepe1.webp")
    st.image(image,width=1000, use_column_width="never", clamp=False, channels="RGB", output_format="PNG")
    st.markdown("###### Unlock the power of PhonePe Pulse data with our user-friendly tool. Seamlessly explore and visualize insights from PhonePe's rich dataset, brought to life through interactive Streamlit and Plotly visualizations. Simplify data-driven decision-making and gain deeper insights effortlessly.")
    col1,col2 =st.columns(2,gap="large") # define column in seperate the page 
    with col1:
        st.markdown("#### :violet[DOMAIN🌏]:")
        st.markdown("#### FINTECH")
        st.markdown("#### :violet[CONCLUTION🎓]:")
        st.markdown("#### ✅ Comprehensive Data Insights")
        st.markdown("#### ✅ Interactive Visualization")
        st.markdown("#### ✅ Informed Decision-Making")
       
    with col2:
        st.markdown("#### :violet[TECHNOLOGIES USED👨‍💻]:") 
        st.markdown("#### Github🔑--Code Hosting Platform")
        st.markdown("#### Python🐍--Versatile Programming")
        st.markdown("#### MySql🐳--Structured Query Language")
        st.markdown("#### Plotly🍃--Interactive Data Visualization")
        st.markdown("#### Streamlit🍁--UI Creation")

##--------------------------TOPCHARTS PAGE----------------------##

if selected == "TOPCHARTS":
    image = Image.open("C:\\Users\\dines\\Downloads\\phonepe2.png")
    st.image(image,width=1000, use_column_width="never", clamp=False, channels="RGB", output_format="PNG")
    Type = st.sidebar.selectbox("**:violet[TYPES]**", ("TRANSACTION", "USERS"))
    colum1,colum2 = st.columns([1.5,1.5],gap='large')
    #st.image('/Users/joesnowafc/Downloads/ppey.jpeg',width=1200)
    with colum1:
        Year = st.selectbox("**:violet[YEAR]**",('2018','2019','2020','2021','2022','2023'))
    with colum2:
        Quarter = st.selectbox("**:violet[QUARTER]**",('1','2','3','4'))
    ##--------------------------TOPCHARTS TRANSACTION type----------------------##
    if Type == "TRANSACTION":
            col1,col2,col3 = st.columns([3,3,3],gap='large')
            if Year == "2023" and Quarter in ['3','4']:
                st.markdown("#### :violet[Data not found, explore ❗️❗️❗️]")
                st.write("#### :green[The year is ongoing 🏃‍♂️]")
            else:    
                with col1:
                    T_TYPE = pd.read_sql("""SELECT DISTINCT transaction_type, SUM(Transaction_amount) AS total_transaction, SUM(Transaction_count) AS total_count FROM agg_indt WHERE year = %s AND quarter = %s GROUP BY 1 ORDER BY 2 DESC LIMIT 10""",engine,params=(Year, Quarter))
                    t_fig = px.bar(T_TYPE, x='transaction_type', y='total_transaction', color='transaction_type',title='TOP TRANSACTION TYPE VS TRANSACTION AMOUNT',labels={'transaction_type': 'Transaction_Type', 'total_transaction': 'Transaction of Amount'},hover_data=['total_count'])
                    t_fig.update_layout(xaxis_tickangle=-90)
                    st.plotly_chart(t_fig, use_container_width=True)

                with col2:
                    ts=pd.read_sql("select distinct state,sum(Transaction_amount) as total_transaction, sum(Transaction_count) as total_count from map_indt WHERE year = %s AND quarter = %s group by 1 order by 2 desc limit 10",engine,params=(Year, Quarter))
                    tts=px.bar(ts, x='state', y='total_transaction', color='state', title='TOP 10 STATE VS TRANSACTION AMOUNT',labels={'state': 'STATE', 'total_transaction': 'Transaction of Amount'},hover_data=['total_count'])
                    tts.update_layout(xaxis_tickangle=-90)
                    st.plotly_chart(tts,use_container_width=True)
                with col3:            
                    TDT1 =pd.read_sql("""SELECT distinct DISTRICT,SUM(Transaction_count) AS TRANSACTION_COUNT,SUM(Transaction_amount) AS TRANSACTION_AMOUNT FROM MAP_TRANS WHERE year = %s AND quarter = %s GROUP BY 1 ORDER BY 3 DESC LIMIT 10""",engine,params=(Year, Quarter))
                    TTD12=px.bar(TDT1, x='DISTRICT', y='TRANSACTION_AMOUNT', color='DISTRICT', title='TOP 10 DISTICT VS TRANS AMOUNT',labels={'DISTRICT': 'DISTRICT', 'TRANSACTION_AMOUNT': 'Total Amount of Transaction'},hover_data=['TRANSACTION_COUNT'])
                    TTD12.update_layout(xaxis_tickangle=-90)
                    st.plotly_chart(TTD12,use_container_width=True)
    ##--------------------------TOPCHARTS USERS type----------------------##
    if Type == "USERS":
            col1,col2,col3 = st.columns([5,5,5],gap='large')
            if Year == "2023" and Quarter in ['3','4']:
                st.markdown("#### :violet[Data not found, explore ❗️❗️❗️]")
                st.write("#### :green[The year is ongoing 🏃‍♂️]")    
            else:    
                with col1:
                    if Year in ["2022","2023" ]and Quarter in ['2','3','4']:
                        st.markdown("#### :violet[Data not found, explore ❗️❗️❗️]")
                    else:    
                        tm = pd.read_sql("select distinct brand,sum(user_count) as TOTAL_USER FROM agg_indu WHERE year = %s AND quarter = %s GROUP BY 1 order by 2 desc limit 10",engine,params=(Year, Quarter))
                        ttm=px.bar(tm, x='brand', y='TOTAL_USER', color='brand', title='TOP 10 BRAND VS TOTAL USER',labels={'brand': 'BRAND', 'TOTAL_USER': 'TOTAL_USER'})
                        ttm.update_layout(xaxis_tickangle=-90)
                        st.plotly_chart(ttm,use_container_width=True)
                with col2:    
                    TTU = pd.read_sql("select distinct state,sum(RegisteredUsers) as TOTAL_USER FROM map_indu WHERE year = %s AND quarter = %s GROUP BY 1 order by 2 desc limit 10",engine,params=(Year, Quarter))
                    ttm=px.bar(TTU, x='state', y='TOTAL_USER', color='state', title='TOP 10 STATE VS TOTAL USER',labels={'state': 'STATE', 'TOTAL_USER': 'TOTAL_USER'})
                    ttm.update_layout(xaxis_tickangle=-90)
                    st.plotly_chart(ttm,use_container_width=True)
                with col3:
                    tao = pd.read_sql("SELECT distinct DISTRICT,SUM(RegisteredUsers) AS TOTAL_USER,SUM(APPOPENS) AS TOTAL_APPOPENS FROM MAP_USER WHERE year = %s AND quarter = %s  group by 1 ORDER BY 3 DESC limit 10",engine,params=(Year, Quarter))
                    ttao=px.bar(tao, x='DISTRICT', y='TOTAL_APPOPENS', color='DISTRICT', title='TOP 10 DISTRICT VS APP OPEN TIME',labels={'DISTRICT': 'DISTRICT', 'TOTAL_APPOPENS': 'Total AppOpens'},hover_data=['TOTAL_USER'])
                    ttao.update_layout(xaxis_tickangle=-90)
                    st.plotly_chart(ttao,use_container_width=True)
##--------------------------VISUALIZATION PAGE----------------------##
if selected == "VISUALIZATION":
    image = Image.open("C:\\Users\\dines\\Downloads\\phonepe3.png")
    st.image(image,width=1000, use_column_width="never", clamp=False, channels="RGB", output_format="PNG")
    Type = st.sidebar.selectbox("**:violet[TYPES]**", ("TRANSACTION", "USERS"))
    colum1,colum2 = st.columns([1.5,1.5],gap='large')
    with colum1:
        Year = st.selectbox("**:violet[YEAR]**",('2018','2019','2020','2021','2022','2023'))
    with colum2:
        Quarter = st.selectbox("**:violet[QUARTER]**",('1','2','3','4'))
    ##--------------------------VISUALIZATION TRANSACTION TYPE----------------------##
    if Type == "TRANSACTION":
        with st.sidebar:    
            selected = option_menu(None, ["AGG TRANSACTION","MAP TRANSACTION","TOP TRANSACTION"], 
                    icons=["sun","globe","forward"],
                    default_index=0,
                    orientation="vertical",
                    styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "2px", "--hover-color": "#0C9BEC"},
                            "icon": {"font-size": "30px"},
                            "container" : {"max-width": "6000px"},
                            "nav-link-selected": {"background-color": "#7616D2"}})
        if Year == "2023" and Quarter in ['3','4']:
                st.markdown("#### :violet[Data not found, explore ❗️❗️❗️]")
                st.write("#### :green[The year is ongoing 🏃‍♂️]")
        else:
            if selected == "AGG TRANSACTION":
                st.markdown("#### :violet[CHOROPLETH MAP OF TRANSACTION_AMOUNT BY STATE🌏]:")
                df = pd.read_sql("""SELECT distinct STATE,SUM(Transaction_count) AS TRANSACTION_COUNT,SUM(Transaction_amount) AS TRANSACTION_AMOUNT FROM MAP_TRANS WHERE year = %s AND quarter = %s  GROUP BY 1 ORDER BY 1 """,engine,params=(Year, Quarter))
                df2 = pd.read_csv("C:\\Users\\dines\\Downloads\\Untitled Folder\\GITPE\\Statenames.csv")
                df.STATE=df2
                fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson", featureidkey='properties.ST_NM',locations='STATE',color='TRANSACTION_AMOUNT',width=1200,color_continuous_scale='Portland')
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(autosize=False,margin = dict(l=0,r=0,b=0,t=0,pad=4,autoexpand=True),width=1200, height=400,)
                st.plotly_chart(fig,use_container_width=True)
            if selected == "MAP TRANSACTION":
                st.markdown("#### :violet[CHOROPLETH MAP OF TRANSACTION_COUNT BY STATE🌏]:")
                df = pd.read_sql("""SELECT distinct STATE,SUM(Transaction_count) AS TRANSACTION_COUNT,SUM(Transaction_amount) AS TRANSACTION_AMOUNT FROM MAP_TRANS WHERE year = %s AND quarter = %s  GROUP BY 1 ORDER BY 1 """,engine,params=(Year, Quarter))
                df2 = pd.read_csv("C:\\Users\\dines\\Downloads\\Untitled Folder\\GITPE\\Statenames.csv")
                df.STATE=df2
                fig = px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson", featureidkey='properties.ST_NM',locations='STATE',color='TRANSACTION_COUNT',width=1200,color_continuous_scale='Jet')
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(autosize=False,margin = dict(l=0,r=0,b=0,t=0,pad=4,autoexpand=True),width=1200, height=400,)
                st.plotly_chart(fig,use_container_width=True)
            if selected == "TOP TRANSACTION":
                col1,col2 = st.columns([4,5],gap='large')
                with col1:
                    TTU = pd.read_sql("select distinct state,sum(Transaction_amount) as total_transaction, sum(Transaction_count) as total_count from map_indt WHERE year = %s AND quarter = %s group by 1 order by 2 desc limit 10",engine,params=(Year, Quarter))
                    tts1=px.bar(TTU, x='state', y='total_transaction', color='state', title='TOP 10 STATE VS TRANSACTION AMOUNT',labels={'state': 'STATE', 'total_transaction': 'Transaction of Amount'},hover_data=['total_count'])
                    tts1.update_layout(xaxis_tickangle=-90)
                    st.plotly_chart(tts1,use_container_width=True)
                with col2:
                    ttpc = pd.read_sql("""SELECT distinct  STATE,PINCODE,SUM(Transaction_count) AS TRANSACTION_COUNT,SUM(Transaction_amount) AS TRANSACTION_AMOUNT FROM TOP_TRANS WHERE year = %s AND quarter = %s GROUP BY 1,2 ORDER BY 4 DESC LIMIT 10""",engine,params=(Year, Quarter))
                    TDT18=px.bar(ttpc, x='STATE', y='TRANSACTION_AMOUNT', color='PINCODE', title='TOP STATE WITH PINCODE VS TRANS AMOUNT',labels={'STATE': 'STATE', 'TRANSACTION_AMOUNT': 'Total Amount of Transaction'},hover_data=['TRANSACTION_COUNT'])
                    TDT18.update_layout(xaxis_tickangle=-90) 
                    st.plotly_chart(TDT18,use_container_width=True) 
    ##--------------------------VISUALIZATION USERS TYPE----------------------##
    if Type == "USERS":
        with st.sidebar:    
            selected = option_menu(None, ["AGG USERS","MAP USERS","TOP USERS"], 
                    icons=["sun","globe","forward"],
                    default_index=0,
                    orientation="vertical",
                    styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "2px", "--hover-color": "#0C9BEC"},
                            "icon": {"font-size": "30px"},
                            "container" : {"max-width": "6000px"},
                                    "nav-link-selected": {"background-color": "#7616D2"}})
            with st.sidebar:
                selected_state = option_menu(None, ['andhra-pradesh','arunachal-pradesh','assam','bihar',
                            'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                            'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                            'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                            'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                            'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'],styles={"nav-link-selected": {"background-color": "#7616D2"}})
        if selected=="AGG USERS":
            if Year == ["2023","2022"] and Quarter in ['2','3','4']:
                st.markdown("#### :violet[Data not found, explore ❗️❗️❗️]")
                st.write("#### :green[The year is ongoing 🏃‍♂️]") 
            else:    
                ttsub=pd.read_sql("""SELECT distinct STATE,BRAND,SUM(USER_COUNT) AS TOTAL_USER FROM agg_user WHERE year = %s AND quarter = %s and STATE =%s  group by 1,2 ORDER BY 3 desc """,engine,params=(Year, Quarter,selected_state))
                TDT13=px.bar(ttsub, x='BRAND', y='TOTAL_USER', color='BRAND', title='STATE WITH BRAND VS TOTAL USER',labels={'BRAND': 'BRAND', 'TOTAL_USER': 'TOTAL_USER'})
                TDT13.update_layout(xaxis_tickangle=-90)
                st.plotly_chart(TDT13,use_container_width=True)
        if selected == "MAP USERS":
            tsdc = pd.read_sql("""SELECT distinct STATE,DISTRICT,SUM(RegisteredUsers) AS TOTAL_USER,SUM(APPOPENS) AS TOTAL_APPOPENS FROM MAP_USER WHERE year = %s AND quarter = %s and STATE =%s group by 1,2 ORDER BY 3 DESC""",engine,params=(Year, Quarter,selected_state))
            TTD14=px.bar(tsdc, x='DISTRICT', y='TOTAL_USER', color='DISTRICT', title='DISTRICT WISE USER COUNT',labels={'DISTRICT': 'DISTRICT', 'TOTAL_USER': 'TOTAL_USER'},hover_data=['TOTAL_APPOPENS'])
            TTD14.update_layout(xaxis_tickangle=-90)
            st.plotly_chart(TTD14,use_container_width=True)
        if selected == "TOP USERS":
            sptu = pd.read_sql("""SELECT distinct STATE,PINCODE,SUM(RegisteredUsers) AS TOTAL_USER FROM TOP_USER WHERE year = %s AND quarter = %s and STATE =%s group by 1,2 ORDER BY 3 DESC limit 10""",engine,params=(Year, Quarter,selected_state))
            sptu['PINCODE'] = sptu['PINCODE'].astype(str)
            TTD15= alt.Chart(sptu).mark_bar().encode(x=alt.Y('PINCODE:N', title='PINCODE',sort='-y'),y='TOTAL_USER:Q',color='PINCODE:N',tooltip=['STATE', 'PINCODE:N', 'TOTAL_USER:Q']).properties(title='STATE WISE TOP PINCODE USERS').configure_axis(labelAngle=0)
            st.altair_chart(TTD15, use_container_width=True)