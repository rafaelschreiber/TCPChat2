const electron = require('electron');
const path = require('path');
const BrowserWindow = electron.remote.BrowserWindow;


online_users = [];
var send_to = "*";



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
    client.write("%getusers");
    //send message
    $('#messageFrom').submit(function (event) {
        event.preventDefault();
        input = document.getElementById("message").value;
        input = '%send '+ send_to + ' "'+input + '"';
        client.write(input);
        $message.val('');
    });

    //receive message
    client.on('data', (data) => {
        console.log(data.toString());
        var message = JSON.parse(data);

        console.log(message.username + " : " + message.content);
        if(message.content === '%isonline'){

            $chat.append('<div class="well" style="color: green">'+ message.username + ' is now online </div>');
            scroll_down();
            client.write("%getusers");

        } else if(message.content === '%isoffline') {

            $chat.append('<div class="well" style="color: red">'+ message.username + ' is now offline </div>');
            scroll_down();
            client.write("%getusers");

        } else if (message.content === '%exit' && message.username === 'server'){

            $chat.append('<div class="well" style="color: red"><strong>Your are kick from the Server</strong></div>')
            scroll_down();
            setTimeout(function () {
            }, 999999999);
            $userFormArea.show();
            $messageArea.hide();

        }else if(message.username === 'server' && message.content === '%userlist'){

            get_online_users(message.userlist);
            create_single_chats(message.userlist);

        } else {

            $chat.append('<div class="well"><strong>'+
                message.username +'</strong> : '+
                message.content+'</div>');
            scroll_down();
        }
    });

    //exit from server
    client.on('end', ()=>{
        client.write("%exit");
    });

}

function get_online_users(data) {
    var html = '';
    for(i = 0; i < data.length; i++){
        html += '<li class="list-group-item" role="presentation" id="'+data[i]+'">'+data[i]+'</li>'
    }
    $users.html(html);
}

function create_single_chats(data) {
    var html = '';
    for(i = 0; i < data.length; i++){
        html += '<div class="chat" id="'+data[i]+'" style="display: none; width:615px;' +
            'height: 450px;"></div>';
    }
    $all_chats.html(html);
}

function start_single_chat(user) {
    $(user).show();
    $chat.hide();
    send_to = user;
}

function scroll_down() {
    document.getElementById("chat").scrollTop = document.getElementById("chat").scrollHeight;
}

function shutdown_client(){
    client.write("%exit");
    client.end();
}

