base_account_private_key = (
    "0xf27e193c43a2cd1b4540f132e59223a938115465a91c0972d155dd4df9ae30c6"
)
base_account_address = "0x35BcFfFAD827B28F0492592c5564De7E26585174"

contract_address = "0xD3940535C56F9dAE2b5673F92B6F34509E03aE89"
contract_abi = [
    {
        "inputs": [
            {"name": "name_", "type": "string"},
            {"name": "symbol_", "type": "string"},
            {"name": "initialSupply", "type": "uint256"},
        ],
        "payable": "false",
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": "false",
        "inputs": [
            {"indexed": "true", "name": "from", "type": "address"},
            {"indexed": "true", "name": "to", "type": "address"},
            {"indexed": "false", "name": "value", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "anonymous": "false",
        "inputs": [
            {"indexed": "true", "name": "owner", "type": "address"},
            {"indexed": "true", "name": "spender", "type": "address"},
            {"indexed": "false", "name": "value", "type": "uint256"},
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "constant": "true",
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": "false",
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": "true",
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": "false",
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": "true",
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": "false",
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": "true",
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": "false",
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": "false",
        "inputs": [
            {"name": "recipient", "type": "address"},
            {"name": "amount", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": "false",
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": "true",
        "inputs": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": "false",
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": "false",
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": "false",
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": "false",
        "inputs": [
            {"name": "sender", "type": "address"},
            {"name": "recipient", "type": "address"},
            {"name": "amount", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": "false",
        "stateMutability": "nonpayable",
        "type": "function",
    },
]
