from flask import Flask, render_template, jsonify, request
import markdown2
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

def get_url_preview(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').text.strip() if soup.find('title') else ''
        description = soup.find('meta', attrs={'name': 'description'})
        description = description['content'].strip() if description else ''
        image = soup.find('meta', property='og:image')
        image = image['content'].strip() if image else ''
        return {'title': title, 'description': description, 'image': image}
    except Exception as e:
        print(f"Error fetching URL preview for {url}: {e}")
        return None

def embed_url_preview(markdown_content):
    try:
        soup = BeautifulSoup(markdown_content, 'html.parser')
        for link in soup.find_all('a'):
            url = link['href']
            preview_data = get_url_preview(url)
            if preview_data:
                preview_html = f'<div class="link-preview"><h2>{preview_data["title"]}</h2><p>{preview_data["description"]}</p><img src="{preview_data["image"]}"></div>'
                link.replace_with(preview_html)
            else:
                print(f"Failed to embed preview for URL: {url}")
        return str(soup)
    except Exception as e:
        print(f"Error embedding URL previews: {e}")
        return markdown_content

@app.route('/')
def index():
    # app_color = os.getenv('APP_COLOR', 'white')
    app_color = os.getenv('APP_COLOR', '#f8f9fa')
    markdown_file = "docker_session_1.md"
    with open(markdown_file, 'r') as file:
        markdown_content = file.read()
    
    html_content = embed_url_preview(markdown_content)
    
    html_content = markdown2.markdown(html_content, extras=["tables", "fenced-code-blocks"])

    # soup = BeautifulSoup(html_content, 'html.parser')
    # tables = soup.find_all('table')
    # formatted_tables = [str(table) for table in tables]
    # html_content = "\n".join(formatted_tables)
    
    # Render the HTML content
    return render_template('index.html', content=html_content, app_color=app_color)

@app.route('/solutions')
def solutions():
    # app_color = os.getenv('APP_COLOR', 'white')
    app_color = os.getenv('APP_COLOR', '#f8f9fa')
    markdown_file = "solutions.md"
    with open(markdown_file, 'r') as file:
        markdown_content = file.read()
    
    html_content = embed_url_preview(markdown_content)
    
    html_content = markdown2.markdown(html_content, extras=["tables", "fenced-code-blocks"])

    # Render the HTML content
    return render_template('solutions.html', content=html_content, app_color=app_color)

@app.route('/handson')
def handson():
    # app_color = os.getenv('APP_COLOR', 'white')
    app_color = os.getenv('APP_COLOR', '#f8f9fa')
    markdown_file = "handson.md"
    with open(markdown_file, 'r') as file:
        markdown_content = file.read()
    
    html_content = embed_url_preview(markdown_content)
    
    html_content = markdown2.markdown(html_content, extras=["tables", "fenced-code-blocks"])

    # Render the HTML content
    return render_template('handson.html', content=html_content, app_color=app_color)


@app.route('/preview')
def preview():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is missing'}), 400

    preview_data = get_url_preview(url)
    if preview_data:
        return jsonify(preview_data)
    else:
        return jsonify({'error': 'Failed to fetch URL preview'}), 500

@app.route('/posts')
def blogs():
    md_content = """
        - just test
            - testing child content
            - testing **bold** content
    """
    html_content = markdown2.markdown(md_content,["tables", "fenced-code-blocks"])
    return render_template('index.html', content=html_content)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
