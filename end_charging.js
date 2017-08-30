var process = require('process');

if (process.argv.length < 5) {
    console.log('not enough params')
    return 1;
}

// 1) get commandline argument: Is the drone's ethereum address
var drone_eth_address = process.argv[2].toLowerCase();
var station_eth_address = process.argv[3].toLowerCase();
var station_owner_eth_address = process.argv[4].toLowerCase();



var Web3 = require('web3');

var settings = require('./settings');

web3 = new Web3(new Web3.providers.HttpProvider("http://192.168.1.120:8545"));
console.log('connection established');

web3.personal.unlockAccount(station_owner_eth_address, "123", '0x249F0');
console.log('account unlocked');

var ABI = [{
    "constant": true,
    "inputs": [],
    "name": "chargingPrice",
    "outputs": [{"name": "", "type": "uint256"}],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
}, {
    "constant": false,
    "inputs": [],
    "name": "register",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
}, {
    "constant": false,
    "inputs": [],
    "name": "withdraw",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
}, {
    "constant": false,
    "inputs": [],
    "name": "stopCharging",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
}, {
    "constant": false,
    "inputs": [{"name": "_chargingPrice", "type": "uint256"}],
    "name": "setChargingPrice",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
}, {
    "constant": false,
    "inputs": [],
    "name": "startCharging",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
}, {
    "constant": true,
    "inputs": [{"name": "", "type": "address"}],
    "name": "refund",
    "outputs": [{"name": "", "type": "uint256"}],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
}, {"inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}, {
    "anonymous": false,
    "inputs": [{"indexed": false, "name": "_drone", "type": "address"}, {
        "indexed": false,
        "name": "result",
        "type": "bool"
    }],
    "name": "Registered",
    "type": "event"
}, {
    "anonymous": false,
    "inputs": [{"indexed": false, "name": "_station", "type": "address"}, {
        "indexed": false,
        "name": "_drone",
        "type": "address"
    }],
    "name": "ChargingStarts",
    "type": "event"
}, {
    "anonymous": false,
    "inputs": [{"indexed": false, "name": "_station", "type": "address"}, {
        "indexed": false,
        "name": "_drone",
        "type": "address"
    }],
    "name": "ChargingStopped",
    "type": "event"
}];

var contract = web3.eth.contract(ABI).at(station_eth_address);
console.log('contract abi is here');

contract.stopCharging({from: station_owner_eth_address}, (e, r) => {
    console.log('request for block');
  console.log(e,r);
  var chargingStopped = contract.ChargingStopped();
    chargingStopped.watch(function(error, result){
        console.log(error, result);
        var addr_station = result.args["_station"].toLowerCase();
        var addr_drone = result.args["_drone"].toLowerCase();
        if (addr_drone == drone_eth_address && addr_station == station_owner_eth_address) {
            console.log("This is my booking (correct drone and station)");
            process.exit(0);
        } else {
            console.log("NOT my booking");
        }
    });
});