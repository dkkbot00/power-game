<!DOCTYPE html>
<html>
<head>
<title>Power Cyber X</title>
<style>
body {
    margin:0;
    background: linear-gradient(-45deg,#0a0015,#1a0033,#12001f,#000);
    background-size:400% 400%;
    animation: bgMove 12s ease infinite;
    font-family: Arial;
    text-align:center;
    color:white;
}

@keyframes bgMove {
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}

h2 {
    color:#c300ff;
    text-shadow:0 0 15px #c300ff;
}

.board {
    display:grid;
    grid-template-columns:repeat(3,90px);
    gap:10px;
    justify-content:center;
    margin-top:20px;
}

.cell {
    width:90px;
    height:90px;
    background:#111;
    border-radius:15px;
    font-size:40px;
    display:flex;
    align-items:center;
    justify-content:center;
    cursor:pointer;
    box-shadow:0 0 15px #c300ff;
    transition:0.2s;
}

.cell:hover {
    box-shadow:0 0 25px #ff00ff;
}

.X { color:#00f7ff; text-shadow:0 0 15px #00f7ff; }
.O { color:#ff00c8; text-shadow:0 0 15px #ff00c8; }

#winner {
    height:30px;
    margin-top:10px;
    font-size:18px;
    color:gold;
}

.score {
    margin-top:10px;
}

#musicToggle {
    position:absolute;
    top:15px;
    right:15px;
    width:45px;
    height:45px;
    border-radius:50%;
    background:#1a0033;
    border:2px solid #c300ff;
    color:white;
    font-size:20px;
    cursor:pointer;
    box-shadow:0 0 15px #c300ff;
}

#premiumBtn {
    margin-top:15px;
    padding:8px 15px;
    background:#1a0033;
    border:1px solid #c300ff;
    color:white;
    cursor:pointer;
}

#premiumPopup {
    display:none;
    position:fixed;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    background:#111;
    padding:20px;
    border:2px solid #c300ff;
    box-shadow:0 0 20px #c300ff;
}

</style>
</head>
<body>

<button id="musicToggle">🔊</button>

<h2>🔥 Power Cyber X 🔥</h2>

<div id="winner"></div>

<div class="score">
X: <span id="scoreX">0</span> |
AI: <span id="scoreO">0</span>
</div>

<div class="board" id="board"></div>

<button id="premiumBtn">💬 Premium Chat</button>

<div id="premiumPopup">
    <h3>🔒 Premium Chat Locked</h3>
    <p>Instagram: me.divakar00</p>
    <p>₹1 = 1 Day</p>
    <p>₹5 = 1 Week</p>
    <button onclick="closePremium()">Close</button>
</div>

<script>
let board = ["","","","","","","","",""];
let currentPlayer="X";
let scoreX=0, scoreO=0;
let aiWinStreak=0;
let aiMode="HARD";
let gameActive=true;

const boardDiv=document.getElementById("board");
const winner=document.getElementById("winner");

const bgMusic=new Audio("static/bg.mp3");
bgMusic.loop=true;
bgMusic.volume=0.15;

const xSound=new Audio("static/x.mp3");
const oSound=new Audio("static/o.mp3");
const winSound=new Audio("static/win.mp3");
const loseSound=new Audio("static/lose.mp3");
const clickSound=new Audio("static/click.mp3");

let musicStarted=false;
let musicOn=true;

function drawBoard(){
    boardDiv.innerHTML="";
    board.forEach((cell,index)=>{
        const div=document.createElement("div");
        div.classList.add("cell");
        if(cell) div.classList.add(cell);
        div.innerText=cell;
        div.onclick=()=>makeMove(index);
        boardDiv.appendChild(div);
    });
}

function makeMove(index){
    if(!gameActive) return;
    if(board[index]!=="" || currentPlayer!=="X") return;

    if(!musicStarted){
        bgMusic.play();
        musicStarted=true;
    }

    board[index]="X";
    xSound.play();
    currentPlayer="O";
    drawBoard();
    if(!checkWinner()) setTimeout(aiMove,500);
}

function aiMove(){
    let move=bestMove();
    board[move]="O";
    oSound.play();
    currentPlayer="X";
    drawBoard();
    checkWinner();
}

function bestMove(){
    for(let i=0;i<9;i++){
        if(board[i]===""){
            board[i]="O";
            if(isWin("O")){ board[i]=""; return i; }
            board[i]="";
        }
    }
    for(let i=0;i<9;i++){
        if(board[i]===""){
            board[i]="X";
            if(isWin("X")){ board[i]=""; return i; }
            board[i]="";
        }
    }
    return randomMove();
}

function randomMove(){
    let empty=board.map((v,i)=>v===""?i:null).filter(v=>v!==null);
    return empty[Math.floor(Math.random()*empty.length)];
}

function isWin(p){
    const w=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    return w.some(([a,b,c])=>board[a]===p&&board[b]===p&&board[c]===p);
}

function checkWinner(){
    if(isWin("X")){
        gameActive=false;
        winner.innerText="🥳 Player X Wins!";
        winSound.play();
        scoreX++;
        aiWinStreak=0;
        updateScore();
        setTimeout(resetGame,2000);
        return true;
    }
    if(isWin("O")){
        gameActive=false;
        winner.innerText="😈 AI Wins!";
        loseSound.play();
        scoreO++;
        aiWinStreak++;
        if(aiWinStreak>=4) aiMode="MEDIUM";
        updateScore();
        setTimeout(resetGame,2000);
        return true;
    }
    if(!board.includes("")){
        gameActive=false;
        winner.innerText="Draw!";
        setTimeout(resetGame,2000);
        return true;
    }
    return false;
}

function resetGame(){
    board=["","","","","","","","",""];
    currentPlayer="X";
    gameActive=true;
    winner.innerText="";
    drawBoard();
}

function updateScore(){
    document.getElementById("scoreX").innerText=scoreX;
    document.getElementById("scoreO").innerText=scoreO;
}

document.getElementById("musicToggle").onclick=function(){
    clickSound.play();
    if(musicOn){
        bgMusic.pause();
        this.innerText="🔇";
        musicOn=false;
    } else {
        bgMusic.play();
        this.innerText="🔊";
        musicOn=true;
    }
};

document.getElementById("premiumBtn").onclick=function(){
    clickSound.play();
    document.getElementById("premiumPopup").style.display="block";
};

function closePremium(){
    document.getElementById("premiumPopup").style.display="none";
}

drawBoard();
</script>

</body>
</html>
