// ============================================
// FAKENEWS ROULETTE - GAME LOGIC
// ============================================

// Game Constants
const GAME_CONSTANTS = {
    SPIN_DURATION: 4000,      // Duration of wheel spin animation in ms
    GAME_OVER_DELAY: 2000,    // Delay before showing game over modal
    NEXT_QUESTION_DELAY: 1500, // Delay before enabling next spin
    PARTICLE_LIFETIME: 1000,   // How long particles last in ms
    BASE_SCORE_MULTIPLIER: 100, // Points per difficulty level
    STREAK_BONUS: 50,          // Extra points per streak
    MAX_STREAK_BONUS: 5        // Maximum streak bonus multiplier
};

// News Data (Mix of real and fake news)
const newsData = [
    {
        text: "Nel 2017, un uomo ha venduto la sua casa per comprare Bitcoin quando valevano circa 1.000$ ciascuno.",
        isReal: true,
        explanation: "Questa storia è vera! Didi Taihuttu ha venduto tutto, inclusa la sua casa, per investire in Bitcoin nel 2017.",
        difficulty: 2
    },
    {
        text: "La Torre Eiffel cresce di 15 centimetri ogni estate a causa dell'espansione termica del metallo.",
        isReal: true,
        explanation: "Vero! L'acciaio si espande con il calore, facendo crescere la torre di circa 15 cm nelle giornate più calde.",
        difficulty: 3
    },
    {
        text: "Il governo italiano ha approvato una legge che rende obbligatorio mangiare pasta almeno 3 volte a settimana.",
        isReal: false,
        explanation: "Questa è una notizia falsa! Non esiste nessuna legge del genere in Italia.",
        difficulty: 1
    },
    {
        text: "Le api possono riconoscere i volti umani e ricordarli per diversi giorni.",
        isReal: true,
        explanation: "Sorprendentemente vero! Gli studi hanno dimostrato che le api hanno capacità di riconoscimento facciale.",
        difficulty: 3
    },
    {
        text: "La NASA ha scoperto un pianeta fatto interamente di diamante a 40 anni luce dalla Terra.",
        isReal: true,
        explanation: "Vero! Il pianeta 55 Cancri e contiene una quantità enorme di carbonio cristallizzato (diamante).",
        difficulty: 2
    },
    {
        text: "In Giappone è stato inventato un gelato che non si scioglie mai, nemmeno a temperature elevate.",
        isReal: true,
        explanation: "Vero! Bioscienze Kanazawa ha creato un gelato con estratto di fragola che mantiene la sua forma molto più a lungo.",
        difficulty: 2
    },
    {
        text: "Elon Musk ha annunciato che Tesla produrrà macchine volanti entro il 2025.",
        isReal: false,
        explanation: "Falso! Non c'è stato nessun annuncio ufficiale di questo tipo da parte di Tesla o Elon Musk.",
        difficulty: 1
    },
    {
        text: "I polpi hanno tre cuori e il loro sangue è di colore blu.",
        isReal: true,
        explanation: "Assolutamente vero! I polpi hanno tre cuori e sangue blu a base di rame.",
        difficulty: 2
    },
    {
        text: "L'Islanda sta costruendo il primo aeroporto spaziale commerciale d'Europa.",
        isReal: false,
        explanation: "Falso! Non esiste nessun progetto confermato per un aeroporto spaziale in Islanda.",
        difficulty: 2
    },
    {
        text: "In Australia esistono più canguri che persone.",
        isReal: true,
        explanation: "Vero! L'Australia ha circa 50 milioni di canguri contro 25 milioni di abitanti.",
        difficulty: 1
    },
    {
        text: "Google ha sviluppato un traduttore universale per comunicare con i delfini.",
        isReal: false,
        explanation: "Falso! Anche se ci sono ricerche sulla comunicazione dei delfini, non esiste un traduttore del genere.",
        difficulty: 2
    },
    {
        text: "Il miele non scade mai e può essere consumato anche dopo migliaia di anni.",
        isReal: true,
        explanation: "Vero! Il miele trovato nelle tombe egizie di 3000 anni fa era ancora commestibile.",
        difficulty: 1
    },
    {
        text: "In Svizzera è illegale possedere un solo porcellino d'India perché sono animali sociali.",
        isReal: true,
        explanation: "Vero! La legge svizzera richiede che i porcellini d'India siano tenuti in coppia.",
        difficulty: 3
    },
    {
        text: "Amazon ha brevettato un drone che può consegnare pacchi in meno di 30 secondi tramite teletrasporto.",
        isReal: false,
        explanation: "Ovviamente falso! Il teletrasporto non esiste nella tecnologia attuale.",
        difficulty: 1
    },
    {
        text: "Le banane sono radioattive, ma la quantità di radiazioni è troppo piccola per essere pericolosa.",
        isReal: true,
        explanation: "Vero! Le banane contengono potassio-40, un isotopo radioattivo, ma in quantità innocue.",
        difficulty: 3
    },
    {
        text: "Un fulmine può raggiungere temperature cinque volte più alte della superficie del sole.",
        isReal: true,
        explanation: "Vero! Un fulmine può raggiungere 30.000 Kelvin, mentre la superficie del sole è circa 5.500 Kelvin.",
        difficulty: 2
    },
    {
        text: "L'Italia ha vietato la vendita di pizza con ananas in tutto il territorio nazionale.",
        isReal: false,
        explanation: "Falso! Non esiste nessuna legge del genere, anche se molti italiani non apprezzano questa combinazione.",
        difficulty: 1
    },
    {
        text: "Il cuore di una balena blu è così grande che un bambino potrebbe nuotare attraverso le sue arterie.",
        isReal: true,
        explanation: "Vero! Il cuore di una balena blu può pesare fino a 180 kg con arterie enormi.",
        difficulty: 2
    },
    {
        text: "Gli smartphone di nuova generazione possono ricaricarsi al 100% in 5 secondi usando l'energia solare.",
        isReal: false,
        explanation: "Falso! La tecnologia attuale non permette una ricarica così veloce, specialmente con l'energia solare.",
        difficulty: 1
    },
    {
        text: "In Giappone esiste un treno che raggiunge i 600 km/h usando la levitazione magnetica.",
        isReal: true,
        explanation: "Vero! Il treno maglev giapponese ha stabilito record di velocità superiori ai 600 km/h.",
        difficulty: 2
    },
    {
        text: "Facebook ha creato un'intelligenza artificiale che può leggere i pensieri umani.",
        isReal: false,
        explanation: "Falso! La tecnologia attuale non permette di leggere i pensieri, anche se ci sono ricerche su interfacce cervello-computer.",
        difficulty: 2
    },
    {
        text: "Le impronte digitali dei koala sono così simili a quelle umane che potrebbero confondere le indagini forensi.",
        isReal: true,
        explanation: "Sorprendentemente vero! I koala hanno impronte digitali quasi identiche a quelle umane.",
        difficulty: 3
    },
    {
        text: "La Grande Muraglia Cinese è visibile dalla Luna a occhio nudo.",
        isReal: false,
        explanation: "Falso! Gli astronauti hanno confermato che la muraglia non è visibile dalla Luna senza strumenti.",
        difficulty: 1
    },
    {
        text: "Un gruppo di fenicotteri si chiama 'flamboyance' in inglese.",
        isReal: true,
        explanation: "Vero! Il termine collettivo per un gruppo di fenicotteri è effettivamente 'flamboyance'.",
        difficulty: 3
    },
    {
        text: "Il Vaticano ha il più alto tasso di criminalità pro capite al mondo.",
        isReal: true,
        explanation: "Tecnicamente vero! Con una popolazione così piccola, anche pochi crimini (come borseggi) creano statistiche alte.",
        difficulty: 3
    },
    {
        text: "Apple sta sviluppando un iPhone pieghevole che può essere arrotolato come un foglio di carta.",
        isReal: false,
        explanation: "Falso! Non ci sono annunci ufficiali di un iPhone che si arrotola come un foglio.",
        difficulty: 2
    },
    {
        text: "Gli elefanti sono gli unici animali che non possono saltare.",
        isReal: true,
        explanation: "Vero! A causa della loro struttura fisica, gli elefanti non possono saltare.",
        difficulty: 1
    },
    {
        text: "Esiste un lago in Tanzania che trasforma gli animali in statue di pietra.",
        isReal: true,
        explanation: "Vero! Il Lago Natron ha acque così alcaline che possono calcificare gli animali morti.",
        difficulty: 3
    },
    {
        text: "La Cina ha costruito una replica a grandezza naturale del Titanic come attrazione turistica.",
        isReal: true,
        explanation: "Vero! Il progetto 'Romandisea' include una replica del Titanic in Sichuan.",
        difficulty: 2
    },
    {
        text: "Il WiFi 7 permetterà di scaricare un film in 4K in meno di un millisecondo.",
        isReal: false,
        explanation: "Esagerato! WiFi 7 sarà veloce, ma non così tanto da scaricare un film in un millisecondo.",
        difficulty: 2
    }
];

