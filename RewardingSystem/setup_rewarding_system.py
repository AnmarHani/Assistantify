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
)
from utils.authentication_utils import get_current_user
from utils.database_utils import User, get_db


class RewardUserRequest(BaseModel):
    account_address: str
    amount: str = "1"


class GetAccountBalanceRequest(BaseModel):
    account_address: str


if TYPE_CHECKING:
    from fastapi import FastAPI

# Connect to Ganache
web3 = Web3(HTTPProvider("http://127.0.0.1:8545"))

# Initialize the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


def setup_rewarding_system(app: "FastAPI"):
    @app.get("/get_new_user_blockchain_account")
    def get_new_user_blockchain_account(
        current_user: str = Depends(get_current_user), db: Session = Depends(get_db)
    ):
        new_account = web3.eth.account.create()
        return new_account.address

    @app.post("/reward_user")
    def reward_user(request: RewardUserRequest):
        # Set the value to send
        value_as_str: str = request.amount
        value_as_str += "000000000000000000"

        value_as_int: int = int(value_as_str)

        # Get the nonce
        nonce = web3.eth.get_transaction_count(base_account_address)

        # Build a transaction to call the contract's `transfer` function
        transaction = contract.functions.transfer(
            request.account_address, value_as_int
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
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return txn_hash

    @app.post("/get_account_balance")
    def get_account_balance(request: GetAccountBalanceRequest):
        base_account_balance = web3.from_wei(
            contract.functions.balanceOf(base_account_address).call(), "ether"
        )
        account_balance = web3.from_wei(
            contract.functions.balanceOf(request.account_address).call(), "ether"
        )

        print(f"Balance of Base Account: {base_account_balance:.13f} tokens")

        return f"{account_balance:.0f}"
