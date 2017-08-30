
// 2) interact with the startCharging contract function
// 3) wait for the Start charging event
// 4) Return 0 if booking is o.k., return 1 if not

// 1) get commandline arguments:
//     - the drone's ethereum address,
//     - the station's eth address,
//     - the start of the timeslot in seconds (unix time)
// 2) interact with the booking function of the station's contract
// 3) wait for the new booking event
// 4) Return 0 if booking is o.k., return 1 if not

var process = require('process');

if (process.argv.length < 5) {
    return 1;
}

// 1) get commandline argument: Is the drone's ethereum address
var drone_eth_address = process.argv[2];
var station_eth_address = process.argv[3];
var timeslot_start = process.argv[4];

console.log(drone_eth_address, station_eth_address, timeslot_start);

var Web3 = require('web3');

var settings = require('./settings');

web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

web3.personal.unlockAccount(web3.eth.accounts[2], "123", 150000);


//'0x772dcb53b59fc61410aa0514bebce8a9bb1e8ed6'

var contractAddress = '0x3f629cee69c94b4e83b3b98ac129022a26ccc478';

var ABI = [{
    "constant": false,
    "inputs": [],
    "name": "addDrone",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
}, {
    "constant": true,
    "inputs": [],
    "name": "getKeys",
    "outputs": [{
        "name": "",
        "type": "address[]"
    }],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
}, {
    "constant": true,
    "inputs": [{
        "name": "",
        "type": "address"
    }],
    "name": "register",
    "outputs": [{
        "name": "",
        "type": "uint256"
    }],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
}, {
    "constant": false,
    "inputs": [],
    "name": "removeDrone",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
}, {
    "inputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "constructor"
}, {
    "anonymous": false,
    "inputs": [{
        "indexed": false,
        "name": "",
        "type": "address"
    }],
    "name": "DroneAdded",
    "type": "event"
}, {
    "anonymous": false,
    "inputs": [{
        "indexed": false,
        "name": "",
        "type": "address"
    }],
    "name": "DroneRemoved",
    "type": "event"
}];

var drs = web3.eth.contract(ABI).at(contractAddress);

drs.addDrone({from: web3.eth.accounts[2]}, (e, r) => {
  console.log(e,r)
});


