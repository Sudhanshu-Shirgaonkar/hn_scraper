import requests
from bs4 import BeautifulSoup
import pprint

BASE_URL = 'https://news.ycombinator.com/news'
MIN_POINTS = 100

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ''

def parse_stories(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('.titleline > a')
    subtexts = soup.select('.subtext')
    stories = []

    for i in range(len(links)):
        title = links[i].get_text()
        href = links[i].get('href')
        vote_tag = subtexts[i].select_one('.score')

        if vote_tag:
            points = int(vote_tag.get_text().replace(' points', ''))
            if points >= MIN_POINTS:
                story = {
                    'title': title,
                    'link': href,
                    'votes': points
                }
                stories.append(story)

    return stories

def sort_stories(stories):
    return sorted(stories, key=lambda s: s['votes'], reverse=True)

def main():
    pages = [BASE_URL, f'{BASE_URL}?p=2']
    all_stories = []

    for page in pages:
        html = fetch_html(page)
        if html:
            stories = parse_stories(html)
            all_stories.extend(stories)

    sorted_stories = sort_stories(all_stories)
    pprint.pprint(sorted_stories)

if __name__ == '__main__':
    main()
