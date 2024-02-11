import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")

DATA_URL = ('Tweets.csv')

@st.cache_data(persist = True)  #The function will not rerun unless the input changes or the app restarts
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    st.write(data.head())
    return data
    
data = load_data()    

st.sidebar.subheader("Sentiment")
random_tweet = st.sidebar.radio("Sentiment", ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of Tweets by Sentiment")
select = st.sidebar.selectbox('Visualise the number of tweets by sentiment', ['Histogram', 'Pie chart'], key = '1')
sentiment_count = data['airline_sentiment'].value_counts() #returns the count of unique values
sentiment_count = pd.DataFrame({
    'Sentiment': sentiment_count.index,
    'Tweets': sentiment_count.values
})
# st.write(sentiment_count.head())

if not st.sidebar.checkbox("Hide",True):
    st.markdown("### Number of Tweets by Sentiment")  
    if select == 'Histogram':
        fig = px.bar(sentiment_count, x = 'Sentiment', y = 'Tweets', color = 'Tweets', height = 500) 
        st.plotly_chart(fig)
    elif select == 'Pie chart':
        fig = px.pie(sentiment_count, values = 'Tweets', names = 'Sentiment')
        st.plotly_chart(fig)

st.sidebar.markdown('When and where are users tweeting from?')
hour = st.sidebar.slider('Hour of the day', 0, 23)
data2 = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Close",True, key='2'):
    st.markdown("### Tweet locations based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(data2), hour, (hour + 1) % 24))
    st.map(data2)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(data2)

st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'))

if len(choice) > 0:
    data3 = data[data['airline'].isin(choice)]
    # fig = px.histogram(data3, x = 'airline', y = 'airline_sentiment', histfunc = 'count', color = 'airline_sentiment', facet_col = 'airline_sentiment', labels = {'airline_sentiment': 'tweets'}, height = 600, width = 800)
    fig = px.histogram(data3, x = 'airline', y = 'airline_sentiment', histfunc = 'count',color = 'airline_sentiment', facet_col= 'airline_sentiment', labels = {'airline_sentiment': 'tweets'}, height= 600, width=800)
    st.plotly_chart(fig)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))

st.set_option('deprecation.showPyplotGlobalUse', False)
if not st.sidebar.checkbox("Close", True, key='3'):
    st.subheader('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords = STOPWORDS, background_color = 'white', height = 640, width = 800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()