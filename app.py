from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Happy Birthday, Cartoon! ❤️</title>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        :root {
            --primary: #ff4b72;
            --secondary: #ff85a2;
            --bg: #0f0c1b;
            --card-bg: rgba(255, 255, 255, 0.08);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Poppins', sans-serif;
        }

        body {
            background: linear-gradient(135deg, #0f0c1b, #2b102f, #1a0826);
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        /* Password Overlay Screen */
        #password-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #0f0c1b, #2b102f, #1a0826);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .pass-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 40px 30px;
            border-radius: 20px;
            text-align: center;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        }

        .pass-card h2 {
            font-family: 'Dancing Script', cursive;
            font-size: 2.2rem;
            color: var(--secondary);
            margin-bottom: 10px;
        }

        .pass-card p {
            font-size: 0.95rem;
            color: #ccc;
            margin-bottom: 20px;
        }

        .pass-input {
            width: 100%;
            padding: 12px 15px;
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            text-align: center;
            font-size: 1.2rem;
            letter-spacing: 3px;
            outline: none;
            margin-bottom: 15px;
        }

        .pass-input::placeholder {
            color: #aaa;
            letter-spacing: normal;
            font-size: 0.95rem;
        }

        .pass-error {
            color: #ff6b6b;
            font-size: 0.85rem;
            margin-top: 10px;
            display: none;
        }

        /* Floating Hearts Animation */
        .heart {
            position: fixed;
            color: var(--primary);
            font-size: 20px;
            pointer-events: none;
            animation: floatUp 6s linear infinite;
            z-index: 1;
        }

        @keyframes floatUp {
            0% { transform: translateY(100vh) scale(0.5); opacity: 1; }
            100% { transform: translateY(-10vh) scale(1.2); opacity: 0; }
        }

        header {
            text-align: center;
            padding: 50px 20px 20px;
            position: relative;
            z-index: 2;
        }

        h1 {
            font-family: 'Dancing Script', cursive;
            font-size: 3.5rem;
            color: #ff85a2;
            text-shadow: 0 0 15px rgba(255, 133, 162, 0.6);
        }

        p.subtitle {
            font-size: 1.2rem;
            opacity: 0.8;
            margin-top: 10px;
        }

        /* Countdown Container */
        .countdown-container {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            max-width: 600px;
            margin: 30px auto;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            position: relative;
            z-index: 2;
        }

        .countdown-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-top: 15px;
        }

        .time-box {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .time-box span {
            display: block;
            font-size: 2rem;
            font-weight: bold;
            color: var(--secondary);
        }

        /* Polaroid Gallery */
        .section-title {
            text-align: center;
            font-size: 2.2rem;
            margin: 50px 0 20px;
            font-family: 'Dancing Script', cursive;
            color: var(--secondary);
        }

        .gallery {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 25px;
            padding: 20px;
            max-width: 1100px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }

        .polaroid {
            background: #fff;
            padding: 15px 15px 25px;
            border-radius: 8px;
            color: #333;
            width: 270px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            transform: rotate(-2deg);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .polaroid:nth-child(even) {
            transform: rotate(2deg);
        }

        .polaroid:hover {
            transform: scale(1.08) rotate(0deg);
            z-index: 5;
        }

        .polaroid img {
            width: 100%;
            height: 320px;
            object-fit: cover;
            border-radius: 4px;
        }

        .polaroid p {
            text-align: center;
            margin-top: 12px;
            font-family: 'Dancing Script', cursive;
            font-size: 1.4rem;
            color: #444;
        }

        /* Cake Section */
        .cake-container {
            text-align: center;
            margin: 50px auto;
            position: relative;
            z-index: 2;
        }

        .cake {
            width: 200px;
            height: 140px;
            background: #f48fb1;
            margin: 60px auto 20px;
            border-radius: 10px 10px 0 0;
            position: relative;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }

        .cake::before {
            content: '';
            position: absolute;
            top: -30px;
            left: 0;
            width: 200px;
            height: 30px;
            background: #ce93d8;
            border-radius: 10px 10px 0 0;
        }

        .candle {
            width: 12px;
            height: 45px;
            background: #fff;
            position: absolute;
            top: -75px;
            left: 94px;
            border-radius: 3px;
        }

        .flame {
            width: 16px;
            height: 24px;
            background: orange;
            border-radius: 50% 50% 20% 20%;
            position: absolute;
            top: -24px;
            left: -2px;
            box-shadow: 0 0 15px orange;
            animation: flicker 0.6s infinite alternate;
            cursor: pointer;
        }

        @keyframes flicker {
            0% { transform: scale(1); }
            100% { transform: scale(1.15); }
        }

        .btn {
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            border: none;
            padding: 12px 30px;
            color: white;
            font-size: 1rem;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(255, 75, 114, 0.4);
            transition: transform 0.2s;
            margin: 10px;
        }

        .btn:hover {
            transform: scale(1.05);
        }

        /* Quiz Container */
        .quiz-container {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            max-width: 600px;
            margin: 40px auto;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            z-index: 2;
        }

        .quiz-option {
            background: rgba(255, 255, 255, 0.1);
            margin: 10px 0;
            padding: 12px;
            border-radius: 10px;
            cursor: pointer;
            transition: background 0.3s;
        }

        .quiz-option:hover {
            background: var(--primary);
        }

        /* Modal Love Letter */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(5px);
            z-index: 10;
            justify-content: center;
            align-items: center;
        }

        .modal-content {
            background: #fff;
            color: #333;
            max-width: 500px;
            padding: 35px;
            border-radius: 15px;
            text-align: center;
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .modal-content h2 {
            font-family: 'Dancing Script', cursive;
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 15px;
        }

        .close-btn {
            position: absolute;
            top: 15px;
            right: 20px;
            font-size: 1.5rem;
            cursor: pointer;
            color: #888;
        }
    </style>
</head>
<body>

    <!-- Password Screen -->
    <div id="password-screen">
        <div class="pass-card">
            <h2>Welcome Cartoon! 🔒</h2>
            <p>Enter the secret passcode to unlock your birthday surprise:</p>
            <input type="password" id="passInput" class="pass-input" placeholder="Enter Code" maxlength="6" onkeydown="if(event.key === 'Enter') checkPassword()">
            <button class="btn" onclick="checkPassword()">Unlock ❤️</button>
            <div id="passError" class="pass-error">Incorrect passcode! Hint: Date & Year 😉</div>
        </div>
    </div>

    <!-- Floating Background Hearts -->
    <div id="hearts-container"></div>

    <header>
        <h1>Advance Happy Birthday, Srashti! 💕</h1>
        <p class="subtitle">To my favorite <strong>Cartoon</strong> 🎨 | DOB: Nov 6, 2008</p>
    </header>

    <!-- Countdown Timer -->
    <div class="countdown-container">
        <h3>Countdown to Her Special Day ✨</h3>
        <div class="countdown-grid">
            <div class="time-box"><span id="days">00</span>Days</div>
            <div class="time-box"><span id="hours">00</span>Hours</div>
            <div class="time-box"><span id="minutes">00</span>Mins</div>
            <div class="time-box"><span id="seconds">00</span>Secs</div>
        </div>
    </div>

    <!-- Gallery with Srashti's Photos -->
    <h2 class="section-title">Precious Moments of Srashti</h2>
    <div class="gallery">
        <div class="polaroid">
            <img src="{{ url_for('static', filename='srashti1.jpg') }}" alt="Srashti Photo 1">
            <p>My Cute Cartoon 😊</p>
        </div>
        <div class="polaroid">
            <img src="{{ url_for('static', filename='srashti2.jpg') }}" alt="Srashti Photo 2">
            <p>Those Expressive Eyes ✨</p>
        </div>
        <div class="polaroid">
            <img src="{{ url_for('static', filename='srashti3.jpg') }}" alt="Srashti Photo 3">
            <p>Traditional Vibe ❤️</p>
        </div>
        <div class="polaroid">
            <img src="{{ url_for('static', filename='srashti4.jpg') }}" alt="Srashti Photo 4">
            <p>Gorgeous Smile 💖</p>
        </div>
        <div class="polaroid">
            <img src="{{ url_for('static', filename='srashti5.jpg') }}" alt="Srashti Photo 5">
            <p>Desi Girl Avatar 🌺</p>
        </div>
        <div class="polaroid">
            <img src="{{ url_for('static', filename='srashti6.jpg') }}" alt="Srashti Photo 6">
            <p>Sunshine Smile ☀️</p>
        </div>
    </div>

    <!-- Virtual Cake Cutting -->
    <div class="cake-container">
        <h2 class="section-title">Blow Candle & Cut Cake</h2>
        <div class="cake">
            <div class="candle">
                <div class="flame" id="flame" onclick="blowCandle()"></div>
            </div>
        </div>
        <button class="btn" onclick="cutCake()">Cut the Birthday Cake 🎂</button>
    </div>

    <!-- Love Quiz -->
    <div class="quiz-container">
        <h2 style="font-family: 'Dancing Script', cursive; font-size: 2rem; color: var(--secondary);">Quick Love Quiz</h2>
        <div id="quiz">
            <p id="quiz-question" style="margin: 15px 0; font-size: 1.1rem;"></p>
            <div id="quiz-options"></div>
        </div>
    </div>

    <!-- Secret Love Letter Button -->
    <div style="text-align: center; margin-bottom: 50px;">
        <button class="btn" onclick="openLetter()">Open Secret Love Letter 💌</button>
    </div>

    <!-- Love Letter Modal -->
    <div class="modal" id="letterModal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeLetter()">&times;</span>
            <h2>Dear Srashti (Cartoon) 💖</h2>
            <p style="line-height: 1.8; font-size: 1rem;">
                Wishing you a very happy birthday in advance! You bring so much joy, light, and laughter into my life. Calling you "Cartoon" is my favorite thing because you are as cute, funny, and unique as one! May your year ahead be filled with happiness, endless smiles, and all your dreams coming true.
            </p>
            <p style="margin-top: 15px; font-weight: bold; color: var(--primary);">Always yours ❤️</p>
        </div>
    </div>

    <script>
        // Password Protection Verification
        function checkPassword() {
            const passInput = document.getElementById('passInput').value;
            const passError = document.getElementById('passError');
            
            if (passInput === '062008') {
                document.getElementById('password-screen').style.display = 'none';
                confetti({ particleCount: 120, spread: 80 });
            } else {
                passError.style.display = 'block';
            }
        }

        // Floating Hearts Logic
        function createHeart() {
            const heart = document.createElement('div');
            heart.classList.add('heart');
            heart.innerHTML = '❤️';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.animationDuration = Math.random() * 3 + 3 + 's';
            document.getElementById('hearts-container').appendChild(heart);
            setTimeout(() => heart.remove(), 6000);
        }
        setInterval(createHeart, 400);

        // Dynamic Countdown Logic
        function updateCountdown() {
            const now = new Date();
            let birthYear = now.getFullYear();
            let targetDate = new Date(`November 6, ${birthYear} 00:00:00`);

            if (now > targetDate) {
                targetDate = new Date(`November 6, ${birthYear + 1} 00:00:00`);
            }

            const diff = targetDate - now;

            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
            const minutes = Math.floor((diff / 1000 / 60) % 60);
            const seconds = Math.floor((diff / 1000) % 60);

            document.getElementById('days').innerText = String(days).padStart(2, '0');
            document.getElementById('hours').innerText = String(hours).padStart(2, '0');
            document.getElementById('minutes').innerText = String(minutes).padStart(2, '0');
            document.getElementById('seconds').innerText = String(seconds).padStart(2, '0');
        }
        setInterval(updateCountdown, 1000);
        updateCountdown();

        // Candle Blow Out & Confetti Logic
        function blowCandle() {
            document.getElementById('flame').style.display = 'none';
            alert("Candle blown out! Make a wish, Srashti! ✨");
        }

        function cutCake() {
            confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.6 }
            });
            alert("🎉 Happy Birthday Cake Cut! Sending virtual sweet bites! 🍰");
        }

        // Quiz Interactive System
        const quizData = [
            {
                question: "What is her special nickname?",
                options: ["Angel", "Cartoon", "Princess", "Sunshine"],
                answer: 1
            },
            {
                question: "What is Srashti's Date of Birth?",
                options: ["06-11-2008", "01-01-2008", "12-10-2008", "06-05-2008"],
                answer: 0
            }
        ];

        let currentQuizIndex = 0;

        function loadQuiz() {
            const currentQuiz = quizData[currentQuizIndex];
            document.getElementById('quiz-question').innerText = currentQuiz.question;
            const optionsContainer = document.getElementById('quiz-options');
            optionsContainer.innerHTML = '';

            currentQuiz.options.forEach((option, idx) => {
                const btn = document.createElement('div');
                btn.classList.add('quiz-option');
                btn.innerText = option;
                btn.onclick = () => selectOption(idx);
                optionsContainer.appendChild(btn);
            });
        }

        function selectOption(index) {
            if (index === quizData[currentQuizIndex].answer) {
                alert("Correct! ❤️ You know her so well!");
            } else {
                alert("Oops! Try again 😊");
            }
            currentQuizIndex = (currentQuizIndex + 1) % quizData.length;
            loadQuiz();
        }

        loadQuiz();

        // Modal Logic
        function openLetter() {
            document.getElementById('letterModal').style.display = 'flex';
            confetti({ particleCount: 100, spread: 60 });
        }

        function closeLetter() {
            document.getElementById('letterModal').style.display = 'none';
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    print("Launching Srashti's Birthday Website at http://127.0.0.1:5000")
    app.run(debug=True)