// Game State
let gameState = {
    score: 0,
    streak: 0,
    maxStreak: 0,
    currentQuestion: 0,
    correctAnswers: 0,
    wrongAnswers: 0,
    totalQuestions: 10,
    currentNews: null,
    isSpinning: false,
    usedNewsIndexes: []
};

// DOM Elements
const elements = {
    wheel: document.getElementById('wheel'),
    spinBtn: document.getElementById('spinBtn'),
    newsCard: document.getElementById('newsCard'),
    newsText: document.getElementById('newsText'),
    newsNumber: document.getElementById('newsNumber'),
    difficulty: document.getElementById('difficulty'),
    sourceInfo: document.getElementById('sourceInfo'),
    realBtn: document.getElementById('realBtn'),
    fakeBtn: document.getElementById('fakeBtn'),
    answerBtns: document.getElementById('answerBtns'),
    resultDisplay: document.getElementById('resultDisplay'),
    resultIcon: document.getElementById('resultIcon'),
    resultText: document.getElementById('resultText'),
    resultExplanation: document.getElementById('resultExplanation'),
    scoreDisplay: document.getElementById('score'),
    streakDisplay: document.getElementById('streak'),
    progressFill: document.getElementById('progressFill'),
    gameOverModal: document.getElementById('gameOverModal'),
    finalScore: document.getElementById('finalScore'),
    correctAnswersDisplay: document.getElementById('correctAnswers'),
    wrongAnswersDisplay: document.getElementById('wrongAnswers'),
    maxStreakDisplay: document.getElementById('maxStreak'),
    rankDisplay: document.getElementById('rankDisplay'),
    playAgainBtn: document.getElementById('playAgainBtn'),
    particles: document.getElementById('particles')
};

