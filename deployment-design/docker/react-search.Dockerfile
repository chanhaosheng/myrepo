FROM node:20-alpine as build

WORKDIR /app

COPY search-ui/package*.json ./

RUN npm install

COPY search-ui/src/ ./src
COPY search-ui/public/ ./public

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]