# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Install app dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Bundle app source
COPY frontend/ ./

# Build the app
RUN npm run build

# Serve the app using a static file serving package
FROM nginx:stable-alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
