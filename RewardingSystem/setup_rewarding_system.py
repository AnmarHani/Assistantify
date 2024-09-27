from typing import TYPE_CHECKING

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from web3 import HTTPProvider, Web3

from RewardingSystem.assistantoin_config import (
    base_account_address,
    base_account_private_key,
    contract_abi,
    contract_address,
    ganache_server
)
from utils.authentication_utils import get_current_user
from utils.database_utils import User, get_db

import random


class RewardUserRequest(BaseModel):
    account_address: str
    amount: str = "1"


class GetAccountBalanceRequest(BaseModel):
    account_address: str


if TYPE_CHECKING:
    from fastapi import FastAPI

# Connect to Ganache
web3 = Web3(HTTPProvider(ganache_server))

# Initialize the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


def setup_rewarding_system(app: "FastAPI"):
    @app.get("/get_new_user_blockchain_account")
    def get_new_user_blockchain_account():
        accounts = web3.eth.accounts
        return random.choice(accounts)

    @app.post("/reward_user")
    def reward_user(request: RewardUserRequest):
        # Set the value to send
        value_as_str: str= "00000000000000"
        value_as_str += request.amount

        value_as_int: int = int(value_as_str)
        
        base_account_address_converted = web3.to_checksum_address(
            int(base_account_address.strip('"'), 16)
        )
        
        # Get the nonce
        nonce = web3.eth.get_transaction_count(base_account_address_converted)
        
        recipent_account_address_converted = web3.to_checksum_address(
            int(request.account_address.strip('"'), 16)
        )
        print("RECIPENT", recipent_account_address_converted)
        # Build a transaction to call the contract's `transfer` function
        transaction = contract.functions.transfer(
            recipent_account_address_converted, value_as_int
        ).build_transaction(
            {
                "gas": 2000000,
                "gasPrice": web3.to_wei("50", "gwei"),
                "nonce": nonce,
            }
        )

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(
            transaction, base_account_private_key
        )

        # Send the transaction
        web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return "Rewarded the User!"

    @app.post("/get_account_balance")
    def get_account_balance(request: GetAccountBalanceRequest):
        base_account_address_converted = web3.to_checksum_address(
            int(base_account_address.strip('"'), 16)
        )
        recipent_account_address_converted = web3.to_checksum_address(
            int(request.account_address.strip('"'), 16)
        )

        base_account_balance = contract.functions.balanceOf(base_account_address_converted).call()
        account_balance = contract.functions.balanceOf(recipent_account_address_converted).call()

        print("BASE ACC BALANCE: ", base_account_balance)

        return str(account_balance).lstrip('0')
