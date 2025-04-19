import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup


exchange_rate = 105  


def scrape_books():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles, prices, ratings = [], [], []

    books = soup.select('article.product_pod')
    for book in books:
        title = book.h3.a['title']
        price = book.select_one('p.price_color').text
        rating_class = book.select_one('p.star-rating')['class'][1]

        titles.append(title)
        prices.append(price)
        ratings.append(rating_class)

    df = pd.DataFrame({
        'Title': titles,
        'Price': prices,
        'Rating': ratings
    })

    df['Price'] = df['Price'].str.replace('Â', '').str.replace('£', '').astype(float)
    df['Price_INR'] = (df['Price'] * exchange_rate).round(2)

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['Rating_Num'] = df['Rating'].map(rating_map)

    return df

# Streamlit dashboard design
st.set_page_config(page_title="📚 Book Dashboard", layout="wide")
st.title("📖 Bookstore Analytics Dashboard")
st.markdown("Live scraped data from [Books to Scrape](http://books.toscrape.com)")

# Load Data
df = scrape_books()

#  KPI Summary
avg_price_inr = round(df['Price_INR'].mean(), 2)
highest_price_inr = df['Price_INR'].max()
total_books = len(df)

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("📚 Total Books", total_books)
kpi2.metric("💰 Avg. Price (INR)", f"₹{avg_price_inr}")
kpi3.metric("💎 Highest Price (INR)", f"₹{highest_price_inr}")

# ⬇ CSV Download
st.download_button(
    label="📥 Download CSV",
    data=df.to_csv(index=False),
    file_name='books.csv',
    mime='text/csv'
)

#  Visualizations of data
fig1 = px.bar(df.sort_values(by='Price_INR', ascending=False).head(10),
              x='Title', y='Price_INR', color='Price_INR',
              title='💸 Top 10 Most Expensive Books (₹ INR)',
              labels={'Price_INR': 'Price (₹)'})

fig2 = px.pie(df, names='Rating',
              title='📚 Rating Distribution of Books')

fig3 = px.scatter(df, x='Rating_Num', y='Price',
                  hover_data=['Title'], color='Rating',
                  title='⭐ Price vs Rating',
                  labels={'Rating_Num': 'Star Rating (Numeric)'})

#  3-column chart layout
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
with col3:
    st.plotly_chart(fig3, use_container_width=True)

#  Footer
st.markdown("---")
st.markdown("👩‍💻 Built by Diya Dave • Data Science Intern • #WebScraping #Dashboard #Streamlit")



# Note: The emojis used in the code are for illustrative purposes. You can replace them with any other emojis you prefer.
#emoji you also can get from https://getemoji.com/ this is a free website to get emojis you can add in to your code mke it more intresting !!!!