// Initialize Game
function initGame() {
    gameState = {
        score: 0,
        streak: 0,
        maxStreak: 0,
        currentQuestion: 0,
        correctAnswers: 0,
        wrongAnswers: 0,
        totalQuestions: 10,
        currentNews: null,
        isSpinning: false,
        usedNewsIndexes: []
    };
    
    updateUI();
    elements.spinBtn.disabled = false;
    elements.realBtn.disabled = true;
    elements.fakeBtn.disabled = true;
    elements.resultDisplay.classList.add('hidden');
    elements.gameOverModal.classList.add('hidden');
    elements.newsCard.classList.remove('correct', 'wrong');
    elements.newsText.textContent = "Premi \"GIRA LA RUOTA\" per iniziare il gioco!";
    elements.newsNumber.textContent = "1";
    elements.sourceInfo.textContent = "";
    updateDifficulty(0);
}

// Update UI Elements
function updateUI() {
    elements.scoreDisplay.textContent = gameState.score;
    elements.streakDisplay.textContent = gameState.streak;
    elements.progressFill.style.width = `${(gameState.currentQuestion / gameState.totalQuestions) * 100}%`;
}

// Update Difficulty Stars
function updateDifficulty(level) {
    const stars = elements.difficulty.querySelectorAll('.diff-star');
    stars.forEach((star, index) => {
        star.classList.toggle('active', index < level);
    });
    
    // Add more stars if needed
    while (elements.difficulty.children.length < 3) {
        const star = document.createElement('span');
        star.className = 'diff-star';
        star.textContent = '⭐';
        elements.difficulty.appendChild(star);
    }
}

// Get Random News
function getRandomNews() {
    const availableIndexes = newsData
        .map((_, index) => index)
        .filter(index => !gameState.usedNewsIndexes.includes(index));
    
    if (availableIndexes.length === 0) {
        gameState.usedNewsIndexes = [];
        return newsData[Math.floor(Math.random() * newsData.length)];
    }
    
    const randomIndex = availableIndexes[Math.floor(Math.random() * availableIndexes.length)];
    gameState.usedNewsIndexes.push(randomIndex);
    return newsData[randomIndex];
}

