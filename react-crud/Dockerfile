# Stage 1: Build React app
FROM node:alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve with Express (includes Prometheus metrics)
FROM node:alpine

WORKDIR /app

# Copy only what's needed to run the server and serve static files
COPY --from=build /app/build ./build
COPY server.js ./
COPY package.json package-lock.json ./

# Reinstall just the production dependencies
RUN npm install --only=production

EXPOSE 80

CMD ["node", "server.js"]
