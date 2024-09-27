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

# Available Accounts
# ==================
# (0) 0x1e942421C6F9F3Bf873484F57Ef24736d581EbCc (1000 ETH)
# (1) 0x1911C85D1320A015bD2a4F97C46Fe58dC358A754 (1000 ETH)
# (2) 0xC3BbB97eE6b124D73101B0C292DA97E334C554Ef (1000 ETH)
# (3) 0x82E269a65238552eD30Ee18f91e50428Af976707 (1000 ETH)
# (4) 0x79FdDefC6C25F59d8DbD942B45EcC1637acFdE03 (1000 ETH)
# (5) 0xD7c18c4A08613C01B5EeEAf91C254824C782DE8F (1000 ETH)
# (6) 0x8Dc71636761625BA821Ae9731Ab1E97026772127 (1000 ETH)
# (7) 0x714e4a7A84EE496c42eb1456B7bd23ec752F7923 (1000 ETH)
# (8) 0x23bb1b3bb494fF282Dd8Fd18bfe0ed8762d55699 (1000 ETH)
# (9) 0x07D471A152245a289315bAc204bEe4F1AA96cB10 (1000 ETH)

# Private Keys
# ==================
# (0) 0xdad9e921281699147567f2725a3184a01723b180f1647411c2a9e65a65342a90
# (1) 0xa893995244239b9035064065b30a0fe3d25952bcd4760a5eda0ee9cf1209307c
# (2) 0x168c818eb8f7ac1462fe4dee75602b3a3c500ab2c4b9d1e781d70aad4d8dd3ba
# (3) 0x1635353143137545f691a731667fc92e4c9c1e1193fbc238d6bc287f53c4a99b
# (4) 0x25f1a6d047df08245ef845f3cc273264f897eeced95a05554cbdd5e28f56a6f3
# (5) 0x49721d8982a4ec22b94598ebdacc73046a00dc10c36991b912449b1506e6a9a2
# (6) 0x32c802b3bcef44cd304a15d9c8ff6e36724f43023ec2712c138dfcaa918c42a5
# (7) 0x6aa0c84d6da4126a27ed518fffaf237a76784cea2b6db305d1730ef516bad6c2
# (8) 0x72291a9549a31d0e4f7076f3bb91f22d2525a8e01f75429312c6f563ec06aa3c

