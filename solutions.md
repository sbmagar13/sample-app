**Task 1**

*Run a container with the `nginx:1.14-alpine` image and name it `webapp`.*

```bash
docker run -p 4000:80 --name webapp -d nginx:1.14-alpine
```

**Task 3**

*Run a container named `shrawan-app` using image `sbmagar/bloggingapp` and set the environment variable `APP_COLOR` to `green`. Make the application available on port `75666` on the host. The application listens on port `5000`.*

- Solution:
```
docker run -d \
--name shrawan-app \
-p 75666:5000 \
-e APP_COLOR=green \
sbmagar/bloggingapp
```