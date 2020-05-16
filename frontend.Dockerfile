# build environment
FROM node:13.12.0-alpine as build
ARG BACKEND_HOST
ARG BACKEND_PORT
ENV REACT_APP_BACKEND_HOST $BACKEND_HOST
ENV REACT_APP_BACKEND_PORT $BACKEND_PORT
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY frontend/package.json ./
COPY frontend/yarn.lock ./
RUN yarn install --silent
# RUN yarn global add react-scripts@3.4.1 --silent
ADD frontend ./
RUN yarn build

# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]