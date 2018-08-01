const electron = require('electron');
const path = require('path');
const fs = require('fs');

class Server_Config {
    constructor(opts) {
        const user_data_path = (electron.app || electron.remote.app).getPath('userData');

        this.path = path.join(user_data_path, opts.configName + '.json');

        this.data = parseDataFile(this.path, opts.defaults);
    }

    get(key) {
        return this.data[key];
    }

    set(key, val) {
        this.data[key] = val;

        fs.writeFileSync(this.path, JSON.stringify(this.data));
    }
}

function parseDataFile(file_path, defaults) {
    try {
        return JSON.parse(fs.readFileSync(file_path));
    } catch (error) {
        return defaults;
    }
}

module.exports = Server_Config;
