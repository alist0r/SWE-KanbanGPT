# Step 1: Use Node as the base image
FROM node:20-alpine AS build

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Step 4: Copy the rest of the app and build
COPY . .
RUN npm run build

# Step 5: Use Nginx to serve the built files
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

# Optional: Copy a default nginx config
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
