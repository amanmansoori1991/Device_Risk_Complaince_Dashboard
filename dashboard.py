import pandas as pd
import streamlit as st
import plotly.express as px
import datetime as dt
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client= OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
st.set_page_config(layout='wide')
df = pd.read_csv("FakeDeviceData.csv")
st.title("Device Compliance Dashboard")
col1 , col2 = st.columns(2)
fig1 = px.pie(df, names='Antivirus Status', title='AV Compliance', color ='Antivirus Status', color_discrete_map={'ON': 'seagreen', 'OFF': 'tomato'})
with col1: st.plotly_chart(fig1)
fig2 = px.pie(df, names='Bitlocker Status', title='Bitlocker Complaince', color ='Bitlocker Status', color_discrete_map={'ON': 'seagreen', 'OFF': 'tomato'})
with col2: st.plotly_chart(fig2)
df['Days Since Reboot'] = (pd.Timestamp('today') - pd.to_datetime(df['Last Rebooted'], format='mixed')).dt.days
df['Days Since Patched'] = (pd.Timestamp('today') - pd.to_datetime(df['Last Patched'], format='mixed')).dt.days
def reboot_risk(days): 
    if days<15: return "Low Risk" 
    elif days<30: return "Medium Risk" 
    else: return "High Risk"
df ['Reboot Risk'] = df['Days Since Reboot'].apply(reboot_risk)
def patch_risk(days): 
    if days<30: return "Low Risk" 
    elif days<60: return "Medium Risk" 
    else: return "High Risk"
df ['Patch Risk'] = df['Days Since Patched'].apply(patch_risk)
def get_ai_recommends(av_status, bitlocker_status, patch_risk, reboot_risk): 
    response=client.chat.completions.create(
        model = "gpt-4o-mini", 
        messages= [{"role": "user", "content": f"Device compliance status - AV : {av_status}, Bitlocker :{bitlocker_status}, Patch Risk: {patch_risk}, Reboot Status: {reboot_risk}. What are risk and remediation steps for an enterprise device. Respond concisely not more than 2 lines. "}])
    return response.choices[0].message.content
df['AI Recommendation'] = df.apply(lambda row: get_ai_recommends(
    row['Antivirus Status'],
    row['Bitlocker Status'],
    row['Patch Risk'],
    row['Reboot Risk']
    ), axis=1)
reboot_counts = df['Reboot Risk'].value_counts().reset_index()
patch_counts = df['Patch Risk'].value_counts().reset_index()
col3 , col4 = st.columns(2)
fig3 = px.bar(reboot_counts, x='Reboot Risk', y='count', title='Restart Complaince', color ='Reboot Risk', color_discrete_map={'High Risk': 'tomato', 'Medium Risk': 'orange', 'Low Risk': 'yellowgreen'}, text_auto=True)
fig4 = px.bar(patch_counts, x='Patch Risk', y='count', title='Patch Complaince', color ='Patch Risk', color_discrete_map={'High Risk': 'tomato', 'Medium Risk': 'orange', 'Low Risk': 'seagreen'}, text_auto=True)
with col3: st.plotly_chart(fig3)
with col4: st.plotly_chart(fig4)
st.write(df)
