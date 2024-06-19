import google.generativeai as genai
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')

def generate_search_link(query):
    base_url = "https://www.google.com/search?q="
    query_params = query.replace(" ", "+")
    search_link = base_url + query_params
    return search_link

def get_search_results(search_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(search_link, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    result_divs = soup.find_all('div', class_='tF2Cxc')
    links = []
    for result_div in result_divs:
        link = result_div.find('a')['href']
        links.append(link)
    return links

def get_links(query, number):
    user_query = query
    search_link = generate_search_link(user_query)
    try:
        search_results = get_search_results(search_link)
        if search_results:
            final_links = []
            for i, link in enumerate(search_results[:number], start=1):
                final_links.append(f"Search result {i}: {link}")
            return final_links
        else:
            return "404 error"
    except:
        return "BOT SERVER PROBLEM"

def get_response(question):
    if question.lower() == "what is your name":
        return "My full name is Lucifer, but you can call me pro for short. How can I help you?"
    else:
        try:        
            key = api_key
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(question)
            gemini = response.text
            rewrite = gemini.replace("*", "")
            links = get_links(question, 2)
            final_ans = f"{rewrite}\n" + "\n".join(links)
            return final_ans
        except:
            value = get_links(question, 5)
            return f"Search result: {value}"
