
function client_listener() {
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
        client.write(input);
        $message.val('');
    });
}

function receive_data() {
    client.on('data', function (data) {
        console.log(data.username);
    });
}