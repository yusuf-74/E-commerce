FROM node:latest

WORKDIR /home/client

COPY ./package.json ./

RUN npm cache clean --force
RUN npm install --legacy-peer-deps

EXPOSE 3000

CMD ["npm" , "start"]