import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title('Whatsapp chat analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    # fetching unique users
    userlist = df['User'].unique().tolist()
    userlist.sort()
    userlist.insert(0,"Overall")

    selecteduser = st.sidebar.selectbox("Select user",userlist)
    st.title("Top Statistics")
    if st.sidebar.button("Show Analysis"):
        total,words,media_count,links=helper.fetch(selecteduser,df)

        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(total)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(media_count)
        with col4:
            st.header("Links shared")
            st.title(links)

        if selecteduser == 'Overall':
            st.title("Group analysis")
            st.header("Most busy users")

            x,newdf = helper.busyusers(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                ax.set_xticklabels(x.index, rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(newdf)

        #wordcloud
        st.header("Worldcloud:")
        dfwc=helper.wordcl(selecteduser,df)
        fig,ax=plt.subplots()
        ax.imshow(dfwc)
        st.pyplot(fig)

        #emojis

        emojidf = helper.extract_emojis(selecteduser, df)
        col1,col2= st.columns(2)
        with col1:
            st.header("Emojis used")
            st.dataframe(emojidf)
        with col2:
            st.header("Top 5 emojis")
            fig,ax= plt.subplots()
            ax.pie(emojidf[1].head(),labels=emojidf[0].head())
            st.pyplot(fig)

        #timeline
        st.header("Monthly analysis")
        timelinem = helper.timeline(selecteduser,df)
        fig, ax =plt.subplots()
        ax.plot(timelinem['time'],timelinem['Message'],color='red')
        ax.set_ylabel("Number of messages")
        ax.set_xlabel("Month")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #dailytimeline
        st.header("Weekly analysis")
        daily = helper.dailytimeline(selecteduser,df)


        fig, ax = plt.subplots()
        ax.plot(daily.index.tolist(),daily.values, color='red')
        ax.set_ylabel("Number of messages")
        ax.set_xlabel("Days")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #mostbusymonth
        st.header("Busy months")
        monthbusy = helper.mostbusymonth(selecteduser, df)

        fig, ax = plt.subplots()
        ax.bar(monthbusy.index.tolist(), monthbusy.values, color='green')
        ax.set_ylabel("Number of messages")
        ax.set_xlabel("Month")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #busyhours heatmap
        st.header("Busy hours")
        fig, ax = plt.subplots()
        pivotdf=helper.busyhours(selecteduser,df)
        ax= sns.heatmap(pivotdf,linecolor='white',linewidths=0.2)
        ax.set_ylabel("Days")
        ax.set_xlabel("Time(24-hours)")
        st.pyplot(fig)