// Spin Wheel
let currentWheelRotation = 0;

function spinWheel() {
    if (gameState.isSpinning || gameState.currentQuestion >= gameState.totalQuestions) return;
    
    gameState.isSpinning = true;
    elements.spinBtn.disabled = true;
    elements.realBtn.disabled = true;
    elements.fakeBtn.disabled = true;
    elements.resultDisplay.classList.add('hidden');
    elements.newsCard.classList.remove('correct', 'wrong');
    
    // Random rotation (multiple full spins + random position)
    const spins = 5 + Math.random() * 3;
    const randomDegree = Math.random() * 360;
    const additionalRotation = spins * 360 + randomDegree;
    currentWheelRotation = (currentWheelRotation + additionalRotation) % 3600; // Keep rotation manageable
    
    // Play spin sound effect (visual feedback instead)
    elements.wheel.style.transition = `transform ${GAME_CONSTANTS.SPIN_DURATION}ms cubic-bezier(0.17, 0.67, 0.12, 0.99)`;
    elements.wheel.style.transform = `rotate(${currentWheelRotation}deg)`;
    
    // Create spinning particles
    createSpinParticles();
    
    // After spin completes
    setTimeout(() => {
        gameState.isSpinning = false;
        gameState.currentQuestion++;
        gameState.currentNews = getRandomNews();
        
        // Update news card
        elements.newsNumber.textContent = gameState.currentQuestion;
        elements.newsText.textContent = gameState.currentNews.text;
        updateDifficulty(gameState.currentNews.difficulty);
        
        // Enable answer buttons
        elements.realBtn.disabled = false;
        elements.fakeBtn.disabled = false;
        
        // Animate card
        elements.newsCard.style.animation = 'none';
        setTimeout(() => {
            elements.newsCard.style.animation = 'correctPulse 0.5s ease-out';
        }, 10);
        
        updateUI();
    }, GAME_CONSTANTS.SPIN_DURATION);
}

// Create Particles Effect
function createSpinParticles() {
    const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#38ef7d', '#ffd200'];
    
    for (let i = 0; i < 30; i++) {
        setTimeout(() => {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = `${50 + (Math.random() - 0.5) * 30}%`;
            particle.style.top = `${30 + (Math.random() - 0.5) * 20}%`;
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            particle.style.width = `${5 + Math.random() * 10}px`;
            particle.style.height = particle.style.width;
            elements.particles.appendChild(particle);
            
            setTimeout(() => particle.remove(), GAME_CONSTANTS.PARTICLE_LIFETIME);
        }, i * 50);
    }
}

