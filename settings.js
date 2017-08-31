var ABI = [
 {
   "constant": true,
   "inputs": [],
   "name": "chargingPrice",
   "outputs": [
     {
       "name": "",
       "type": "uint256"
     }
   ],
   "payable": false,
   "stateMutability": "view",
   "type": "function"
 },
 {
   "constant": false,
   "inputs": [],
   "name": "register",
   "outputs": [],
   "payable": false,
   "stateMutability": "nonpayable",
   "type": "function"
 },
 {
   "constant": false,
   "inputs": [],
   "name": "withdraw",
   "outputs": [],
   "payable": false,
   "stateMutability": "nonpayable",
   "type": "function"
 },
 {
   "constant": false,
   "inputs": [],
   "name": "stopCharging",
   "outputs": [],
   "payable": false,
   "stateMutability": "nonpayable",
   "type": "function"
 },
 {
   "constant": false,
   "inputs": [
     {
       "name": "_chargingPrice",
       "type": "uint256"
     }
   ],
   "name": "setChargingPrice",
   "outputs": [],
   "payable": false,
   "stateMutability": "nonpayable",
   "type": "function"
 },
 {
   "constant": true,
   "inputs": [],
   "name": "stationOwner",
   "outputs": [
     {
       "name": "",
       "type": "address"
     }
   ],
   "payable": false,
   "stateMutability": "view",
   "type": "function"
 },
 {
   "constant": false,
   "inputs": [],
   "name": "startCharging",
   "outputs": [],
   "payable": false,
   "stateMutability": "nonpayable",
   "type": "function"
 },
 {
   "constant": true,
   "inputs": [
     {
       "name": "",
       "type": "address"
     }
   ],
   "name": "refund",
   "outputs": [
     {
       "name": "",
       "type": "uint256"
     }
   ],
   "payable": false,
   "stateMutability": "view",
   "type": "function"
 },
 {
   "inputs": [],
   "payable": false,
   "stateMutability": "nonpayable",
   "type": "constructor"
 },
 {
   "anonymous": false,
   "inputs": [
     {
       "indexed": false,
       "name": "_drone",
       "type": "address"
     },
     {
       "indexed": false,
       "name": "result",
       "type": "bool"
     }
   ],
   "name": "Registered",
   "type": "event"
 },
 {
   "anonymous": false,
   "inputs": [
     {
       "indexed": false,
       "name": "_station",
       "type": "address"
     },
     {
       "indexed": false,
       "name": "_drone",
       "type": "address"
     }
   ],
   "name": "ChargingStarts",
   "type": "event"
 },
 {
   "anonymous": false,
   "inputs": [
     {
       "indexed": false,
       "name": "_station",
       "type": "address"
     },
     {
       "indexed": false,
       "name": "_drone",
       "type": "address"
     }
   ],
   "name": "ChargingStopped",
   "type": "event"
 }
];


module.exports = {
    'ABI': ABI,
    'node_url': 'http://192.168.1.120:8545',
};