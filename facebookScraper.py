import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Query
import psycopg2

app = FastAPI()

# PostgreSQL connection config
conn = psycopg2.connect(
        host="db",
        database="facebook",
        user="user",
        password="password"
    )

cur = conn.cursor()

    # SQL statement to create the table
create_table_query = '''
    CREATE TABLE IF NOT EXISTS facebook_data (
        id SERIAL PRIMARY KEY,
        page_title TEXT,
        description TEXT,
        image_url TEXT,
        likes TEXT,
        followers TEXT,
        category TEXT,
        website TEXT,
        phone_number TEXT,
        email TEXT,
        address TEXT
    )
    '''

    # Execute the CREATE TABLE statement
cur.execute(create_table_query)

    # Commit the transaction
conn.commit()

    # Close the cursor and connection


@app.get("/data")
def get_data(url: str = Query(..., description="facebook page url")):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    page_title = soup.find('title').text.strip()

    description = soup.find('meta', property='og:description')
    description_content = description['content'] if description else None

    image_url = soup.find('meta', property='og:image')
    image_url_content = image_url['content'] if image_url else None

    likes = soup.find('div', class_='_4-u3 _5sqi _5sqk')
    likes_count = likes.find('span').text.strip() if likes else None

    followers = soup.find('div', class_='_4bl7')
    followers_count = followers.find('span').text.strip() if followers else None

    category = soup.find('div', class_='_4bl9')
    category_name = category.find('a').text.strip() if category else None

    website = soup.find('div', class_='_4bl9')
    website_url = website.find('a')['href'] if website else None

    phone = soup.find('div', class_='_2iem')
    phone_number = phone.find('a')['href'].replace('tel:', '') if phone else None

    email = soup.find('div', class_='_2iep')
    email_address = email.find('a')['href'].replace('mailto:', '') if email else None

    address = soup.find('div', class_='_2iem _50f7')
    address_text = address.find('div', class_='_50f4').text.strip() if address else None

    response = {
        "page_title":page_title,
        "description_content":description_content,
        "image_url_content":image_url_content,
        "likes_count":likes_count,
        "followers_count":followers_count,
        "category_name":category_name,
        "website_url":website_url,
        "phone_number":phone_number,
        "email_address":email_address,
        "address_text":address_text
    }

    data = (
        page_title,
        description_content,
        image_url_content,
        likes_count,
        followers_count,
        category_name,
        website_url,
        phone_number,
        email_address,
        address_text
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO facebook_data (page_title, description, image_url, likes, followers, category, website, phone_number, email, address) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        data
    )
    conn.commit()
    cur.close()
    conn.close()

    return data;