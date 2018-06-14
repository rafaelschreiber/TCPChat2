let net = require('net');

let client = new net.Socket();
let $userFormArea = $('#userFormArea');
let $user = $('#username');
let $userArea = $('#userArea');
let $messageArea = $('#messageArea');
let $messageFromArea = $('#messageFormArea');


client.connect(2018, "localhost");


$userFormArea.submit(function (event) {
    $userArea.hide();
    $messageArea.show();
    event.preventDefault();
    username = '%setusername ' + $user.val();
    client.write(username);
    $user.val('');
});