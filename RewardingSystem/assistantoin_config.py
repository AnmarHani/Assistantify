base_account_private_key = (
    "0x849308eb66842fba203da62ac0abbc4f34d08fee0727c04ff701d4ea60d07688"
)
base_account_address = "0xBa88fb3cBe0D82fC7FF827608B0AD2a3A4BaCDb6"

contract_address = "0xCa0Da2766B7BfC0e0EA221448174a4e11Fdf79B0"
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
