from bs4 import BeautifulSoup
import numpy as np
import requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cuda')

def get_links(current_link):
    html = requests.get(current_link)
    soup = BeautifulSoup(html.content, features='html.parser')
    links = soup.find_all('a')

    possible_pages = []

    for link in links:
        title = link.get('title')
        href = link.get('href')

        if title is None:
            continue

        if href.startswith('http'):
            continue

        possible_pages.append((title, href))

    return possible_pages

def calculate_similarity(a, b):
    dot_product = np.dot(a, b)
    normA = np.linalg.norm(a)
    normB = np.linalg.norm(b)
    sim = dot_product / (normA * normB);
    return sim

def get_next_page(current_link, target_href, target_embedding, visited):
    possible_pages = get_links(current_link)

    most_similar = float('-inf')
    best_link = ""
    best_title = ""

    titles = [title for title, _ in possible_pages]
    embeddings = model.encode(titles)

    for (title, link), embedding in zip(possible_pages, embeddings):
        if link == target_href:
            return title, link

        if title in visited:
            continue

        sim = calculate_similarity(target_embedding, embedding)
        if sim > most_similar:
            most_similar = sim
            best_link = link
            best_title = title
    
    return best_title, best_link

def speedrun(start_url, end_url):
    start_html = requests.get(start_url).content
    end_html = requests.get(end_url).content
    
    start_soup = BeautifulSoup(start_html, features='html.parser')
    end_soup = BeautifulSoup(end_html, features='html.parser')

    start_title = start_soup.find('h1').get_text()
    end_title = end_soup.find('h1').get_text()

    print("starting at:", start_title)
    print("trying to find:", end_title)

    target_embedding = model.encode(end_title)

    visited = []
    title, link = get_next_page(start_url, end_url, target_embedding, visited)
    visited.append(title)
    
    distance = 1
    
    while True:
        print("At:", title, link)

        if title == end_title:
            print("finished in", distance, "moves")
            break

        title, link = get_next_page(f'https://en.wikipedia.org/{link}', end_url, target_embedding, visited)
        visited.append(title)
        distance += 1


# speedrun("https://en.wikipedia.org/wiki/Dune_(novel)", "https://en.wikipedia.org/wiki/Barbie_(film)")

start = input('input starting url: ')
end = input('input ending url: ')

speedrun(start, end)
