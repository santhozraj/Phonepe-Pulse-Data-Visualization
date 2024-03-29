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

# sql connection for Transaction Amount And Count visualization Part:
    
    # Transaction Amount visualization

def top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Santhozraj",
                            database="phonepe_data",
                            port="5432")
    cursor=mydb.cursor()

    # Desc_Amount_Plot_1
    query1=f'''SELECT states,SUM(transaction_amount) AS transaction_amount
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_amount DESC
            LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states","transaction_amount"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1,x="states",y="transaction_amount",title="TOP 10 TRANSACTION AMOUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount_1)


    # Asce_Amount_Plot_2 
    query2=f'''SELECT states,SUM(transaction_amount) AS transaction_amount
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_amount 
            LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states","transaction_amount"))
    with col2:
        fig_amount_2=px.bar(df_2,x="states",y="transaction_amount",title="LAST 10 OF TRANSACTION AMOUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)


    # Avg_Amount_Plot_3 
    query3=f'''SELECT states,AVG(transaction_amount) AS transaction_amount
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states","transaction_amount"))

    fig_amount_3=px.bar(df_3,x="transaction_amount",y="states",title="AVERAGE OF TRANSACTION AMOUNT",hover_name="states",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=800,width=1000)
    st.plotly_chart(fig_amount_3)

 # Transaction Count visualization:

def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Santhozraj",
                            database="phonepe_data",
                            port="5432")
    cursor=mydb.cursor()

    # Desc_Count_Plot_1
    query1=f'''SELECT states,SUM(transaction_count) AS transaction_count
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_count DESC
            LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()
    df_1=pd.DataFrame(table_1, columns=("states","transaction_count"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df_1,x="states",y="transaction_count",title="TOP 10 TRANSACTION COUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount)


    # Asce_Count_Plot_2 
    query2=f'''SELECT states,SUM(transaction_count) AS transaction_count
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_count 
            LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states","transaction_count"))
    with col2:
        fig_amount_2=px.bar(df_2,x="states",y="transaction_count",title="LAST 10 TRANSACTION COUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)

    # Avg_count_Plot_3 
    query3=f'''SELECT states,AVG(transaction_count) AS transaction_count
            FROM {table_name}
            GROUP BY states
            ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states","transaction_count"))

    fig_amount_3=px.bar(df_3,x="transaction_count",y="states",title="AVERAGE OF TRANSACTION COUNT",hover_name="states",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=800,width=1000)
    st.plotly_chart(fig_amount_3)


# Map User
# sql connection for registeredusers visualization Part:

def top_chart_registered_users(table_name,state):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Santhozraj",
                            database="phonepe_data",
                            port="5432")
    cursor=mydb.cursor()

    # Desc_RegisteredUser_Plot_1
    query1=f'''SELECT districts, SUM (registeredusers) as registeredusers
               FROM {table_name}
               WHERE states='{state}'
               GROUP BY districts
               ORDER BY registeredusers DESC
               LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts","registeredusers"))

    col1,col2=st.columns(2)
    with col1:
        fig_reguser=px.bar(df_1,x="districts",y="registeredusers",title="TOP 10 REGISTERED USERS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_reguser)


    # Asce_RegisteredUser_Plot_2 
    query2=f'''SELECT districts, SUM (registeredusers) as registeredusers
               FROM {table_name}
               WHERE states='{state}'
               GROUP BY districts
               ORDER BY registeredusers
               LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts","registeredusers"))
    with col2:
        fig_reguser_1=px.bar(df_2,x="districts",y="registeredusers",title="LAST 10 REGISTERED USERS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_reguser_1)


    # Avg_RegisteredUser_Plot_3 
    query3=f'''SELECT districts, AVG (registeredusers) as registeredusers
               FROM {table_name}
               WHERE states='{state}'
               GROUP BY districts
               ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts","registeredusers"))

    fig_reguser_2=px.bar(df_3,x="registeredusers",y="districts",title="AVERAGE OF REGISTERED USERS",hover_name="districts",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=850,width=1000)
    st.plotly_chart(fig_reguser_2)

# sql connection for appopens visualization Part:

def top_chart_appopens(table_name,state):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Santhozraj",
                            database="phonepe_data",
                            port="5432")
    cursor=mydb.cursor()

    # Desc_AppOpens_Plot_1
    query1=f'''SELECT districts, SUM (appopens) as appopens
               FROM {table_name}
               WHERE states='{state}'
               GROUP BY districts
               ORDER BY appopens DESC
               LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts","appopens"))

    col1,col2=st.columns(2)
    with col1:
        fig_appopens=px.bar(df_1,x="districts",y="appopens",title="TOP 10 APPOPENS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_appopens)


    # Asce_AppOpens_Plot_2 
    query2=f'''SELECT districts, SUM (appopens) as appopens
               FROM {table_name}
               WHERE states='{state}'
               GROUP BY districts
               ORDER BY appopens
               LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts","appopens"))

    with col2:
        fig_appopens_1=px.bar(df_2,x="districts",y="appopens",title="LAST 10 APPOPENS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_appopens_1)


    # Avg_AppOpens_Plot_3 
    query3=f'''SELECT districts, AVG (appopens) as appopens
               FROM {table_name}
               WHERE states='{state}'
               GROUP BY districts
               ORDER BY appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts","appopens"))

    fig_appopens_2=px.bar(df_3,x="appopens",y="districts",title="AVERAGE OF APPOPENS",hover_name="districts",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=850,width=1000)
    st.plotly_chart(fig_appopens_2)

# Top User
# sql connection for Of registerusers visualization Part:

def top_chart_register_users(table_name):
    mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Santhozraj",
                            database="phonepe_data",
                            port="5432")
    cursor=mydb.cursor()

    # Desc_RegisterUsers_Plot_1
    query1=f'''SELECT states,SUM(registerusers) AS registerusers
               FROM {table_name}
               GROUP BY states
               ORDER BY registerusers DESC
               LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states","registerusers"))

    col1,col2=st.columns(2)
    with col1:
        fig_regusers=px.bar(df_1,x="states",y="registerusers",title="TOP 10 REGISTER USERS",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_regusers)


    # Asce_RegisterUsers_Plot_2 
    query2=f'''SELECT states,SUM(registerusers) AS registerusers
               FROM {table_name}
               GROUP BY states
               ORDER BY registerusers 
               LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states","registerusers"))
    with col2:
        fig_regusers_1=px.bar(df_2,x="states",y="registerusers",title="LAST 10 REGISTER USERS",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_regusers_1)


    # Avg_RegisterUsers_Plot_3 
    query3=f'''SELECT states,AVG(registerusers) AS registerusers
               FROM {table_name}
               GROUP BY states
               ORDER BY registerusers;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states","registerusers"))

    fig_regusers_2=px.bar(df_3,x="registerusers",y="states",title="AVERAGE OF REGISTER USERS",hover_name="states",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=850,width=1000)
    st.plotly_chart(fig_regusers_2)


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
    
    Question=st.selectbox("Select The Question", ["1. Transactionn Amount and Count Of Aggregated Insurance","2. Transactionn Amount and Count Of Map Insurance",
                                                  "3. Transactionn Amount and Count Of Top Insurance","4. Transactionn Amount and Count Of Aggregated Transaction",
                                                  "5. Transactionn Amount and Count Of Map Transaction","6. Transactionn Amount and Count Of Top Transaction",
                                                  "7. Transactionn Count Of Aggregated User","8. Registered Users Of Map User",
                                                  "9. App Opens Of Map User","10. Register Users Of Top User"])                                          
    
    if Question == "1. Transactionn Amount and Count Of Aggregated Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif Question == "2. Transactionn Amount and Count Of Map Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif Question == "3. Transactionn Amount and Count Of Top Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif Question == "4. Transactionn Amount and Count Of Aggregated Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif Question == "5. Transactionn Amount and Count Of Map Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif Question == "6. Transactionn Amount and Count Of Top Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif Question == "7. Transactionn Count Of Aggregated User":
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif Question == "8. Registered Users Of Map User":

        states=st.selectbox("Select The State",map_user["States"].unique()) 
        st.subheader("REGISTERED USER")
        top_chart_registered_users("map_user",states)

    elif Question == "9. App Opens Of Map User":

        states=st.selectbox("Select The State",map_user["States"].unique()) 
        st.subheader("APPOPENS")
        top_chart_appopens("map_user",states) 

    elif Question == "10. Register Users Of Top User":

        st.subheader("REGISTER USERS")
        top_chart_register_users("top_user")   