**Task 2**

*Containerize Python/NodeJS application and push the image to Dockerhub.*

**Step 1** - Create Python/NodeJS app. (Clone from GitHub) =>[Python](https://github.com/sbmagar/luckydrawapp-python) OR [NodeJS](https://github.com/sbmagar/luckydrawapp-nodejs)

**Step 2** - Write Dockerfile for the app

**Step 3** - Create image for the app

**Step 4** - Run the container for the app 

**Step 5** - If it works push the image on Dockerhub (optional)


#### Solution(Python App):
- Create **Dockerfile** for your project:
    ```docker
    FROM python:3.8.6-alpine

    WORKDIR /app

    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    EXPOSE 5000

    CMD ["python", "simpleapp.py"]
    ```

- Build image from Dockerfile:
    ```
    docker build -t luckydrawapp-python .
    ```

- Run the container:
    ```
    docker run -d -p 5000:5000 luckydrawapp-python:latest
    ```

- Access from browser [http://localhost:5000](http://localhost:5000)

#### Solution(NodeJS App):
- Create **Dockerfile** for your project:
    ```docker
    FROM node:20-alpine

    WORKDIR /app

    COPY package*.json ./
    RUN npm install

    COPY . .

    EXPOSE 3000

    CMD ["node", "simpleapp.js"]
    ```

- Build image from Dockerfile:
    ```
    docker build -t luckydrawapp-nodejs .
    ```

- Run the container:
    ```
    docker run -d -p 3000:3000 luckydrawapp-nodejs:latest
    ```

- Access from browser [http://localhost:3000](http://localhost:3000)