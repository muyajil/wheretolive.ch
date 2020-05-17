# build environment
FROM node:13.12.0-alpine as build
ARG BACKEND_URL
ENV REACT_APP_BACKEND_URL $BACKEND_URL
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY frontend/package.json ./
COPY frontend/yarn.lock ./
RUN yarn install --silent
ADD frontend ./
RUN yarn build

# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]