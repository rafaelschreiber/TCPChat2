var net = require('net');

var client = new net.Socket();

client.connect(2018, "2bhif.at", function () {
    alert('You now connected to 2bhif.at');
    console.log('Lerry');
    client.write('Hello!');
});