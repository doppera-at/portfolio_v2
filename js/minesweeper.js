/*




Event-Listener for right click needed a flag after the function, as described here:
https://stackoverflow.com/questions/4235426/how-can-i-capture-the-right-click-event-in-javascript

To prevent the right click menu, I used this thread from StackOverflow:
https://stackoverflow.com/questions/737022/how-do-i-disable-right-click-on-my-web-page
*/

import { Logger } from "./logger.js"
var logger = new Logger("main", Logger.LOG_LEVELS.FINEST);

class Cell {
    index = -1;
    hasMine = false;
    revealed = false;
    flagged = false;
    numMinesAround = 0;

    constructor(index) {
        this.index = index;
    }

    getSymbol() {
        if (this.flagged) {
            return '🚩';
        }
        if (this.hasMine) {
            return '💣';
        }
        return this.numMinesAround;
    }
}

document.addEventListener("contextmenu", event => event.preventDefault());

logger.info(`Inizialization of game started. Defining constants and resetting variables.`);

const DIFFICULTIES = Object.freeze({
    Easy: { name: "Easy", numRows: 8, numCols: 8, numMines: 10, },
    Medium: { name: "Medium", numRows: 15, numCols: 15, numMines: 40, },
    Hard: { name: "Hard", numRows: 16, numCols: 30, numMines: 99, },
});
var difficulty = DIFFICULTIES.Easy;
var gameBoard = [];
var numCells = 0;
var cellsRevealed = 0;
var clickedOnMine = false;

// HTML Elements
const divStatusBar = document.getElementById("game-status");
const divControlBar = document.getElementById("game-control");
const divGameBoard = document.getElementById("game-board");

logger.info("Initialization finished.");


function startGame() {
    let log = logger.createSubLogger("startGame");
    log.info(`Starting a new game`);

    let difficultySelector = document.getElementById("select-difficulty");
    if (difficultySelector) {
        difficulty = DIFFICULTIES[difficultySelector.value];
    } else {
        difficulty = DIFFICULTIES.Easy;
    }
    logger.debug(`Difficulty read from selector: ${difficulty.name}`);

    divStatusBar.innerText = `Difficulty: ${difficulty.name}, Number of mines: ${difficulty.numMines}`;
    divStatusBar.style.removeProperty("background-color");
    logger.debug(`Status bar has been reset`);

    numCells = difficulty.numRows * difficulty.numCols
    cellsRevealed = 0;
    clickedOnMine = false;

    resetControlPanel();
    initializeGameBoard();
    renderGameBoard();

    log.info(`New game started!`);
}



function initializeGameBoard() {
    let log = logger.createSubLogger("initializeGameBoard");
    log.info(`Initializing the game board.`);

    gameBoard = [];
    numCells = difficulty.numRows * difficulty.numCols;
    for (let i = 0; i < numCells; i++) {
        gameBoard.push(new Cell(i));
        log.fine(`Added cell to game board: ${JSON.stringify(gameBoard.at(-1))}`);
    }
    log.debug(`Created ${gameBoard.length} cells on the game board`);

    let minesPlaced = [];
    while (minesPlaced.length < difficulty.numMines) {
        let index = Math.trunc(Math.random() * numCells);
        if (minesPlaced.includes(index)) continue;

        log.fine(`Making cell ${index} a mine.`);
        let cell = gameBoard[index];
        log.finer(`Cell at index ${index}:\n${JSON.stringify(cell)}`);
        if (cell.hasMine) continue;
    
        cell.hasMine = true;
        minesPlaced.push(index);
    }
    log.info(`Placed ${minesPlaced.length} mines on the board.`);

    for (let index = 0; index < numCells; index++) {
        let cell = gameBoard[index];

        if (cell.hasMine) continue;
        log.fine(`Cell ${index} has no mine. Calculating mine count.`);

        for (let dRow = index - difficulty.numCols; dRow <= index + difficulty.numCols; dRow += difficulty.numCols) {
            for (let dCol = -1; dCol <= 1; dCol++) {
                let dIndex = dRow + dCol;
                log.finer(`Checking index: ${dIndex}`);
                if (dIndex < 0 || dIndex >= numCells) {
                    log.finest(`   Index is out of bounds!`);
                    continue;
                }
                if (cell.index % difficulty.numCols == 0 && dIndex % difficulty.numCols > 1) {
                    log.finest(`   Cell at ${index} is at the left edge, but index ${dIndex} is on the right edge!`);
                    continue;
                }
                if (cell.index % difficulty.numCols == difficulty.numCols-1 && dIndex % difficulty.numCols == 0) {
                    log.finest(`   Cell at ${index} is at the right edge, but index ${dIndex} is on the left edge!`);
                    continue;
                }

                if (gameBoard[dIndex].hasMine) {
                    log.finest(`   Found a mine at index ${dIndex}.`);
                    cell.numMinesAround++;
                }
            }
        }
        log.debug(`Cell ${index} has ${cell.numMinesAround} mines around it.`);
    }
    log.info(`Calculated mineCount for each cell without a mine.`);

    log.info(`Finished initialization of the game board.`);
}



