FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . ./
RUN mkdir -p /app/public
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=8080

RUN mkdir -p /app/public

COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public* ./public/
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 8080

CMD ["npm", "start", "--", "-p", "8080"]
