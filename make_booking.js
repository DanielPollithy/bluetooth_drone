var process = require('process');

if (process.argv.length < 4) {
    return 1;
}

// 1) get commandline argument: Is the drone's ethereum address
var drone_eth_address = process.argv[2];
var station_eth_address = process.argv[3];



var Web3 = require('web3');

var settings = require('./settings');

web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

web3.personal.unlockAccount(drone_eth_address, "123", 150000);


//'0x772dcb53b59fc61410aa0514bebce8a9bb1e8ed6'

var contractAddress = '0x3f629cee69c94b4e83b3b98ac129022a26ccc478';

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

contract.register({from: drone_eth_address}, (e, r) => {
  console.log(e,r);
  var registered = contract.Registered();
    registered.watch(function(error, result){
        console.log(error, result);
        var addr_drone = result.args["_drone"];
        var success = result.args["result"];
        if (addr_drone == drone_eth_address) {
            console.log("This is my booking");
            if (success) {
                console.log("Booking successful");
                process.exit(0);
            } else {
                console.log("Booking NOT successful");
                process.exit(1);
            }
        } else {
            console.log("NOT my booking");
        }
    });
});








