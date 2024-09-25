# Svelte Dockerfile
FROM node:21 AS build

WORKDIR /app

COPY ./ui/package*.json ./
RUN npm install

COPY ./ui/ ./
RUN npm run build

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
