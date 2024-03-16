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

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Add a new configuration file and entrypoint script
COPY ./nginx/default.conf.template /etc/nginx/conf.d/default.conf.template
COPY ./nginx/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set the entrypoint script to be executed
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
