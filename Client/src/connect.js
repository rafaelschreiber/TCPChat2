const electron = require('electron');
const path = require('path');
const BrowserWindow = electron.remote.BrowserWindow;


const add_server_btn = document.getElementById("add_server_btn");

let username;

function client_listener() {
    client.setEncoding('utf8');
    client.connect(2018, "localhost", function () {
        send_username();
    });
}

function send_username() {
    var name = "%setusername " + input;
    //var buffer_name = Buffer.from(name, 'utf8');
    client.write(name);
    send_data();
    receive_data();

}

function send_data() {
    $('#messageFrom').submit(function (event) {
        event.preventDefault();
        input = document.getElementById("message").value;
        input = "%send * " + input;
        client.write(input);
        $message.val('');
    });
}

function receive_data() {
    client.on('data', function (data) {
        console.log();
    });
}

add_server_btn.addEventListener('click', function (event) {
    const modalPath = path.join('/',__dirname, 'add.html');
    let win = new BrowserWindow({width: 300, height:400, resizable: false});
    win.loadFile(modalPath);
    win.show();
});
