// CUSTOM LOGGER to provide different levels of log messages,
// especially useful to show debugging informtion when coding, but only
// have informative output after the script is finished

// I used the Mozilla Developer Network to learn about class structure,
// and how to format output for console.log().
// The resulting logger was then easy to write, following the basic 
// structure I also used in Java already

export class Logger {

    static LOG_LEVELS = Object.freeze({
        ERROR: 100,
        WARNING: 200,
        INFO: 400,
        DEBUG: 800,
        FINE: 1000,
        FINER: 1200,
        FINEST: 1500,
    })

    logLevel = 0;
    method = "main"

    constructor(method, logLevel) {
        if (!method || typeof method != "string") method = "";
        if (!logLevel || isNaN(logLevel)) logLevel = Logger.LOG_LEVELS.INFO;
        this.method = method;
        this.logLevel = logLevel;
    }


    log(message, logLevel) {
        if (logLevel > this.logLevel) return;
        console.log(
            "%c%s:%s> %s",
            this.getStyleForLevel(logLevel),
            this.getPrefixForLevel(logLevel),
            this.method,
            message);
    }

    error(message) {
        this.log(message, Logger.LOG_LEVELS.ERROR);
    }
    warn(message) {
        this.log(message, Logger.LOG_LEVELS.WARNING);
    }
    info(message) {
        this.log(message, Logger.LOG_LEVELS.INFO);
    }
    debug(message) {
        this.log(message, Logger.LOG_LEVELS.DEBUG);
    }
    fine(message) {
        this.log(message, Logger.LOG_LEVELS.FINE);
    }
    finer(message) {
        this.log(message, Logger.LOG_LEVELS.FINER);
    }
    finest(message) {
        this.log(message, Logger.LOG_LEVELS.FINEST);
    }


    getStyleForLevel(logLevel) {
        switch (logLevel) {
            case Logger.LOG_LEVELS.ERROR: return "color: #c02;"
            case Logger.LOG_LEVELS.WARNING: return "color: #aa0;"
            case Logger.LOG_LEVELS.INFO: return ""
            case Logger.LOG_LEVELS.DEBUG: return "color: #999;"
            case Logger.LOG_LEVELS.FINE: return "color: #777;"
            case Logger.LOG_LEVELS.FINER: return "color: #555;"
            case Logger.LOG_LEVELS.FINEST: return "color: #333;"
            default: return "";
        }
    }
    getPrefixForLevel(logLevel) {
        switch (logLevel) {
            case Logger.LOG_LEVELS.ERROR: return "ERROR";
            case Logger.LOG_LEVELS.WARNING: return "WARN"
            case Logger.LOG_LEVELS.INFO: return "Info"
            case Logger.LOG_LEVELS.DEBUG: return "Debug"
            case Logger.LOG_LEVELS.FINE: return "Fine";
            case Logger.LOG_LEVELS.FINER: return "Finer";
            case Logger.LOG_LEVELS.FINEST: return "Finest";
            default: return "";
        }
    }


    createSubLogger(method) {
        if (!method || typeof method !== "string") method = "undef";
        return new Logger(method, this.logLevel);
    }
}