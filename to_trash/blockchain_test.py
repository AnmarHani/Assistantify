


# Initialize the contract
contract = web3.eth.contract(address=contract_name, abi=contract_abi)

# Replace with your account's private key and the recipient's address
private_key = '0xdf1c9ea0f925bc5f9191c0efb2f2fd386023fc2bbe1babb7dbb7a7b7f23d07e0'
account = '0x5E74c269af19Be6bcd796FD8c8599DB6eBc9b950'
recipient = '0xFd8f5764301a695dCbfC422392c89dcC50Bbf3b0'

# Set the value to send
value = "1"  # 5 tokens
value += "000000000000000000"
value = int(value)

print("VALUE",f"{web3.from_wei(value, 'ether'):.13f}")

# Get the nonce
nonce = web3.eth.get_transaction_count(account)

# Build a transaction to call the contract's `transfer` function
transaction = contract.functions.transfer(recipient, value).build_transaction({
    'gas': 2000000,
    'gasPrice': web3.to_wei('50', 'gwei'),
    'nonce': nonce,
})

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

print(f'Transaction hash: {txn_hash.hex()}')

# Get the balance of the accounts
balance_sender = web3.from_wei(contract.functions.balanceOf(account).call(), 'ether')
balance_recipient = web3.from_wei(contract.functions.balanceOf(recipient).call(), 'ether')
print(f'Balance of sender: {balance_sender:.13f} tokens')
print(f'Balance of recipient: {balance_recipient:.13f} tokens')