// Create Celebration Particles
function createCelebrationParticles(isCorrect) {
    const colors = isCorrect 
        ? ['#11998e', '#38ef7d', '#00ff88', '#00cc6a']
        : ['#eb3349', '#f45c43', '#ff6b6b', '#ff4757'];
    
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${40 + Math.random() * 30}%`;
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            particle.style.width = `${5 + Math.random() * 15}px`;
            particle.style.height = particle.style.width;
            elements.particles.appendChild(particle);
            
            setTimeout(() => particle.remove(), GAME_CONSTANTS.PARTICLE_LIFETIME);
        }, i * 30);
    }
}

// Handle Answer
function handleAnswer(userAnswer) {
    if (!gameState.currentNews || gameState.isSpinning) return;
    
    const isCorrect = (userAnswer === 'real' && gameState.currentNews.isReal) ||
                     (userAnswer === 'fake' && !gameState.currentNews.isReal);
    
    // Disable buttons
    elements.realBtn.disabled = true;
    elements.fakeBtn.disabled = true;
    
    // Update game state
    if (isCorrect) {
        gameState.streak++;
        if (gameState.streak > gameState.maxStreak) {
            gameState.maxStreak = gameState.streak;
        }
        gameState.correctAnswers++;
        
        // Score calculation with streak bonus
        const baseScore = gameState.currentNews.difficulty * GAME_CONSTANTS.BASE_SCORE_MULTIPLIER;
        const streakBonus = Math.min(gameState.streak - 1, GAME_CONSTANTS.MAX_STREAK_BONUS) * GAME_CONSTANTS.STREAK_BONUS;
        gameState.score += baseScore + streakBonus;
        
        elements.newsCard.classList.add('correct');
        elements.resultIcon.textContent = '🎉';
        elements.resultText.textContent = 'CORRETTO!';
        elements.resultText.className = 'result-text correct';
        
        createCelebrationParticles(true);
    } else {
        gameState.streak = 0;
        gameState.wrongAnswers++;
        
        elements.newsCard.classList.add('wrong');
        elements.resultIcon.textContent = '😢';
        elements.resultText.textContent = 'SBAGLIATO!';
        elements.resultText.className = 'result-text wrong';
        
        createCelebrationParticles(false);
    }
    
    // Show explanation
    elements.resultExplanation.textContent = gameState.currentNews.explanation;
    elements.resultDisplay.classList.remove('hidden');
    elements.sourceInfo.textContent = gameState.currentNews.isReal ? '✓ Notizia Vera' : '✗ Notizia Falsa';
    
    updateUI();
    
    // Check if game is over
    if (gameState.currentQuestion >= gameState.totalQuestions) {
        setTimeout(showGameOver, GAME_CONSTANTS.GAME_OVER_DELAY);
    } else {
        // Enable spin button for next question
        setTimeout(() => {
            elements.spinBtn.disabled = false;
        }, GAME_CONSTANTS.NEXT_QUESTION_DELAY);
    }
}

// Show Game Over Modal
function showGameOver() {
    elements.gameOverModal.classList.remove('hidden');
    elements.finalScore.textContent = gameState.score;
    elements.correctAnswersDisplay.textContent = gameState.correctAnswers;
    elements.wrongAnswersDisplay.textContent = gameState.wrongAnswers;
    elements.maxStreakDisplay.textContent = gameState.maxStreak;
    
    // Calculate rank
    const percentage = (gameState.correctAnswers / gameState.totalQuestions) * 100;
    let rankIcon, rankText;
    
    if (percentage >= 90) {
        rankIcon = '🏆';
        rankText = 'MAESTRO DELLE NOTIZIE!';
    } else if (percentage >= 70) {
        rankIcon = '🥇';
        rankText = 'ESPERTO DI FAKE NEWS!';
    } else if (percentage >= 50) {
        rankIcon = '🥈';
        rankText = 'DETECTIVE IN TRAINING';
    } else if (percentage >= 30) {
        rankIcon = '🥉';
        rankText = 'PRINCIPIANTE';
    } else {
        rankIcon = '📰';
        rankText = 'HAI BISOGNO DI PRATICA!';
    }
    
    elements.rankDisplay.innerHTML = `
        <span class="rank-icon">${rankIcon}</span>
        <span class="rank-text">${rankText}</span>
    `;
    
    // Create final celebration
    for (let i = 0; i < 100; i++) {
        setTimeout(() => {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.backgroundColor = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#38ef7d', '#ffd200'][Math.floor(Math.random() * 6)];
            particle.style.width = `${5 + Math.random() * 15}px`;
            particle.style.height = particle.style.width;
            elements.particles.appendChild(particle);
            
            setTimeout(() => particle.remove(), 1500);
        }, i * 20);
    }
}

// Event Listeners
elements.spinBtn.addEventListener('click', spinWheel);
elements.realBtn.addEventListener('click', () => handleAnswer('real'));
elements.fakeBtn.addEventListener('click', () => handleAnswer('fake'));
elements.playAgainBtn.addEventListener('click', initGame);

// Keyboard Controls
document.addEventListener('keydown', (e) => {
    if (e.key === ' ' || e.key === 'Enter') {
        if (!elements.spinBtn.disabled) {
            e.preventDefault();
            spinWheel();
        }
    } else if (e.key === 'v' || e.key === 'V' || e.key === '1') {
        if (!elements.realBtn.disabled) {
            e.preventDefault();
            handleAnswer('real');
        }
    } else if (e.key === 'f' || e.key === 'F' || e.key === '2') {
        if (!elements.fakeBtn.disabled) {
            e.preventDefault();
            handleAnswer('fake');
        }
    }
});

// Initialize on load
document.addEventListener('DOMContentLoaded', initGame);
