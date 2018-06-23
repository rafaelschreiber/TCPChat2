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
    client.on('data', function (data) {
        console.log(data.toString);
        $chat.append('<div class="well">'+
            '<strong>'+ data.username +'</strong>'+'<div>'+
            data.content+'</div>');
    });

    //get all online users
    client.on('get users', function (data) {
        for(i =0; data.length; i++){
            html += '<li class="list-group-item">'+data[i]+'</li>';
        }
    });
    $users.html(html);

}



add_server_btn.addEventListener('click', function (event) {
    const modalPath = path.join('/',__dirname, 'add.html');
    let win = new BrowserWindow({width: 300, height:400, resizable: false});
    win.loadFile(modalPath);
    win.show();
});
