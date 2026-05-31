import streamlit as st

# Configure the Streamlit page to be completely wide and seamless
st.set_page_config(
    page_title="Coded Archives - Interactive Cinematic Console",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom injection to completely strip down Streamlit's default padding, margins, headers and bars
st.markdown("""
    <style>
        /* Hide default header, footer and margins */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
        div[data-testid="stToolbar"] {display: none !important;}
        
        /* Smooth scrolling across the app */
        html {
            scroll-behavior: smooth;
            background-color: #030308;
        }
        body {
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            background-color: #030308;
            font-family: 'Inter', system-ui, sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Main Web Component containing HTML, CSS, Canvas Logic and Layout Architecture
portfolio_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Coded Archives</title>
    <!-- Importing sleek futuristic typography -->
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;600&display=swap" rel="stylesheet">
    
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body, html {
            width: 100%;
            height: 100%;
            background-color: #020205;
            color: #ffffff;
            font-family: 'Space Grotesk', sans-serif;
            overflow-x: hidden;
        }

        /* --- STAGE 1: THE REEL COUNTDOWN LOADER --- */
        #loader-screen {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #020205;
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            transition: opacity 1s cubic-bezier(0.76, 0, 0.24, 1), visibility 1s;
        }
        .ring-container {
            position: relative;
            width: 120px;
            height: 120px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .progress-ring {
            transform: rotate(-90deg);
        }
        .progress-ring__circle {
            stroke: #ff1f44; /* Neon Crimson */
            stroke-dasharray: 314;
            stroke-dashoffset: 314;
            transition: stroke-dashoffset 0.05s linear;
            filter: drop-shadow(0 0 8px #ff1f44);
        }
        .progress-ring__bg {
            stroke: rgba(0, 191, 255, 0.1); /* Soft Blue Shadow */
        }
        #countdown-text {
            position: absolute;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: #00d2ff; /* Neon Blue text */
            text-shadow: 0 0 10px rgba(0, 210, 255, 0.6);
        }

        /* --- GLOBAL BACKGROUND CANVAS --- */
        #canvas-container {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: 1;
            pointer-events: none;
        }

        /* --- NAVIGATION HEADER --- */
        .nav-header {
            position: fixed;
            top: 0; left: 0; width: 100%;
            padding: 30px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
            mix-blend-mode: difference;
        }
        .logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            font-weight: 900;
            letter-spacing: 4px;
            color: #00d2ff;
            text-shadow: 0 0 8px rgba(0, 210, 255, 0.4);
            text-transform: uppercase;
        }
        .nav-btn {
            padding: 10px 24px;
            border: 1px solid rgba(255, 31, 68, 0.4);
            background: rgba(255, 31, 68, 0.05);
            color: #ffffff;
            border-radius: 50px;
            cursor: pointer;
            font-weight: 600;
            letter-spacing: 1px;
            font-size: 0.85rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }
        .nav-btn:hover {
            border-color: #00d2ff;
            background: rgba(0, 210, 255, 0.1);
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
            transform: translateY(-2px);
        }

        /* --- CONTAINER SCROLL LAYOUT --- */
        .scroll-container {
            position: relative;
            z-index: 2;
            width: 100%;
        }
        .page-section {
            position: relative;
            width: 100%;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 100px 10%;
        }

        /* --- STAGE 2: HERO SWIRLING GALAXY SCREEN --- */
        #hero-section {
            flex-direction: column;
            text-align: center;
            justify-content: center;
        }
        .hero-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 5rem;
            font-weight: 900;
            letter-spacing: 14px;
            text-transform: uppercase;
            background: linear-gradient(135deg, #ffffff 30%, #00d2ff 70%, #ff1f44 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            filter: drop-shadow(0 0 30px rgba(0,210,255,0.15));
            animation: pulseGlow 4s infinite alternate;
        }
        .hero-subtitle {
            font-size: 1.1rem;
            letter-spacing: 4px;
            color: rgba(255, 255, 255, 0.6);
            max-width: 600px;
            margin: 0 auto 40px auto;
            line-height: 1.8;
        }
        .scroll-hint {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.8rem;
            letter-spacing: 6px;
            color: #ff1f44;
            text-transform: uppercase;
            margin-top: 20px;
            opacity: 0.8;
            animation: bounce 2s infinite;
        }

        /* --- STAGE 3: INTERACTIVE PLANET MAP (HOVER HOTSPOTS) --- */
        #planet-section {
            flex-direction: column;
            justify-content: center;
        }
        .section-header {
            text-align: center;
            margin-bottom: 60px;
        }
        .section-header h2 {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            letter-spacing: 8px;
            color: #ffffff;
            margin-bottom: 10px;
        }
        .section-header p {
            color: #00d2ff;
            letter-spacing: 2px;
            font-size: 0.9rem;
        }
        .interactive-node-container {
            position: relative;
            width: 600px;
            height: 600px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        /* Holographic Central Planet ring */
        .planet-core {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255,31,68,0.2) 0%, rgba(0,210,255,0.05) 70%, transparent 100%);
            border: 1px dashed rgba(0, 210, 255, 0.3);
            position: relative;
            animation: spin 20s linear infinite;
        }
        /* Hotspot Pins Orbiting */
        .hotspot {
            position: absolute;
            width: 20px;
            height: 20px;
            cursor: pointer;
            z-index: 10;
        }
        .hotspot-trigger {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: #ff1f44;
            border: 4px solid #020205;
            box-shadow: 0 0 10px #ff1f44;
            transition: all 0.3s ease;
        }
        .hotspot:hover .hotspot-trigger {
            background: #00d2ff;
            box-shadow: 0 0 20px #00d2ff;
            transform: scale(1.3);
        }
        /* Reveal-on-hover info boxes */
        .hotspot-info {
            position: absolute;
            bottom: 35px;
            left: 50%;
            transform: translateX(-50%) translateY(10px);
            width: 260px;
            background: rgba(3, 3, 8, 0.85);
            border: 1px solid rgba(0, 210, 255, 0.3);
            padding: 20px;
            border-radius: 8px;
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .hotspot:hover .hotspot-info {
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) translateY(0);
        }
        .hotspot-info h4 {
            font-family: 'Orbitron', sans-serif;
            color: #00d2ff;
            font-size: 1rem;
            margin-bottom: 6px;
            letter-spacing: 1px;
        }
        .hotspot-info p {
            font-size: 0.85rem;
            color: rgba(255,255,255,0.7);
            line-height: 1.5;
        }
        /* Specific layouts of points inside the orbit map */
        #node1 { top: 15%; left: 50%; }
        #node2 { top: 45%; left: 10%; }
        #node3 { top: 45%; right: 10%; }
        #node4 { bottom: 15%; left: 30%; }
        #node5 { bottom: 15%; right: 30%; }

        /* --- STAGE 4: STRAND HORIZONTAL OVERLAYS --- */
        #strand-section {
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
        }
        .strand-card {
            width: 100%;
            max-width: 900px;
            border-left: 3px solid #ff1f44;
            background: linear-gradient(90deg, rgba(255,31,68,0.03) 0%, transparent 100%);
            padding: 40px;
            margin-bottom: 30px;
            backdrop-filter: blur(2px);
            transition: all 0.4s ease;
        }
        .strand-card:hover {
            border-left-color: #00d2ff;
            background: linear-gradient(90deg, rgba(0,210,255,0.05) 0%, transparent 100%);
            transform: translateX(15px);
        }
        .strand-meta {
            font-family: 'Orbitron', sans-serif;
            color: #ff1f44;
            font-size: 0.8rem;
            letter-spacing: 3px;
            margin-bottom: 10px;
        }
        .strand-card h3 {
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }
        .strand-card p {
            color: rgba(255,255,255,0.6);
            line-height: 1.7;
            max-width: 750px;
        }

        /* --- STAGE 5: LINE AND CONTACT INTERFACE --- */
        #contact-section {
            flex-direction: column;
            height: 100vh;
            justify-content: space-between;
            padding-bottom: 60px;
        }
        .footer-line {
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, #ff1f44 30%, #00d2ff 70%, transparent 100%);
            margin-top: auto;
            margin-bottom: 60px;
            box-shadow: 0 0 10px rgba(0,210,255,0.5);
        }
        .contact-wrap {
            text-align: center;
            max-width: 600px;
            margin: 0 auto;
        }
        .contact-wrap h2 {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            letter-spacing: 6px;
            margin-bottom: 20px;
        }
        .contact-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 40px;
        }
        .info-block {
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.05);
            background: rgba(255,255,255,0.01);
            border-radius: 4px;
        }
        .info-block span {
            display: block;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.75rem;
            color: #00d2ff;
            letter-spacing: 2px;
            margin-bottom: 5px;
        }
        .info-block p {
            font-size: 1.1rem;
            color: #ffffff;
        }

        /* Animations */
        @keyframes pulseGlow {
            0% { filter: drop-shadow(0 0 20px rgba(0,210,255,0.1)); }
            100% { filter: drop-shadow(0 0 40px rgba(255,31,68,0.3)); }
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        @keyframes spin {
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

    <!-- STAGE 1: COUNTDOWN INTERFACE -->
    <div id="loader-screen">
        <div class="ring-container">
            <svg class="progress-ring" width="110" height="110">
                <circle class="progress-ring__bg" stroke-width="4" fill="transparent" r="50" cx="55" cy="55"/>
                <circle class="progress-ring__circle" stroke-width="4" fill="transparent" r="50" cx="55" cy="55"/>
            </svg>
            <div id="countdown-text">0%</div>
        </div>
    </div>

    <!-- BACKGROUND ENGINE -->
    <div id="canvas-container">
        <canvas id="cosmic-canvas"></canvas>
    </div>

    <!-- PERSISTENT TOP UTILITY BAR -->
    <header class="nav-header">
        <div class="logo">Coded Archives</div>
        <button class="nav-btn" onclick="document.getElementById('contact-section').scrollIntoView();">INITIATE ENQUIRY</button>
    </header>

    <div class="scroll-container">
        
        <!-- STAGE 2: THE SWIRLING HERO GALAXY -->
        <section class="page-section" id="hero-section">
            <h1 class="hero-title">Coded Archives</h1>
            <p class,="hero-subtitle">An adaptive interactive system managing spatial data flows across complex node environments.</p>
            <div class="scroll-hint">SCROLL TO ENTER</div>
        </section>

        <!-- STAGE 3: INTERACTIVE PLANET NODES (HOVER ENGINE) -->
        <section class="page-section" id="planet-section">
            <div class="section-header">
                <h2>SYSTEM INFRASTRUCTURE</h2>
                <p>Hover over coordinates to query live node sub-matrices</p>
            </div>

            <div class="interactive-node-container">
                <div class="planet-core"></div>
                
                <!-- Hotspot 1 -->
                <div class="hotspot" id="node1">
                    <div class="hotspot-trigger"></div>
                    <div class="hotspot-info">
                        <h4>DISCOVERY APEX</h4>
                        <p>Deep cluster exploration mapping high-density vector anomalies across cosmic configurations.</p>
                    </div>
                </div>

                <!-- Hotspot 2 -->
                <div class="hotspot" id="node2">
                    <div class="hotspot-trigger"></div>
                    <div class="hotspot-info">
                        <h4>CONSOLE SUB-STATION</h4>
                        <p>Real-time telemetry and operation tracking layout engines updated sub-second.</p>
                    </div>
                </div>

                <!-- Hotspot 3 -->
                <div class="hotspot" id="node3">
                    <div class="hotspot-trigger"></div>
                    <div class="hotspot-info">
                        <h4>SYSTEM OVERSEER</h4>
                        <p>Automated diagnostic engine keeping cluster thresholds running within parameters.</p>
                    </div>
                </div>

                <!-- Hotspot 4 -->
                <div class="hotspot" id="node4">
                    <div class="hotspot-trigger"></div>
                    <div class="hotspot-info">
                        <h4>ROADMAP ARCHIVE</h4>
                        <p>Chronological phase scheduling documentation outlining systemic evolutionary paths.</p>
                    </div>
                </div>

                <!-- Hotspot 5 -->
                <div class="hotspot" id="node5">
                    <div class="hotspot-trigger"></div>
                    <div class="hotspot-info">
                        <h4>OUTCOME SYNAPSE</h4>
                        <p>Final transactional payload execution terminals serving consumer edge points.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- STAGE 4: STRAND SPECIFICATIONS -->
        <section class="page-section" id="strand-section">
            <div class="strand-card">
                <div class="strand-meta">MODULE // 01</div>
                <h3>Three views. One architecture. One system.</h3>
                <p>Isolating runtime variations through custom micro-engines allows seamless orchestration. Complex clusters process multi-variant datasets smoothly without presentation-tier blocking.</p>
            </div>

            <div class="strand-card">
                <div class="strand-meta">MODULE // 02</div>
                <h3>Advanced Cosmic Telemetry Rendering</h3>
                <p>Leveraging processing loops directly within browser instances cuts calculation overhead. Complex interactive environments can run alongside responsive system data tracks seamlessly.</p>
            </div>
        </section>

        <!-- STAGE 5: REVEAL LINE AND ENQUIRY CONTACT FOOTER -->
        <section class="page-section" id="contact-section">
            <div class="footer-line"></div>
            
            <div class="contact-wrap">
                <h2>PROJECT INQUIRIES</h2>
                <p style="color: rgba(255,255,255,0.5); letter-spacing: 1px;">Establish communication links with our development operators.</p>
                
                <div class="contact-grid">
                    <div class="info-block">
                        <span>SECURE TERMINAL</span>
                        <p>ops@coded-archives.io</p>
                    </div>
                    <div class="info-block">
                        <span>QUANTUM COMMS</span>
                        <p>+1 (800) 555-CODE</p>
                    </div>
                </div>
            </div>
        </section>

    </div>

    <!-- MATH/GL PARTICLES ENGINE ENGINE -->
    <script>
        // Progress Loader Control Animation Logic
        const circle = document.querySelector('.progress-ring__circle');
        const radius = circle.r.baseVal.value;
        const circumference = radius * 2 * Math.PI;
        const countdownText = document.getElementById('countdown-text');
        const loaderScreen = document.getElementById('loader-screen');

        circle.style.strokeDasharray = `${circumference} ${circumference}`;
        circle.style.strokeDashoffset = circumference;

        let progress = 0;
        const interval = setInterval(() => {
            progress += 1;
            const offset = circumference - (progress / 100) * circumference;
            circle.style.strokeDashoffset = offset;
            countdownText.innerText = progress + '%';

            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(() => {
                    loaderScreen.style.opacity = '0';
                    loaderScreen.style.visibility = 'hidden';
                }, 500);
            }
        }, 35); // Smooth mock load time

        // Canvas Particle Galaxy Rendering Loop Engine (WebGL style HTML5 context fallback)
        const canvas = document.getElementById('cosmic-canvas');
        const ctx = canvas.getContext('2d');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        const particles = [];
        const particleCount = 1400;
        
        // Define cosmic particle attributes mixing Red and Blue colors
        for (let i = 0; i < particleCount; i++) {
            const angle = Math.random() * Math.PI * 2;
            // Distribute along arm spirals
            const armOffset = (Math.floor(Math.random() * 3) * (2 * Math.PI / 3));
            const distance = Math.pow(Math.random(), 2) * (width * 0.35) + 10;
            
            // Alternating neon cluster colors
            const colorType = Math.random();
            let color = 'rgba(0, 210, 255, ' + (Math.random() * 0.6 + 0.2) + ')'; // Neon Blue
            if (colorType > 0.6) {
                color = 'rgba(255, 31, 68, ' + (Math.random() * 0.7 + 0.3) + ')'; // Neon Crimson Red
            } else if (colorType > 0.45) {
                color = 'rgba(255, 255, 255, ' + (Math.random() * 0.4 + 0.1) + ')'; // Ambient Star Dust
            }

            particles.push({
                baseAngle: angle + armOffset,
                distance: distance,
                speed: (0.01 + (1 / distance) * 0.5),
                size: Math.random() * 1.5 + 0.5,
                color: color,
                // Add minor random floating perturbation
                seedY: Math.random() * 100
            });
        }

        // Kinetic Scroll Factor Capture
        let scrollY = 0;
        window.addEventListener('scroll', () => {
            scrollY = window.scrollY;
        });

        function animate() {
            ctx.fillStyle = 'rgba(2, 2, 5, 0.12)'; // Deep space motion persistence trail
            ctx.fillRect(0, 0, width, height);

            // Shift cluster center calculation downward dynamically as user moves deeper into sections
            const centerY = (height / 2) - (scrollY * 0.35);
            const centerX = width / 2;

            for (let i = 0; i < particleCount; i++) {
                const p = particles[i];
                
                // Advance the spiral angular path over time
                p.baseAngle += p.speed * 0.25;

                // Modulate physics configuration dynamically to mimic transformation from Galaxy to Sphere
                let currentAngle = p.baseAngle;
                let currentDist = p.distance;

                // Kinetic compression logic altering matrix into a concentrated planetary circle 
                if (scrollY > 300) {
                    const transformFactor = Math.min((scrollY - 300) / 500, 1);
                    // Compress cosmic spread smoothly to generate structured circular pathing coordinates
                    currentDist = (p.distance * (1 - transformFactor)) + ((160 + Math.sin(p.baseAngle * 3 + p.seedY) * 30) * transformFactor);
                }

                const x = centerX + Math.cos(currentAngle) * currentDist;
                const y = centerY + Math.sin(currentAngle) * currentDist;

                ctx.beginPath();
                ctx.arc(x, y, p.size, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.fill();
            }

            requestAnimationFrame(animate);
        }

        animate();
    </script>
</body>
</html>
"""

# Render the layout directly into Streamlit's container DOM scope cleanly
st.components.v1.html(portfolio_html, height=3500, scrolling=True)
