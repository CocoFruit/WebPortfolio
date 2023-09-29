const choices = ["rock", "paper", "scissors"];
const playerHand = document.getElementById("player-choice");
const computerHand = document.getElementById("computer-choice");
const resultText = document.querySelector(".result p");
const choiceButtons = document.querySelectorAll(".choice");

choiceButtons.forEach(button => {
    button.addEventListener("click", () => {
        const playerChoice = button.getAttribute("data-choice");
        const computerChoice = choices[Math.floor(Math.random() * choices.length)];
        playerHand.src = `images/${playerChoice}.jpg`;
        computerHand.src = `images/${computerChoice}.jpg`;
        
        setTimeout(() => {
            const winner = determineWinner(playerChoice, computerChoice);
            displayResult(winner);
        }, 1500);
    });
});

function determineWinner(playerChoice, computerChoice) {
    if (playerChoice === computerChoice) {
        return "It's a tie!";
    } else if (
        (playerChoice === "rock" && computerChoice === "scissors") ||
        (playerChoice === "paper" && computerChoice === "rock") ||
        (playerChoice === "scissors" && computerChoice === "paper")
    ) {
        return "Player wins!";
    } else {
        return "Computer wins!";
    }
}

function displayResult(winner) {
    resultText.textContent = winner;
}