function renderGameBoard() {
    let log = logger.createSubLogger("renderGameBoard");
    log.info(`Rendering the game board.`);

    divGameBoard.innerHTML = "";
    let gridColumns = "";
    for (let i = 0; i < difficulty.numCols; i++) {
        gridColumns += " 2rem";
    }
    divGameBoard.style.gridTemplateColumns = gridColumns;
    let gridRows = "";
    for (let i = 0; i < difficulty.numRows; i++) {
        gridRows += " 2rem";
    }
    divGameBoard.style.gridTemplateRows = gridRows;
    for(let i = 0; i < numCells; i++) {
        let divCell = document.createElement("div");
        divCell.id = "div-" + i;
        divCell.name = i;
        divCell.addEventListener("click", revealCellEvent);
        divCell.addEventListener("contextmenu", flagCellEvent, false);
        divGameBoard.appendChild(divCell);
    }
    log.debug(`Added ${divGameBoard.getElementsByTagName('div').length} cells to the html document.`);
    log.info(`Finished rendering the game board.`);
}



function resetControlPanel() {
    let log = logger.createSubLogger("createControlPanels");
    log.info(`Creating the control panel.`);

    divControlBar.innerHTML = "";

    const buttonNewGame = document.createElement("button");
    buttonNewGame.id = "button-new-game";
    buttonNewGame.innerText = "New Game";
    buttonNewGame.addEventListener("click", () => startGame());
    log.debug(`Created button to start a new game with the selected difficulty.`);

    const difficultySelector = document.createElement("select");
    difficultySelector.id = "select-difficulty";
    difficultySelector.name = "select-difficulty";
    for (const [key, value] of Object.entries(DIFFICULTIES)) {
        log.fine(`Key/Value pair of difficulty entry:\n    ${key}, ${JSON.stringify(value)}`);
        const option = document.createElement("option");
        option.value = key;
        option.innerText = value.name;
        if (value.name == difficulty.name) {
            option.selected = true;
        }
        difficultySelector.appendChild(option);
    }
    difficultySelector.addEventListener("change", startGame);
    log.debug(`Created select element with all difficulties added as options`);

    divControlBar.appendChild(difficultySelector);
    divControlBar.appendChild(buttonNewGame);
    log.info(`Finished creating the control panel.`);
}



