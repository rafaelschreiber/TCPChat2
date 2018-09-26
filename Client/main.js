const {app, BrowserWindow, Menu} = require('electron');
const shell = require('electron').shell;

let win;

function createWindow () {
    win = new BrowserWindow({width: 1000,height: 650,resizable: false});

    win.loadFile('src/index.html');

    const template = [{
        label: 'Edit',
        submenu: [{
            label: 'Go to our Website',

            accelerator: (() =>{
                if(process.platform === 'darwin'){
                    return 'Alt+Command+B';
                } else {
                    return 'Ctrl+Shift+B';
                }
            })(),
            click: function () {
                shell.openExternal('https://3bhif.at');
            }

        },{
            type: 'separator'
        },{
            label: 'Quit',
            accelerator: 'CmdOrCtrl+q',
            role: 'quit',
        }]
    },{
        label: 'View',
        submenu: [{
            label: 'Toggle Developer Tools',
            accelerator: (() => {
                if(process.platform === 'darwin'){
                    return 'Alt+Command+I';
                } else {
                    return 'Ctrl+Shift+I';
                }
            })(),
            click: (items, focusedWindow) => {
                if(focusedWindow){
                    focusedWindow.toggleDevTools();
                    console.log('Test123');
                }
            }
        }]
    }];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);

    //win.webContents.openDevTools()

    win.on('closed', () => {
        win = null;
    });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
});



app.on('activate', () => {
    if (win === null) {
        createWindow()
    }
});