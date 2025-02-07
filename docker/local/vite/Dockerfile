FROM node:22-bookworm-slim

RUN apt-get update && apt-get install -y git

WORKDIR /app

ENV NODE_ENV dev

# Install node modules
COPY package.json package-lock.json ./

RUN npm ci

ENV PATH ./node_modules/.bin/:$PATH

# Note: vite.config.js and src code will be mounted via volumes
