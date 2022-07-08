# pull the official base image
FROM node:alpine
EXPOSE 8888
# set working direction
WORKDIR /app
# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH
# install application dependencies
COPY ./employit/package.json .
COPY ./employit/package-lock.json .
RUN npm i
# add app
COPY ./employit ./
# start app
CMD ["npm", "start"]