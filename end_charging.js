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

web3 = new Web3(new Web3.providers.HttpProvider(settings.node_url));

web3.personal.unlockAccount(station_owner_eth_address, "123", '0x249F0');

var contract = web3.eth.contract(settings.ABI).at(station_eth_address);

contract.stopCharging({from: station_owner_eth_address}, (e, r) => {
    console.log('request for block');
  console.log(e,r);
  var chargingStopped = contract.ChargingStopped();
    chargingStopped.watch(function(error, result){
        console.log(error, result);
        var addr_station = result.args["_station"].toLowerCase();
        var addr_station_owner = result.args["_drone"].toLowerCase();
        if (addr_station_owner == station_owner_eth_address && addr_station == station_eth_address) {
            console.log("This is my booking (correct drone and station)");
            process.exit(0);
        } else {
            console.log("NOT my booking");
        }
    });
});