# install Streamlit and execute
# > streamlit run streamlit.py

import re
import time
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick

@st.cache
def load_data():
    df = pd.read_csv("data/data.csv", sep="|")
    cols_to_drop = [col for col in df.columns if re.search('visit', col)]
    df.drop(cols_to_drop, axis=1, inplace=True)
    df['day']=pd.to_datetime(df['day'])
    df.set_index(['day'],drop=True, inplace=True)
    df=df.groupby('identifier').resample('W').sum()
    return df.drop('identifier', axis=1).reset_index(0)

res=load_data()

st.title("my Streamlit App")
st.latex(r'''\hat {\boldsymbol {\beta }}=\left(\mathrm {X} ^{\mathsf {T}}\mathrm {X} \right)^{-1}\mathrm {X} ^{\mathsf {T}}\mathbf {y} .''')

if st.button("reload Data"):
    st.caching.clear_cache()

def plot(df,date,identifier,col):
    
    df = df[(df.identifier==identifier)]
    maxi1=round(df[col].max()*1.5)
    
    df=df.loc[df.index[0]:pd.Timestamp(date)]
    fig, (ax1) = plt.subplots(1,figsize=(5,3),dpi=100)
    ax1.plot(df[col],marker='o', linestyle='--', linewidth=2,markersize=3, color='tab:green')

    ax1.set_xlim([START, END])
    ax1.set_ylim([0, maxi1])
    ax1.tick_params(axis='x', labelsize=7)
    ax1.tick_params(axis='y', labelsize=7 , rotation=33)    
    ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))

    plt.title('%s per week for account %s'%(col, identifier), fontsize=11)
    plt.tight_layout()
    return fig

id = list(res.identifier.unique())
option1 = st.selectbox('Account Number', ['?']+id)

if option1=='?':
    st.stop()

st.dataframe(res[(res.identifier==option1)].sort_index(ascending=False))

ts = list(res.columns)
ts.remove('identifier')
option2 = st.selectbox('Feature', ts)

if st.button('Plot'):
    START=res.index[0]
    END=res.index[-1]
    for date in pd.date_range(start = START, end = END,freq = '1W'):
        fig = plot(res, date, option1, option2)
        if date==START:
            empty = st.pyplot(fig)
        else:
            empty.pyplot(fig)
        time.sleep(.005)
    
    st.balloons()