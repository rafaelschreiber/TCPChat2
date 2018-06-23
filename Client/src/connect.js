const electron = require('electron');
const path = require('path');
const BrowserWindow = electron.remote.BrowserWindow;


const add_server_btn = document.getElementById("add_server_btn");

function client_listener() {
    client.setEncoding('utf8');
    client.connect(2018, "localhost", function () {
        data_traffic();
    });
}

function data_traffic() {
    //send server username
    var name = "%setusername " + input;
    client.write(name);

    //send message
    $('#messageFrom').submit(function (event) {
        event.preventDefault();
        input = document.getElementById("message").value;
        input = '%send * ' + '"'+input + '"';
        client.write(input);
        $message.val('');
    });

    //receive message
    client.on('data', (data) => {
        console.log(data.toString());
        var message = JSON.parse(data);
        console.log(message.username + " : " + message.content);
        $chat.append('<div class="well"><strong>'+
            message.username +'</strong> : '+
            message.content+'</div>');
    })
    //get all online users

}



add_server_btn.addEventListener('click', function (event) {
    const modalPath = path.join('/',__dirname, 'add.html');
    let win = new BrowserWindow({width: 300, height:400, resizable: false});
    win.loadFile(modalPath);
    win.show();
});
