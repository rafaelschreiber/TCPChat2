const fs = require('fs'),
    xml2js = require('xml2js');

let parser = new xml2js.Parser();


fs.readFile(__dirname + '../assets/xml/colors.xml', function (err, data) {
    parser.parseString(data, function (err, result) {
        console.dir(result);
        console.log('Read finished');
    });
});
