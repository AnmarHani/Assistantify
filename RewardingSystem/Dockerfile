FROM node:20-bullseye-slim as base

RUN apt-get update && \
    apt-get install --no-install-recommends --fix-missing -y \
        build-essential \
        xdg-utils \
        python3 && \
    rm -fr /var/lib/apt/lists/* && \
    rm -rf /etc/apt/sources.list.d/*

RUN npm install --global --quiet npm truffle ganache

# FROM base as truffle

# RUN mkdir -p /home/app
# WORKDIR /home/app

# COPY package.json /home/app
# COPY package-lock.json /home/app

# RUN npm install --quiet

# COPY truffle-config.js /home/app
# COPY contracts /home/app/contracts
# COPY migrations /home/app/migrations/
# COPY test /home/app/test/

# # CMD ["truffle", "version"]
# CMD ["tail", "-f", "/dev/null"]

FROM base as ganache

RUN mkdir -p /home
WORKDIR /home
EXPOSE 8545

ENTRYPOINT ["ganache", "--host=0.0.0.0"]

# TO UPDATE THE IMAGE
# docker build . --platform linux/amd64 -t atn_reward_system
# docker tag atn_reward_system anmarhani/atn_reward_system
# docker push anmarhani/atn_reward_system 

