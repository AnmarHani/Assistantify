base_account_private_key = '0x462cefb05c00f98aeba627b2acdeeddd0c8c816c5e371a7907e8cf9032320a0e'
base_account_address = '0x6A47D2F113Ab617F320Caf05cd164C62e1f1Db46'

contract_address = "0x9a3D8880E092e3a49f5041A7a901cacc7165674c"
contract_abi = [
    {
      "inputs": [
        {
          "name": "name_",
          "type": "string"
        },
        {
          "name": "symbol_",
          "type": "string"
        },
        {
          "name": "initialSupply",
          "type": "uint256"
        }
      ],
      "payable": "false",
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": "false",
      "inputs": [
        {
          "indexed": "true",
          "name": "from",
          "type": "address"
        },
        {
          "indexed": "true",
          "name": "to",
          "type": "address"
        },
        {
          "indexed": "false",
          "name": "value",
          "type": "uint256"
        }
      ],
      "name": "Transfer",
      "type": "event"
    },
    {
      "anonymous": "false",
      "inputs": [
        {
          "indexed": "true",
          "name": "owner",
          "type": "address"
        },
        {
          "indexed": "true",
          "name": "spender",
          "type": "address"
        },
        {
          "indexed": "false",
          "name": "value",
          "type": "uint256"
        }
      ],
      "name": "Approval",
      "type": "event"
    },
    {
      "constant": "true",
      "inputs": [],
      "name": "name",
      "outputs": [
        {
          "name": "",
          "type": "string"
        }
      ],
      "payable": "false",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": "true",
      "inputs": [],
      "name": "symbol",
      "outputs": [
        {
          "name": "",
          "type": "string"
        }
      ],
      "payable": "false",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": "true",
      "inputs": [],
      "name": "totalSupply",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": "false",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": "true",
      "inputs": [
        {
          "name": "account",
          "type": "address"
        }
      ],
      "name": "balanceOf",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": "false",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": "false",
      "inputs": [
        {
          "name": "recipient",
          "type": "address"
        },
        {
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "transfer",
      "outputs": [
        {
          "name": "",
          "type": "bool"
        }
      ],
      "payable": "false",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": "true",
      "inputs": [
        {
          "name": "owner",
          "type": "address"
        },
        {
          "name": "spender",
          "type": "address"
        }
      ],
      "name": "allowance",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": "false",
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": "false",
      "inputs": [
        {
          "name": "spender",
          "type": "address"
        },
        {
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "approve",
      "outputs": [
        {
          "name": "",
          "type": "bool"
        }
      ],
      "payable": "false",
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": "false",
      "inputs": [
        {
          "name": "sender",
          "type": "address"
        },
        {
          "name": "recipient",
          "type": "address"
        },
        {
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "transferFrom",
      "outputs": [
        {
          "name": "",
          "type": "bool"
        }
      ],
      "payable": "false",
      "stateMutability": "nonpayable",
      "type": "function"
    }
]
