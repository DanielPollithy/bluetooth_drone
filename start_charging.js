var process = require('process');

if (process.argv.length < 4) {
    return 1;
}

// 1) get commandline argument: Is the drone's ethereum address
var drone_eth_address = process.argv[2].toLowerCase();
var station_eth_address = process.argv[3].toLowerCase();



var Web3 = require('web3');

var settings = require('./settings');

web3 = new Web3(new Web3.providers.HttpProvider(settings.node_url));

web3.personal.unlockAccount(drone_eth_address, "123", '0x249F0');

var contract = web3.eth.contract(settings.ABI).at(station_eth_address);

setTimeout(function () {
    process.exit(1);
}, 7000);

contract.startCharging({from: drone_eth_address}, (e, r) => {
  console.log(e,r);
  var chargingStarts = contract.ChargingStarts();
    chargingStarts.watch(function(error, result){
        var addr_station = result.args["_station"].toLowerCase();
        var addr_drone = result.args["_drone"].toLowerCase();
        if (addr_drone == drone_eth_address && addr_station == station_eth_address) {
            console.log("OK");
            process.exit(0);
        } else {
        }
    });
});