function revealCellEvent(event) {
    revealCell(event.target.name);
}
function revealCell(index) {
    let log = logger.createSubLogger("revealCell");

    let cell = gameBoard[index];
    if (!cell) {
        log.error(`Unable to get cell ${index}. Out of bounds?`);
        return;
    }
    log.debug(`Cell: ${JSON.stringify(cell)}`);

    if (cell.revealed) {
        log.warn(`Tried to reveal already revealed cell. This should be prevented!`);
        return;
    }

    log.info(`Revealing cell ${index}.`);
    cell.revealed = true;
    cellsRevealed++;

    let divCell = document.getElementById("div-" + cell.index);
    log.debug(`Div of Cell: ${JSON.stringify(divCell)}`);
    divCell.removeEventListener("click", revealCellEvent);
    divCell.removeEventListener("contextmenu", flagCellEvent);
    divCell.classList.add("revealed");
    divCell.innerText = cell.getSymbol();

    if (cell.hasMine) {
        divCell.classList.add("mine");
        clickedOnMine = true;
        gameOver();
    } else if (cellsRevealed >= numCells - difficulty.numMines) {
        gameOver();
    }

    if (!cell.hasMine && cell.numMinesAround == 0) {
        log.debug(`Cell has no mines around, so revealing those cells too`);
        for (let dRow = index - difficulty.numCols; dRow <= index + difficulty.numCols; dRow += difficulty.numCols) {
            for (let dCol = -1; dCol <= 1; dCol++) {
                let dIndex = dRow + dCol;
                log.finer(`Checking index: ${dIndex}`);
                if (dIndex < 0 || dIndex >= numCells) {
                    log.finest(`   Index is out of bounds!`);
                    continue;
                }
                if (index % difficulty.numCols == 0 && dIndex % difficulty.numCols > 1) {
                    log.finest(`   Cell at ${index} is at the left edge, but index ${dIndex} is on the right edge!`);
                    continue;
                }
                if (index % difficulty.numCols == difficulty.numCols-1 && dIndex % difficulty.numCols == 0) {
                    log.finest(`   Cell at ${index} is at the right edge, but index ${dIndex} is on the left edge!`);
                    continue;
                }
                if (gameBoard[dIndex].revealed) continue;

                revealCell(dIndex);
            }
        }
    }
}


function flagCellEvent(event) {
    flagCell(event.target.name);
}
function flagCell(index) {
    let log = logger.createSubLogger("flagCell");

    let cell = gameBoard[index];
    if (!cell) {
        log.error(`Unable to get cell ${index}. Out of bounds?`);
        return;
    }

    if (cell.revealed) {
        log.warn(`Tried to reveal already revealed cell. This should be prevented!`);
        return;
    }

    if (!cell.flagged) {
        log.info(`Flagging cell ${index}.`);
        log.debug(`   Cell: ${JSON.stringify(cell)}`);
        cell.flagged = true;

        let divCell = document.getElementById(`div-${index}`);
        log.debug(`Div of cell: ${JSON.stringify(divCell)}`);
        divCell.classList.add("flagged");
        divCell.innerText = cell.getSymbol();
        divCell.removeEventListener("click", revealCellEvent);
    } else {
        log.info(`Unflagging cell ${index}.`);
        log.debug(`   Cell: ${JSON.stringify(cell)}`);
        cell.flagged = false;

        let divCell = document.getElementById(`div-${index}`);
        log.debug(`Div of cell: ${JSON.stringify(divCell)}`);
        divCell.classList.remove("flagged");
        divCell.innerText = "";
        divCell.addEventListener("click", revealCellEvent);
    }
}


function gameOver() {
    let log = logger.createSubLogger("gameOver");

    let divs = divGameBoard.children;
    log.debug(divs);

    if (clickedOnMine) {
        log.info(`Clicked on a mine! Game is over!`);
        divStatusBar.style.backgroundColor = "red";
        divStatusBar.innerText = "You stepped on a mine! Game Over!";
    } else {
        log.info(`No mistake made! Congratulations!`);
        divStatusBar.style.backgroundColor = "green";
        divStatusBar.innerText = "You made it through the minefield! You Won! :D";
    }

    for (let i = 0; i < numCells; i++) {
        let cell = gameBoard[i];
        if (cell.flagged && cell.hasMine) {
            cell.flagged = false;
        }
        if (cell.hasMine && !cell.revealed) {
            revealCell(i);
        }
    }
}




startGame();
