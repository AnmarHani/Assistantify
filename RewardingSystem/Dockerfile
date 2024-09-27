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

ENTRYPOINT ["ganache", "--host=0.0.0.0", \
    "--wallet.accounts", "0xdad9e921281699147567f2725a3184a01723b180f1647411c2a9e65a65342a90,1000000000000000000000", \
    "--wallet.accounts", "0xa893995244239b9035064065b30a0fe3d25952bcd4760a5eda0ee9cf1209307c,1000000000000000000000", \
    "--wallet.accounts", "0x168c818eb8f7ac1462fe4dee75602b3a3c500ab2c4b9d1e781d70aad4d8dd3ba,1000000000000000000000", \
    "--wallet.accounts", "0x1635353143137545f691a731667fc92e4c9c1e1193fbc238d6bc287f53c4a99b,1000000000000000000000", \
    "--wallet.accounts", "0x25f1a6d047df08245ef845f3cc273264f897eeced95a05554cbdd5e28f56a6f3,1000000000000000000000", \
    "--wallet.accounts", "0x49721d8982a4ec22b94598ebdacc73046a00dc10c36991b912449b1506e6a9a2,1000000000000000000000", \
    "--wallet.accounts", "0x32c802b3bcef44cd304a15d9c8ff6e36724f43023ec2712c138dfcaa918c42a5,1000000000000000000000", \
    "--wallet.accounts", "0x6aa0c84d6da4126a27ed518fffaf237a76784cea2b6db305d1730ef516bad6c2,1000000000000000000000", \
    "--wallet.accounts", "0x72291a9549a31d0e4f7076f3bb91f22d2525a8e01f75429312c6f563ec06aa3c,1000000000000000000000", \
    "--wallet.accounts", "0xe1d84e821221b8deab74c480a83a71c7fda0e4e0c4d11a592a7704311ad64126,1000000000000000000000"]

# TO UPDATE THE IMAGE
# docker build . --platform linux/amd64 -t atn_reward_system
# docker tag atn_reward_system anmarhani/atn_reward_system
# docker push anmarhani/atn_reward_system 

