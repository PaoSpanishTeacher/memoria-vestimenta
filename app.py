import streamlit as st
import streamlit.components.v1 as components

# Configuración de página
st.set_page_config(page_title="Memoria - La Vestimenta", layout="wide")

# Estilo para limpiar el contenedor de Streamlit
st.markdown("""
    <style>
    .block-container { padding: 0rem; }
    iframe { border: none; }
    </style>
    """, unsafe_allow_html=True)

# Código completo del juego
html_vestimenta = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Quicksand:wght@500;700&family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #ff4d6d;
            --secondary: #4cc9f0;
            --accent: #fee440;
            --text-dark: #2b2d42;
            --card-back: #7209b7;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }

        body {
            font-family: 'Quicksand', sans-serif;
            min-height: 100vh;
            background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), 
                        url('https://img.freepik.com/free-vector/walk-closet-cartoon-interior-with-clothes_107791-2465.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px;
        }

        header { text-align: center; margin: 10px 0; z-index: 10; }
        h1 { font-family: 'Fredoka', sans-serif; font-size: 2.8rem; color: var(--primary); text-shadow: 3px 3px 0px white; }
        .brand-name { font-family: 'Dancing Script', cursive; font-size: 1.6rem; color: var(--text-dark); margin-top: -5px; }

        .game-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            width: 100%;
            max-width: 800px;
            perspective: 1000px;
            margin-top: 10px;
        }

        .card {
            aspect-ratio: 1/1.2;
            cursor: pointer;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card:hover:not(.flipped) { transform: translateY(-5px) scale(1.03); }
        .card.flipped { transform: rotateY(180deg); }

        .card-face {
            position: absolute;
            width: 100%; height: 100%;
            backface-visibility: hidden;
            border-radius: 15px;
            border: 4px solid white;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        .card-back {
            background: var(--secondary);
            background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40"><path d="M20 10v20M10 20h20" stroke="white" stroke-width="2" opacity="0.3" fill="none"/></svg>');
        }
        .card-back::after { content: "🛍️"; font-size: 3rem; filter: drop-shadow(2px 2px 0px rgba(0,0,0,0.1)); }

        .card-front { background: #fff9fb; transform: rotateY(180deg); padding: 10px; }
        .card-word { font-family: 'Fredoka', sans-serif; font-size: 1.3rem; color: var(--primary); font-weight: 600; text-transform: uppercase; text-align: center; }
        .card-image { font-size: 4.5rem; filter: drop-shadow(0 4px 4px rgba(0,0,0,0.1)); }

        #feedback-msg {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0);
            font-family: 'Fredoka', sans-serif; font-size: 4rem; color: white;
            text-shadow: 0 0 15px rgba(0,0,0,0.3), 4px 4px 0 var(--primary); 
            z-index: 100; pointer-events: none;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #feedback-msg.show { transform: translate(-50%, -50%) scale(1); animation: starPop 1s forwards; }
        @keyframes starPop { 0% { opacity: 1; } 80% { opacity: 1; } 100% { opacity: 0; transform: translate(-50%, -65%) scale(1.2); } }

        .watermark {
            position: fixed; bottom: 10px; right: 20px;
            font-size: 0.9rem; color: rgba(0, 0, 0, 0.2);
            font-family: 'Dancing Script', cursive; font-weight: bold;
        }

        #victory-screen {
            position: fixed; inset: 0; background: rgba(255, 77, 109, 0.97);
            display: none; flex-direction: column; justify-content: center;
            align-items: center; z-index: 2000; text-align: center; color: white; padding: 20px;
        }

        .profesor { font-size: 8rem; animation: float 3s infinite ease-in-out; margin-bottom: 10px; }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }

        .btn-restart {
            background: var(--accent); color: var(--text-dark); border: none;
            padding: 15px 40px; font-size: 1.8rem; font-family: 'Fredoka', sans-serif;
            border-radius: 50px; cursor: pointer; box-shadow: 0 6px 0 #d4bd00; margin-top: 20px;
            transition: transform 0.1s;
        }
        .btn-restart:active { transform: translateY(4px); box-shadow: 0 2px 0 #d4bd00; }

        .balloon { position: absolute; bottom: -100px; animation: up 6s linear forwards; font-size: 3rem; z-index: 2001; }
        @keyframes up { to { transform: translateY(-120vh) rotate(20deg); } }
    </style>
</head>
<body>

    <header>
        <h1>Memoria - La Vestimenta</h1>
        <div class="brand-name">PaoSpanishTeacher</div>
    </header>

    <div class="game-container" id="board"></div>
    <div id="feedback-msg">¡Excelente! ⭐</div>
    <div class="watermark">PaoSpanishTeacher</div>

    <div id="victory-screen">
        <div class="profesor">👨‍🏫</div>
        <h2 style="font-size: 2.2rem; margin-bottom: 10px;">¡Felicidades!</h2>
        <p style="font-size: 1.4rem;">Has completado la memoria de la vestimenta.</p>
        <p style="margin-top: 15px; font-weight: bold; opacity: 0.9;">Juego creado por PaoSpanishTeacher</p>
        <button class="btn-restart" id="restart-btn">Jugar otra vez</button>
    </div>

    <audio id="sfx-hit" src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>
    <audio id="sfx-error" src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>
    <audio id="sfx-win" src="https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3"></audio>

    <script>
        const CLOTHES = [
            { w: "Camisa", i: "👔" }, { w: "Pantalón", i: "👖" },
            { w: "Vestido", i: "👗" }, { w: "Falda", i: "👗" },
            { w: "Zapatos", i: "👟" }, { w: "Chaqueta", i: "🧥" },
            { w: "Sombrero", i: "👒" }, { w: "Camiseta", i: "👕" },
            { w: "Abrigo", i: "🧥" }, { w: "Corbata", i: "👔" }
        ];

        // Ajuste manual de iconos para evitar duplicados visuales si el sistema lo requiere
        const DATA = [
            {w: "Camisa", i: "👔"}, {w: "Pantalón", i: "👖"}, {w: "Vestido", i: "👗"},
            {w: "Falda", i: "👗"}, {w: "Zapatos", i: "👞"}, {w: "Chaqueta", i: "🧥"},
            {w: "Sombrero", i: "👒"}, {w: "Camiseta", i: "👕"}, {w: "Abrigo", i: "🧥"},
            {w: "Corbata", i: "👔"}
        ];

        let flippedCards = [];
        let matchedCount = 0;
        let isLock = false;

        function shuffle(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        }

        function createBoard() {
            const board = document.getElementById('board');
            board.innerHTML = '';
            let deck = [];
            
            DATA.forEach(item => {
                deck.push({ type: 'word', value: item.w, pairId: item.w });
                deck.push({ type: 'img', value: item.i, pairId: item.w });
            });

            shuffle(deck);

            deck.forEach(data => {
                const card = document.createElement('div');
                card.className = 'card';
                card.dataset.pairId = data.pairId;
                
                card.innerHTML = `
                    <div class="card-face card-back"></div>
                    <div class="card-face card-front">
                        ${data.type === 'word' 
                            ? `<div class="card-word">${data.value}</div>` 
                            : `<div class="card-image">${data.value}</div>`}
                    </div>
                `;
                
                card.onclick = () => handleFlip(card);
                board.appendChild(card);
            });
        }

        function handleFlip(card) {
            if (isLock || card.classList.contains('flipped') || flippedCards.includes(card)) return;

            card.classList.add('flipped');
            flippedCards.push(card);

            if (flippedCards.length === 2) {
                checkMatch();
            }
        }

        function checkMatch() {
            isLock = true;
            const [c1, c2] = flippedCards;
            const isMatch = c1.dataset.pairId === c2.dataset.pairId;

            if (isMatch) {
                matchedCount++;
                document.getElementById('sfx-hit').play().catch(()=>{});
                showFeedback();
                flippedCards = [];
                isLock = false;
                if (matchedCount === DATA.length) endGame();
            } else {
                document.getElementById('sfx-error').play().catch(()=>{});
                setTimeout(() => {
                    c1.classList.remove('flipped');
                    c2.classList.remove('flipped');
                    flippedCards = [];
                    isLock = false;
                }, 1200);
            }
        }

        function showFeedback() {
            const msg = document.getElementById('feedback-msg');
            msg.classList.add('show');
            setTimeout(() => msg.classList.remove('show'), 1000);
        }

        function endGame() {
            const winSfx = document.getElementById('sfx-win');
            winSfx.currentTime = 0;
            winSfx.play().catch(()=>{});

            document.getElementById('victory-screen').style.display = 'flex';
            
            confetti({ particleCount: 200, spread: 80, origin: { y: 0.6 } });
            
            // Globos
            for(let i=0; i<15; i++) {
                setTimeout(() => {
                    const b = document.createElement('div');
                    b.className = 'balloon';
                    b.innerHTML = ['🎈', '✨', '👗', '🧥'][Math.floor(Math.random()*4)];
                    b.style.left = Math.random() * 90 + 'vw';
                    document.body.appendChild(b);
                    setTimeout(() => b.remove(), 6000);
                }, i * 300);
            }

            // Voz
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance("Adelante, sigue avanzando en tu español.");
                utterance.lang = 'es-ES';
                window.speechSynthesis.speak(utterance);
            }
        }

        document.getElementById('restart-btn').onclick = () => {
            const winSfx = document.getElementById('sfx-win');
            winSfx.pause();
            document.getElementById('victory-screen').style.display = 'none';
            matchedCount = 0;
            createBoard();
        };

        createBoard();
    </script>
</body>
</html>
"""

# Renderizar el componente HTML
components.html(html_vestimenta, height=900, scrolling=False)
