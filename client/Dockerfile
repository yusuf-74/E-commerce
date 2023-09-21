FROM node:latest

WORKDIR /home/client

COPY ./package.json ./

RUN npm cache clean --force
RUN npm install -g npm@latest
RUN npm install --legacy-peer-deps
CMD ["npm" , "start"]