from flask import Flask, render_template, jsonify, request
import markdown2
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Function to fetch URL preview data
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

# Function to embed URL previews into Markdown content
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
    # Read the Markdown file and embed URL previews
    markdown_file = "docker_session_1.md"
    with open(markdown_file, 'r') as file:
        markdown_content = file.read()
    
    html_content = embed_url_preview(markdown_content)
    
    # Convert Markdown to HTML
    html_content = markdown2.markdown(html_content, extras=["tables", "code-friendly", "fenced-code-blocks", "metadata", "latex", "footnotes", "smarty-pants", "strike", "tag-friendly", "xml"])

    # soup = BeautifulSoup(html_content, 'html.parser')
    # tables = soup.find_all('table')
    # formatted_tables = [str(table) for table in tables]
    # html_content = "\n".join(formatted_tables)
    
    # Render the HTML content
    return render_template('index.html', content=html_content)

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
    html_content = """
        - Example:
    - **Run MySQL Container**: Start the MySQL container with a name `mysql-container`, exposing port 3306:
        
        ```bash
        docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=password -d mysql:latest
        ```
        
    - **Create a .NET Core Application**: Assume you have a .NET Core application that needs to connect to the MySQL database. Build the .NET Core application and create a Docker image for it. Here's a simple Dockerfile assuming the application is published to a folder named `app`:
        
        ```
        FROM mcr.microsoft.com/dotnet/core/runtime:latest
        WORKDIR /app 
        COPY ./app .
        ENTRYPOINT ["dotnet", "YourApp.dll"]
        ```
        
    - **Run .NET Core Application Container Linked to MySQL**: Now, run the .NET Core application container, linking it to the MySQL container:
        
        ```bash
        docker run --name dotnet-app --link mysql-container:mysql -d your-dotnet-image:latest
        ```
        
    
    In this example:
    
    - `-name mysql-container` assigns the name `mysql-container` to the MySQL container.
    - `e MYSQL_ROOT_PASSWORD=password` sets the root password for MySQL.
    - `-name dotnet-app` assigns the name `dotnet-app` to the .NET Core application container.
    - `-link mysql-container:mysql` links the .NET Core application container to the MySQL container with an alias `mysql`.
    - `d` runs both containers in detached mode.
    
    Inside the .NET Core application container, you can now access the MySQL database using the hostname `mysql` and the exposed port. Make sure your .NET Core application is configured to connect to MySQL using the correct hostname and port.
    
    """
    return render_template('index.html', content=html_content)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
