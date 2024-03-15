# Stage 1: Build the React application
FROM node:14 as build-stage

# Set the working directory in the container
WORKDIR /app

# Install app dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Bundle app source
COPY . ./

# Build the app
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:stable-alpine as production-stage

# Copy the build output to replace the default nginx contents
COPY --from=build-stage /app/build /usr/share/nginx/html

# Expose port 80 to the outside once the container has launched
EXPOSE 80

# Use the "daemon off;" option to ensure that Nginx stays in the foreground so Docker can track the process properly
CMD ["nginx", "-g", "daemon off;"]
