const electron = require('electron');
const path = require('path');
const BrowserWindow = electron.remote.BrowserWindow;


online_users = [];


function client_listener() {
    client.setEncoding('utf8');
    client.connect(port, servername, function () {
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
        if(message.content === '%isonline'){
            $chat.append('<div class="well" style="color: green">'+ message.username + 'is now online </div>');
        }
        $chat.append('<div class="well"><strong>'+
            message.username +'</strong> : '+
            message.content+'</div>');
    });

    //exit from server
    client.on('end', ()=>{
        client.write("%exit");
    });

    //Online Users


}

function shutdown_client(){
    client.write("%exit");
    client.end();
}

