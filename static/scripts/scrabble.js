
// GLOBALS
let specials = {};
let playerBag = [undefined, undefined, undefined, undefined, undefined, undefined, undefined];
let full_grid = [];
let dictionary = [];
let letters_things = {
A:	[9,	1],
B:	[2,	3],
C:	[2,	3],
D:	[4,	2],
E:	[12,1],
F:  [2,	4],
G:	[3,	2],
H:	[2,	4],
I:	[9,	1],
J:	[1,	8],
K:	[1,	5],
L:	[4,	1],
M:	[2,	3],
N:	[6,	1],
O:	[8,	1],
P:	[2,	3],
Q:	[1,10],
R:	[6,	1],
S:	[4,	1],
T:	[6,	1],
U:	[4,	1],
V:	[2,	4],
W:	[2,	4],
X:	[1,	8],
Y:	[2,	4],
Z:	[1,10],
BLANK:	[2,	0]
};

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
  }

function getRandomLetter() {
	const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	return letters[Math.floor(Math.random() * letters.length)]
}

function placeTile(letter, row, col, playerTileCol=None) {
	const cell = document.getElementById(`cell-${row}-${col}`);
	// get rid of any special classesa
	cell.classList = [];

	// add the new classes
	cell.classList.add("cell");
	cell.classList.add("letter");
	cell.textContent = letter;3
	cell.draggable = true;

	cell.addEventListener('dragover', handleDragOver);
	cell.addEventListener('dragenter', handleDragEnter);
	cell.addEventListener('dragleave', handleDragLeave);
	cell.addEventListener('drop', handleDrop);
	cell.addEventListener('dragstart', handleDragStart);
	cell.addEventListener('dragend', handleDragEnd);

	// remove the letter from the player's bag
	playerBag[playerTileCol] = undefined;
	const playerTile = document.getElementById(`playerTile-${playerTileCol}`);
	playerTile.textContent = "";

}

function refillPlayerBag(playerBag) {
	for (let i = 0; i < 7; i++) {
		if(playerBag[i] == undefined){
			playerBag[i]=getRandomLetter()
			const cell = document.getElementById(`playerTile-${i}`);
			cell.classList.add("big_letter");
			cell.textContent = playerBag[i];
		}
	}
}

function handleDragStart(e) {
	this.style.opacity = '0.4';

	dragSrcEl = this;

	e.dataTransfer.effectAllowed = 'move';
	e.dataTransfer.setData('text/html', this.innerHTML);

  }
  
function handleDragEnd(e) {
	this.style.opacity = '1';
  }


function handleDragOver(e) {
e.preventDefault();
return false;
}

function handleDragEnter(e) {
this.classList.add('over');
}

function handleDragLeave(e) {
this.classList.remove('over');
}

function handleDrop(e) {
	e.stopPropagation(); // stops the browser from redirecting.
	this.innerHTML = e.dataTransfer.getData('text/html');
	this.classList.remove('over');
	tileCol = dragSrcEl.id.split("-")[1]
	placeTile(this.textContent, this.id.split("-")[1], this.id.split("-")[2],tileCol)
	return false;	
}

function setup(){
	specials = {
		"W3": [[0,0], [0,7], [0,14], [7,0], [7,14], [14,0], [14,7], [14,14]],
		"W2": [[1,1], [1,13], [2,2], [2,12], [3,3], [3,11], [4,4], [4,10], [10,4], [10,10], [11,3], [11,11], [12,2], [12,12], [13,1], [13,13]],
		"L3": [[1,5], [1,9], [5,1], [5,5], [5,9], [5,13], [9,1], [9,5], [9,9], [9,13], [13,5], [13,9]],
		"L2": [[0,3], [0,11], [2,6], [2,8], [3,0], [3,7], [3,14], [6,2], [6,6], [6,8], [6,12], [7,3], [7,11], [8,2], [8,6], [8,8], [8,12], [11,0], [11,7], [11,14], [12,6], [12,8], [14,3], [14,11]],
		"start": [[7,7]]
	}

	full_grid = []
	playerBag = [undefined, undefined, undefined, undefined, undefined, undefined, undefined]

	// Get the "scrabbleBoard" div element
	const boardContainer = document.getElementById("scrabbleBoard");

	// Create a 15x15 grid of divs
	const gridSize = 15;
	const grid = document.createElement("div");
	grid.classList.add("grid");

	for (let row = 0; row < gridSize; row++) {
		full_grid.push([])
		for (let col = 0; col < gridSize; col++) {
			full_grid[row].push(0)
			const cell = document.createElement("div");
			cell.classList.add("cell");
			cell.id = `cell-${row}-${col}`;
			cell.addEventListener('dragover', handleDragOver);
			cell.addEventListener('dragenter', handleDragEnter);
			cell.addEventListener('dragleave', handleDragLeave);
			cell.addEventListener('drop', handleDrop);
			grid.appendChild(cell);
		}
	}
	sleep(1).then(() => {
	// Add special tiles
	for (let special in specials) {
		for (let tile of specials[special]) {
			full_grid[tile[0]][tile[1]] = special
			const cell = document.getElementById(`cell-${tile[0]}-${tile[1]}`);
			cell.classList.add(special);
			if (special == "W3") {
				cell.textContent = "TW";
			}
			else if (special == "W2") {
				cell.textContent = "DW";
			}
			else if (special == "L3") {
				cell.textContent = "TL";
			}
			else if (special == "L2") {
				cell.textContent = "DL";
			}
			else if (special == "start") {
				cell.textContent = "★";
			}
		}
	}
	});

	// Create player tile 1x7 grid of divs
	const playerTileContainer = document.getElementById("playerTiles");
	const playerTileSize = 7;
	const playerTileGrid = document.createElement("div");
	playerTileGrid.classList.add("playerTileGrid");

	playerTileGrid.classList.add("grid");
	for (let col = 0; col < playerTileSize; col++) {
		const cell = document.createElement("div");
		cell.classList.add("playerCell");
		cell.id = `playerTile-${col}`;
		cell.draggable = true;
		cell.addEventListener('dragstart', handleDragStart);
		cell.addEventListener('dragend', handleDragEnd);
		playerTileGrid.appendChild(cell);
	}

	sleep(1).then(() => {
	refillPlayerBag(playerBag);
	});

	// append the children to the parents
	playerTileContainer.appendChild(playerTileGrid);
	boardContainer.appendChild(grid);
	playerTileContainer.appendChild(playerTileGrid);
}



