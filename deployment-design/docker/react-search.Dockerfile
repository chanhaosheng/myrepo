FROM node:20-alpine as build

WORKDIR /app

COPY search-ui/package*.json ./
COPY search-ui/index.html ./

RUN npm install

COPY search-ui/src/ ./src

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "dev"]