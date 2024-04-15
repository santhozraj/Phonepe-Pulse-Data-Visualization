#Import the necessary libraries
import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image


# DataFrame Creation

#sql connection

mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Santhozraj",
                        database="phonepe_data",
                        port="5432")
cursor=mydb.cursor()

#aggre_insurance_DF

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))


#aggre_transaction_DF

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggre_user_DF

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))

#map_insurance_DF

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_transaction_DF

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_user_DF

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts","RegisteredUsers","AppOpens"))

#top_insurance_DF

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_transaction_DF

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_user_DF

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes","RegisterUsers"))



def Transaction_amount_count_Y(df, year):

    TACY=df[df["Years"]==year]
    TACY.reset_index(drop=True,inplace=True)

    TACYG=TACY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TACYG.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount=px.bar(TACYG,x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(TACYG,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_count)


    col1,col2=st.columns(2)

    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(TACYG,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_amount"].min(),TACYG["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=650,width=600 )
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(TACYG,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_count"].min(),TACYG["Transaction_count"].max()),
                                hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=650,width=600 )
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return TACY


def Transaction_amount_count_Y_Q(df, quarter):
    TACY=df[df["Quarter"]==quarter]
    TACY.reset_index(drop=True,inplace=True)

    TACYG=TACY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TACYG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(TACYG,x="States",y="Transaction_amount",title=f"{TACY['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(TACYG,x="States",y="Transaction_count",title=f"{TACY['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(TACYG,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_amount"].min(),TACYG["Transaction_amount"].max()),
                                hover_name="States",title=f"{TACY['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
                                height=650,width=600 )
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(TACYG,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_count"].min(),TACYG["Transaction_count"].max()),
                                hover_name="States",title=f"{TACY['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
                                height=650,width=600 )
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return TACY


def Aggre_Tran_Transaction_type(df,state):
    TACY=df[df["States"]==state]
    TACY.reset_index(drop=True,inplace=True)

    TACYG=TACY.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    TACYG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame=TACYG,names="Transaction_type",values="Transaction_amount",width=600,title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.5 )

        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2=px.pie(data_frame=TACYG,names="Transaction_type",values="Transaction_count",width=600,title=f"{state.upper()} TRANSACTION COUNT",hole=0.5 )

        st.plotly_chart(fig_pie_2)


def Aggre_user_plot_1(df,year):
    AGUY=df[df["Years"]==year]
    AGUY.reset_index(drop=True,inplace=True)

    AGUYG=pd.DataFrame (AGUY.groupby("Brands")["Transaction_count"].sum())
    AGUYG.reset_index(inplace=True)


    fig_bar_1=px.bar(AGUYG,x="Brands",y="Transaction_count",title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.Agsunset_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return AGUY

def Aggre_user_plot_2(df,quarter): 

    AGUYQ=df[df["Quarter"]==quarter]
    AGUYQ.reset_index(drop=True,inplace=True)   

    AGUYQG=pd.DataFrame(AGUYQ.groupby("Brands")["Transaction_count"].sum())
    AGUYQG.reset_index(inplace=True)

    fig_bar_2=px.bar(AGUYQG,x="Brands",y="Transaction_count",title=f"{quarter} QUARTER,BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.Agsunset_r,hover_name="Brands")
    st.plotly_chart(fig_bar_2)

    return AGUYQ

def Aggre_user_plot_3(df,state):
    AGUYQS=df[df["States"]==state]
    AGUYQS.reset_index(drop=True,inplace=True)

    fig_line_1=px.line(AGUYQS,x="Brands",y="Transaction_count",hover_data="Percentage",
                    title=f"{state.upper()}  BRANDS, TRANSACTION COUNT, PERCENTAGE",width=1000,markers=True)
    st.plotly_chart(fig_line_1)

# Map_Insurance_Districts

def Map_insur_Districts(df,state):
    TACY=df[df["States"]==state]
    TACY.reset_index(drop=True,inplace=True)

    TACYG=TACY.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    TACYG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_bar_1=px.bar(TACYG,x="Transaction_amount",y="Districts",orientation="h",title=f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT",height=600,
                        color_discrete_sequence=px.colors.sequential.Cividis)

        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2=px.bar(TACYG,x="Transaction_count",y="Districts",orientation="h",title=f"{state.upper()} DISTRICTS AND TRANSACTION COUNT",height=600,
                        color_discrete_sequence=px.colors.sequential.GnBu_r)

        st.plotly_chart(fig_bar_2 )   


# Map_User_Plot_1
        
def map_user_plot_1(df,year):
    MUY=df[df["Years"]==year]
    MUY.reset_index(drop=True,inplace=True)
    MUYG=MUY.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    MUYG.reset_index(inplace=True)

    fig_line_1=px.line(MUYG,x="States",y=["RegisteredUsers","AppOpens"],
                    title=f"{year} REGISTERED USERS, APPOPENS",width=1000, height=800,markers=True)
    st.plotly_chart(fig_line_1)

    return MUY

# Map_User_Plot_2

def map_user_plot_2(df,quarter):
    MUYQ=df[df["Quarter"]==quarter]
    MUYQ.reset_index(drop=True,inplace=True)
    MUYQG=MUYQ.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    MUYQG.reset_index(inplace=True)

    fig_line_1=px.line(MUYQG,x="States",y=["RegisteredUsers","AppOpens"],
                    title=f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USERS, APPOPENS",width=1000, height=800,markers=True,
                    color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return MUYQ


# Map_User_Plot_3

def map_user_plot_3(df,States):
    MUYQS=df[df["States"]==States]
    MUYQS.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_map_user_bar_1=px.bar(MUYQS,x="RegisteredUsers",y="Districts",orientation="h",
                                title=f"{States.upper()} REGISTERED USER",height=800,color_discrete_sequence=px.colors.sequential.Bluyl)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:

        fig_map_user_bar_2=px.bar(MUYQS,x="AppOpens",y="Districts",orientation="h",
                                title=f"{States.upper()} APPOPENS",height=800,color_discrete_sequence=px.colors.sequential.Jet)
        st.plotly_chart(fig_map_user_bar_2)

# top_insurance_plot_1
        
def top_insurance_plot_1(df,states):
    TIY=df[df["States"]==states]
    TIY.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_top_insur_bar_1=px.bar(TIY,x="Quarter",y="Transaction_amount",hover_data="Pincodes",
                                    title=" TRANSACTION AMOUNT",height=650,width=650,color_discrete_sequence=px.colors.sequential.BuGn_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:
        fig_top_insur_bar_2=px.bar(TIY,x="Quarter",y="Transaction_count",hover_data="Pincodes",
                            title=" TRANSACTION COUNT",height=650,width=650,color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)


def top_user_plot_1(df,year):
    TUY=df[df["Years"]==year]
    TUY.reset_index(drop=True,inplace=True)

    TUYG=pd.DataFrame (TUY.groupby(["States","Quarter"])["RegisterUsers"].sum())
    TUYG.reset_index(inplace=True)
    fig_top_user_plot_1=px.bar(TUYG,x="States",y="RegisterUsers",color="Quarter",width=1000,height=800,
                            color_discrete_sequence=px.colors.sequential.Brwnyl_r,hover_name="States",title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_user_plot_1)

    return TUY



def top_user_plot_2(df,state):
    TUYS=df[df["States"]==state]
    TUYS.reset_index(drop=True,inplace=True)

    fig_top_user_plot_2=px.bar(TUYS,x="Quarter",y="RegisterUsers",title="REGISTER USERS, PINCODES, QUARTER",
                            width=1000,height=800,color="RegisterUsers",hover_data="Pincodes",
                            color_continuous_scale=px.colors.sequential.Magenta)

    st.plotly_chart(fig_top_user_plot_2)

# top_chart part

def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence=['blue'])
    return st.plotly_chart(fig_sa)

def ques6():
    sa= map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence=['blue'])
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)

### Streamlit Application Code ###

st.set_page_config(layout="wide")
st.title(":violet[Phonepe Pulse Data Analysis]")


with st.sidebar:

        select = option_menu(
        menu_title=None,
        options=["Home", "Data Exploration", "Top Charts"],
        icons=["house", "bar-chart", "geo"],
        menu_icon="cast",
        default_index=0,
    )

def setting_bg():
   
   st.markdown(f""" <style>.stApp {{
                        background:url("https://wallpapers.com/images/high/purple-and-black-background-9a0om5bk62fizm2m.webp");
                        background-size:cover}}
                     </style>""", unsafe_allow_html=True)
   
setting_bg()
    

if select =="Home":
    st.write(
        """
        Welcome to Phonepe Pulse, a data visualization and exploration project that provides insights
        into the world of digital transactions in India. This project utilizes data from PhonePe users
        and transactions to uncover trends and patterns in the way people make payments across the country.
        """
    )

    col1,col2= st.columns(2)

    with col1:
        st.video("https://www.phonepe.com/webstatic/6508/videos/page/home-fast-secure-v3.mp4")

    with col2:
        st.header(":blue[PHONEPE]")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown(":blue[To offer every Indian equal opportunity to accelerate their progress by unlocking the flow of money and access to services.]")
        st.write(":red[****FEATURES****]")
        st.write("****Simple, Fast & Secure****")
        st.write("****One app for all things money.****")
        st.write("****Pay whenever you like, wherever you like.****")
        st.write("****Find all your favourite apps on PhonePe Switch.****")
        st.link_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        st.write("     ")
        st.image("https://www.phonepe.com/webstatic/6508/static/bab93065eae063d167f5ea2699093877/c1679/hp-banner-pg.jpg")

elif select == "Data Exploration":

    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map  Analysis","Top Analysis"])

    with tab1:
        method = st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method == "Insurance Analysis":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            TAC_Y= Transaction_amount_count_Y(Aggre_insurance, years)
            
            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select The Quarter",TAC_Y["Quarter"].min(),TAC_Y["Quarter"].max(),TAC_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(TAC_Y, quarters)

        elif method =="Transaction Analysis":

            col1,col2= st.columns(2)

            with col1:

                years= st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select The State",Aggre_tran_tac_Y["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q (Aggre_tran_tac_Y,quarters)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select The State Name",Aggre_tran_tac_Y_Q["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)


        elif method =="User Analysis":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y= Aggre_user_plot_1(Aggre_user,years)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q=Aggre_user_plot_2 (Aggre_user_Y,quarters)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Select The State",Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q,states)

            
    
    with tab2:

        method_2 = st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method_2 == "Map Insurance":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Choose The Year",map_insurance["Years"].min(),map_insurance["Years"].max(),map_insurance["Years"].min())
            Map_insur_tac_Y= Transaction_amount_count_Y(map_insurance, years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Choose The State",Map_insur_tac_Y["States"].unique())

            Map_insur_Districts(Map_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Choose The Quarter",Map_insur_tac_Y["Quarter"].min(),Map_insur_tac_Y["Quarter"].max(),Map_insur_tac_Y["Quarter"].min())
            Map_insur_tac_Y_Q=Transaction_amount_count_Y_Q (Map_insur_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Choose The State",Map_insur_tac_Y_Q["States"].unique())

            Map_insur_Districts(Map_insur_tac_Y_Q,states)


        elif method_2 =="Map Transaction":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Choose The Year",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min())
            Map_tran_tac_Y= Transaction_amount_count_Y(map_transaction, years)

            col1,col2=st.columns(2)

            with col1:
                states=st.selectbox("Choose The State",Map_tran_tac_Y["States"].unique())

            Map_insur_Districts(Map_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Choose The Quarter",Map_tran_tac_Y["Quarter"].min(),Map_tran_tac_Y["Quarter"].max(),Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q=Transaction_amount_count_Y_Q (Map_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Choose The State Name",Map_tran_tac_Y_Q["States"].unique())

            Map_insur_Districts(Map_tran_tac_Y_Q,states)


        elif method_2 =="Map User":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Choose The Year",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min())
            Map_user_Y= map_user_plot_1(map_user, years)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Choose The Quarter",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_Y_Q=map_user_plot_2 (Map_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Choose The State",Map_user_Y_Q["States"].unique())

            map_user_plot_3(Map_user_Y_Q,states)

            

    with tab3:
        method_3 = st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method_3 == "Top Insurance":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Pick The Year",top_insurance["Years"].min(),top_insurance["Years"].max(),top_insurance["Years"].min())
            Top_insur_tac_Y= Transaction_amount_count_Y(top_insurance, years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Pick The State",Top_insur_tac_Y["States"].unique())

            top_insurance_plot_1(Top_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Pick The Quarter",Top_insur_tac_Y["Quarter"].min(),Top_insur_tac_Y["Quarter"].max(),Top_insur_tac_Y["Quarter"].min())
            Top_insur_tac_Y_Q=Transaction_amount_count_Y_Q (Top_insur_tac_Y,quarters)


        elif method_3 =="Top Transaction":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Pick The Year",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min())
            Top_tran_tac_Y= Transaction_amount_count_Y(top_transaction, years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Pick The State",Top_tran_tac_Y["States"].unique())

            top_insurance_plot_1(Top_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Pick The Quarter",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q=Transaction_amount_count_Y_Q (Top_tran_tac_Y,quarters)


        elif method_3 =="Top User":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Pick The Year",top_user["Years"].min(),top_user["Years"].max(),top_user["Years"].min())
            top_user_Y= top_user_plot_1(top_user, years)


            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Pick The State",top_user_Y["States"].unique())

            top_user_plot_2(top_user_Y,states)
            

elif select == "Top Charts":
    
    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()   