import re

HTML_PATH = '/Users/albinkrasniqi/Desktop/SITE/index.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. ARCADE MINIGAME CSS
arcade_css = """
    /* ==========================================================================
       ===== VEIRA VOID FIGHTER ARCADE MINIGAME STYLES =====
       ========================================================================== */
    #arcade-game {
      background: radial-gradient(circle at 50% 30%, rgba(0, 229, 255, 0.04) 0%, #000000 85%);
      position: relative;
      z-index: 5;
      padding: 100px 0;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .arcade-wrapper {
      max-width: 980px;
      margin: 0 auto;
      background: #06080d;
      border: 2px solid rgba(0, 229, 255, 0.4);
      box-shadow: 0 0 50px rgba(0, 229, 255, 0.15), inset 0 0 30px rgba(0, 0, 0, 0.9);
      position: relative;
      overflow: hidden;
    }

    .arcade-top-bar {
      background: #0b0f17;
      padding: 12px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(0, 229, 255, 0.3);
      font-family: var(--font-mono);
      font-size: 13px;
      color: #94a3b8;
    }

    .arcade-title-tag {
      display: flex;
      align-items: center;
      gap: 10px;
      color: #ffffff;
      font-weight: 700;
      letter-spacing: 1px;
    }

    .arcade-title-tag .blinking-led {
      width: 10px;
      height: 10px;
      background: #00ff9d;
      box-shadow: 0 0 8px #00ff9d;
      animation: arcadeBlink 1s infinite alternate;
    }

    @keyframes arcadeBlink {
      0% { opacity: 0.3; }
      100% { opacity: 1; }
    }

    .arcade-hud-row {
      background: rgba(4, 6, 10, 0.95);
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      font-family: var(--font-mono);
    }

    .arcade-hearts-hud {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .arcade-hearts-hud .hud-label {
      font-size: 12px;
      color: #71717a;
      letter-spacing: 1.5px;
      font-weight: 700;
      margin-right: 4px;
    }

    .heart-icon {
      font-size: 20px;
      color: #ff2a5f;
      text-shadow: 0 0 10px rgba(255, 42, 95, 0.8);
      transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .heart-icon.empty {
      color: #27272a;
      text-shadow: none;
      filter: grayscale(1);
      opacity: 0.4;
    }

    .arcade-stats-hud {
      display: flex;
      align-items: center;
      gap: 24px;
      font-size: 14px;
    }

    .stat-box {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .stat-label {
      font-size: 10.5px;
      color: #64748b;
      letter-spacing: 1px;
      text-transform: uppercase;
    }

    .stat-value {
      color: #00e5ff;
      font-weight: 700;
      font-size: 16px;
      letter-spacing: 1px;
      text-shadow: 0 0 8px rgba(0, 229, 255, 0.5);
    }

    .stat-value.gold {
      color: #ffd700;
      text-shadow: 0 0 8px rgba(255, 215, 0, 0.5);
    }

    .arcade-controls-hud {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .arcade-btn-toggle {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #cbd5e1;
      padding: 6px 12px;
      font-size: 11.5px;
      font-family: var(--font-mono);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .arcade-btn-toggle:hover {
      background: rgba(0, 229, 255, 0.15);
      border-color: #00e5ff;
      color: #ffffff;
    }

    .arcade-btn-toggle.active {
      background: rgba(0, 255, 157, 0.15);
      border-color: #00ff9d;
      color: #00ff9d;
    }

    /* The Main Game Canvas Screen */
    .arcade-viewport {
      position: relative;
      width: 100%;
      height: 520px;
      background: #000000;
      cursor: crosshair;
      overflow: hidden;
    }

    #game-canvas {
      display: block;
      width: 100%;
      height: 100%;
      image-rendering: pixelated;
    }

    /* Retro Scanline Overlay */
    .arcade-scanlines {
      position: absolute;
      inset: 0;
      background: linear-gradient(
        to bottom,
        rgba(255,255,255,0),
        rgba(255,255,255,0) 50%,
        rgba(0, 0, 0, 0.3) 50%,
        rgba(0, 0, 0, 0.3)
      );
      background-size: 100% 4px;
      pointer-events: none;
      opacity: 0.65;
    }

    .arcade-crt-glow {
      position: absolute;
      inset: 0;
      box-shadow: inset 0 0 80px rgba(0, 229, 255, 0.08), inset 0 0 20px rgba(0, 0, 0, 0.9);
      pointer-events: none;
    }

    /* Start / Pause / Game Over Screens */
    .arcade-overlay-screen {
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.88);
      backdrop-filter: blur(4px);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 30px;
      z-index: 10;
      transition: opacity 0.3s ease;
    }

    .arcade-overlay-screen.hidden {
      opacity: 0;
      pointer-events: none;
      visibility: hidden;
    }

    .game-logo-title {
      font-family: var(--font-display);
      font-size: clamp(28px, 5vw, 44px);
      font-weight: 800;
      letter-spacing: 2px;
      color: #ffffff;
      margin-bottom: 8px;
      text-shadow: 0 0 20px rgba(0, 229, 255, 0.8);
    }

    .game-logo-sub {
      font-family: var(--font-mono);
      font-size: 13.5px;
      color: #00e5ff;
      letter-spacing: 2px;
      margin-bottom: 24px;
    }

    .game-instructions-box {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.12);
      padding: 16px 24px;
      max-width: 520px;
      margin-bottom: 28px;
      font-family: var(--font-mono);
      font-size: 12.5px;
      color: #94a3b8;
      line-height: 1.7;
      text-align: left;
    }

    .game-instructions-box b {
      color: #ffffff;
    }

    .game-instructions-box span.key-badge {
      display: inline-block;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: #00ff9d;
      padding: 1px 6px;
      font-size: 11px;
      margin: 0 2px;
    }

    .btn-play-game {
      background: #00e5ff;
      color: #000000;
      font-family: var(--font-mono);
      font-weight: 800;
      font-size: 15px;
      letter-spacing: 1.5px;
      padding: 14px 36px;
      border: none;
      cursor: pointer;
      box-shadow: 0 0 25px rgba(0, 229, 255, 0.6);
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 10px;
    }

    .btn-play-game:hover {
      background: #ffffff;
      transform: scale(1.04);
      box-shadow: 0 0 35px rgba(255, 255, 255, 0.8);
    }

    .arcade-bottom-bar {
      background: #0b0f17;
      padding: 12px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: #64748b;
    }

    /* Floating Quick Launch Button */
    #floating-arcade-launcher {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: rgba(6, 8, 13, 0.92);
      border: 1px solid #00e5ff;
      color: #ffffff;
      padding: 10px 18px;
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      letter-spacing: 0.5px;
      cursor: pointer;
      z-index: 9999;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.9), 0 0 20px rgba(0, 229, 255, 0.35);
      backdrop-filter: blur(10px);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    #floating-arcade-launcher:hover {
      background: #00e5ff;
      color: #000000;
      transform: translateY(-3px);
      box-shadow: 0 12px 35px rgba(0, 229, 255, 0.6);
    }

    #floating-arcade-launcher .pulse-red-dot {
      width: 8px;
      height: 8px;
      background: #ff2a5f;
      border-radius: 50% !important;
      box-shadow: 0 0 8px #ff2a5f;
      animation: redPulse 1.2s infinite;
    }

    @keyframes redPulse {
      0% { transform: scale(0.9); opacity: 0.6; }
      50% { transform: scale(1.3); opacity: 1; }
      100% { transform: scale(0.9); opacity: 0.6; }
    }

    @media (max-width: 768px) {
      .arcade-viewport { height: 420px; }
      .arcade-hud-row { padding: 10px 14px; gap: 10px; }
      .stat-value { font-size: 14px; }
      .arcade-stats-hud { gap: 14px; }
    }
"""

# Insert Arcade CSS before </style>
if '#arcade-game' not in content:
    content = content.replace('  </style>', arcade_css + '\n  </style>')

# 2. ARCADE MINIGAME SECTION HTML
arcade_section_html = """
  <!-- ===== ARCADE GAME SECTION (LIVE GAME DEV SHOWCASE) ===== -->
  <section id="arcade-game">
    <div class="container">
      <div class="reveal-item" style="text-align: center; max-width: 780px; margin: 0 auto 40px auto;">
        <span class="section-eyebrow" style="justify-content: center;">Playable Engine Demo</span>
        <h2 class="section-title">VEIRA VOID FIGHTER — <span class="text-gradient">PLAY LIVE</span></h2>
        <p class="section-desc" style="margin: 0 auto;">Pilot our custom HTML5/Canvas fighter ship, dodge slow alien plasma projectiles, and eliminate hostile enemy waves to test our 60 FPS real-time combat engine.</p>
      </div>

      <div class="arcade-wrapper reveal-item">
        <!-- Arcade Top Bar -->
        <div class="arcade-top-bar">
          <div class="arcade-title-tag">
            <span class="blinking-led"></span>
            <span>VEIRA HARD-SURFACE ARCADE ENGINE // V2.4</span>
          </div>
          <div>SIMULATION READY • 60 FPS FIXED</div>
        </div>

        <!-- Arcade HUD Row -->
        <div class="arcade-hud-row">
          <!-- 3 HP Hearts -->
          <div class="arcade-hearts-hud">
            <span class="hud-label">SHIELD HP:</span>
            <span id="hp-heart-1" class="heart-icon">❤️</span>
            <span id="hp-heart-2" class="heart-icon">❤️</span>
            <span id="hp-heart-3" class="heart-icon">❤️</span>
          </div>

          <!-- Stats: Score, Wave, High Score -->
          <div class="arcade-stats-hud">
            <div class="stat-box">
              <span class="stat-label">Score</span>
              <span id="game-score-val" class="stat-value">00000</span>
            </div>
            <div class="stat-box">
              <span class="stat-label">Wave</span>
              <span id="game-wave-val" class="stat-value">1</span>
            </div>
            <div class="stat-box">
              <span class="stat-label">High Score</span>
              <span id="game-high-val" class="stat-value gold">00000</span>
            </div>
          </div>

          <!-- Quick Controls / Toggles -->
          <div class="arcade-controls-hud">
            <button id="toggle-sound-btn" class="arcade-btn-toggle active" title="Toggle 8-bit Audio">
              <span>🔊</span> <span id="sound-label">SFX: ON</span>
            </button>
            <button id="toggle-autofire-btn" class="arcade-btn-toggle active" title="Toggle Auto Fire">
              <span>⚡</span> <span id="autofire-label">AUTO-FIRE: ON</span>
            </button>
          </div>
        </div>

        <!-- Arcade Canvas Viewport -->
        <div class="arcade-viewport" id="game-viewport">
          <canvas id="game-canvas"></canvas>
          <div class="arcade-scanlines"></div>
          <div class="arcade-crt-glow"></div>

          <!-- Start Screen Overlay -->
          <div class="arcade-overlay-screen" id="game-start-screen">
            <div class="game-logo-title">VEIRA VOID FIGHTER</div>
            <div class="game-logo-sub">[RETRO ARCADE COMBAT SIMULATOR]</div>
            <div class="game-instructions-box">
              <div><b>MISSION:</b> Defend the quadrant from incoming alien battlecraft.</div>
              <div><b>SHIELD:</b> You start with <span style="color:#ff2a5f;">❤️❤️❤️ 3 HP Hearts</span>.</div>
              <div><b>CONTROLS:</b> Move with <span class="key-badge">MOUSE / TOUCH</span> or <span class="key-badge">W A S D</span> / <span class="key-badge">ARROWS</span>.</div>
              <div><b>FIRE:</b> <span class="key-badge">LEFT CLICK</span> or <span class="key-badge">SPACEBAR</span> (Auto-fire enabled by default).</div>
              <div style="color: #00ff9d; margin-top: 4px;">💡 <i>Tip: Alien plasma flies slower than your lasers—dodge through gaps!</i></div>
            </div>
            <button id="start-game-btn" class="btn-play-game">
              <span>LAUNCH FIGHTER ➔</span>
            </button>
          </div>

          <!-- Game Over Screen Overlay -->
          <div class="arcade-overlay-screen hidden" id="game-over-screen">
            <div class="game-logo-title" style="color: #ff2a5f; text-shadow: 0 0 20px rgba(255, 42, 95, 0.8);">MISSION FAILED</div>
            <div class="game-logo-sub" id="game-over-reason">[SHIP DESTROYED // SHIELD DEPLETED]</div>
            
            <div class="game-instructions-box" style="text-align: center;">
              <div style="font-size: 15px; margin-bottom: 6px;">FINAL SCORE: <span id="final-score-val" style="color: #00e5ff; font-weight: bold;">00000</span></div>
              <div style="font-size: 13px; margin-bottom: 6px;">WAVES CLEARED: <span id="final-waves-val" style="color: #00ff9d; font-weight: bold;">1</span></div>
              <div style="font-size: 13px; color: #ffd700;">ALIENS VAPORIZED: <span id="final-kills-val" style="font-weight: bold;">0</span></div>
            </div>

            <button id="restart-game-btn" class="btn-play-game" style="background: #ff2a5f; box-shadow: 0 0 25px rgba(255, 42, 95, 0.6); color: #ffffff;">
              <span>REDEPLOY SHIP ➔</span>
            </button>
          </div>
        </div>

        <!-- Arcade Bottom Status -->
        <div class="arcade-bottom-bar">
          <div>ENGINE: Custom Canvas 2D + WebAudio Synthesizer</div>
          <div>POWERUPS: ❤️ Shield Repair • ⚡ Plasma Boost • 💣 Screen Bomb</div>
        </div>
      </div>
    </div>
  </section>

  <!-- Floating Quick Launcher for Minigame -->
  <a href="#arcade-game" id="floating-arcade-launcher" aria-label="Play Void Fighter Minigame">
    <span class="pulse-red-dot"></span>
    <span>🕹️ PLAY VOID FIGHTER [3 ❤️ HP]</span>
  </a>
"""

# Insert Arcade Section right before #models3d section
if '<section id="arcade-game">' not in content:
    content = content.replace('<section id="models3d" class="section">', arcade_section_html + '\n  <section id="models3d" class="section">')

# 3. COMPLETE MINIGAME ENGINE JAVASCRIPT
minigame_engine_js = """
  <!-- ===== VOID FIGHTER PLAYABLE MINIGAME ENGINE ===== -->
  <script>
  (function() {
    'use strict';

    // DOM Elements
    const canvas = document.getElementById('game-canvas');
    const viewport = document.getElementById('game-viewport');
    if (!canvas || !viewport) return;

    const ctx = canvas.getContext('2d');
    const scoreValEl = document.getElementById('game-score-val');
    const waveValEl = document.getElementById('game-wave-val');
    const highValEl = document.getElementById('game-high-val');
    const heart1El = document.getElementById('hp-heart-1');
    const heart2El = document.getElementById('hp-heart-2');
    const heart3El = document.getElementById('hp-heart-3');
    const soundBtn = document.getElementById('toggle-sound-btn');
    const soundLabel = document.getElementById('sound-label');
    const autofireBtn = document.getElementById('toggle-autofire-btn');
    const autofireLabel = document.getElementById('autofire-label');
    const startScreen = document.getElementById('game-start-screen');
    const gameOverScreen = document.getElementById('game-over-screen');
    const startBtn = document.getElementById('start-game-btn');
    const restartBtn = document.getElementById('restart-game-btn');
    const finalScoreEl = document.getElementById('final-score-val');
    const finalWavesEl = document.getElementById('final-waves-val');
    const finalKillsEl = document.getElementById('final-kills-val');

    // Web Audio 8-bit Sound Synthesizer
    let audioCtx = null;
    let soundEnabled = true;
    let autoFireEnabled = true;

    function initAudio() {
      if (!audioCtx) {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (AudioContextClass) {
          audioCtx = new AudioContextClass();
        }
      }
      if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
    }

    function playSound(type) {
      if (!soundEnabled || !audioCtx) return;
      try {
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        if (type === 'laser') {
          // Pew Pew sound
          osc.type = 'square';
          osc.frequency.setValueAtTime(880, now);
          osc.frequency.exponentialRampToValueAtTime(140, now + 0.12);
          gain.gain.setValueAtTime(0.15, now);
          gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
          osc.start(now);
          osc.stop(now + 0.12);
        } else if (type === 'alien_laser') {
          // Lower tone slow shot
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(320, now);
          osc.frequency.exponentialRampToValueAtTime(80, now + 0.2);
          gain.gain.setValueAtTime(0.08, now);
          gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
          osc.start(now);
          osc.stop(now + 0.2);
        } else if (type === 'explode') {
          // Retro Explosion rumble
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(160, now);
          osc.frequency.exponentialRampToValueAtTime(30, now + 0.35);
          gain.gain.setValueAtTime(0.3, now);
          gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
          osc.start(now);
          osc.stop(now + 0.35);
        } else if (type === 'hurt') {
          // Player Hit Hurt buzz
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(180, now);
          osc.frequency.linearRampToValueAtTime(60, now + 0.25);
          gain.gain.setValueAtTime(0.35, now);
          gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
          osc.start(now);
          osc.stop(now + 0.25);
        } else if (type === 'heart') {
          // 1UP / Health Restore chime
          osc.type = 'sine';
          osc.frequency.setValueAtTime(523.25, now); // C5
          osc.frequency.setValueAtTime(659.25, now + 0.08); // E5
          osc.frequency.setValueAtTime(783.99, now + 0.16); // G5
          osc.frequency.setValueAtTime(1046.50, now + 0.24); // C6
          gain.gain.setValueAtTime(0.2, now);
          gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
          osc.start(now);
          osc.stop(now + 0.35);
        } else if (type === 'gameover') {
          // Descending loss tones
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(260, now);
          osc.frequency.setValueAtTime(220, now + 0.15);
          osc.frequency.setValueAtTime(175, now + 0.3);
          osc.frequency.setValueAtTime(110, now + 0.45);
          gain.gain.setValueAtTime(0.25, now);
          gain.gain.exponentialRampToValueAtTime(0.01, now + 0.65);
          osc.start(now);
          osc.stop(now + 0.65);
        }
      } catch (err) {
        // Fallback gracefully if Web Audio is blocked
      }
    }

    if (soundBtn) {
      soundBtn.addEventListener('click', () => {
        soundEnabled = !soundEnabled;
        soundBtn.classList.toggle('active', soundEnabled);
        if (soundLabel) soundLabel.textContent = soundEnabled ? 'SFX: ON' : 'SFX: OFF';
        if (soundEnabled) initAudio();
      });
    }

    if (autofireBtn) {
      autofireBtn.addEventListener('click', () => {
        autoFireEnabled = !autoFireEnabled;
        autofireBtn.classList.toggle('active', autoFireEnabled);
        if (autofireLabel) autofireLabel.textContent = autoFireEnabled ? 'AUTO-FIRE: ON' : 'AUTO-FIRE: OFF';
      });
    }

    // Game Dimensions & Setup
    let W = 800;
    let H = 500;
    let isPlaying = false;
    let score = 0;
    let highScore = parseInt(localStorage.getItem('veira_void_highscore') || '0', 10);
    let wave = 1;
    let kills = 0;
    let screenShake = 0;

    if (highValEl) highValEl.textContent = String(highScore).padStart(5, '0');

    function resizeGame() {
      const rect = viewport.getBoundingClientRect();
      W = Math.floor(rect.width);
      H = Math.floor(rect.height);
      canvas.width = W;
      canvas.height = H;
    }

    window.addEventListener('resize', resizeGame);

    // Keyboard / Mouse Control State
    const keys = {};
    let mousePos = { x: W / 2, y: H - 80 };
    let isMouseDown = false;

    window.addEventListener('keydown', (e) => {
      keys[e.code] = true;
      if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) {
        if (document.activeElement === canvas || viewport.contains(document.activeElement)) {
          e.preventDefault();
        }
      }
      if (e.code === 'Space' && !isPlaying && !startScreen.classList.contains('hidden')) {
        startGame();
      } else if (e.code === 'Space' && !isPlaying && !gameOverScreen.classList.contains('hidden')) {
        startGame();
      }
    });

    window.addEventListener('keyup', (e) => {
      keys[e.code] = false;
    });

    viewport.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      mousePos.x = e.clientX - rect.left;
      mousePos.y = e.clientY - rect.top;
    });

    viewport.addEventListener('mousedown', () => {
      isMouseDown = true;
      initAudio();
    });

    window.addEventListener('mouseup', () => {
      isMouseDown = false;
    });

    // Touch support for mobile / tablets
    viewport.addEventListener('touchmove', (e) => {
      if (e.touches.length > 0) {
        const rect = canvas.getBoundingClientRect();
        mousePos.x = e.touches[0].clientX - rect.left;
        mousePos.y = e.touches[0].clientY - rect.top;
      }
    }, { passive: true });

    viewport.addEventListener('touchstart', (e) => {
      isMouseDown = true;
      initAudio();
      if (e.touches.length > 0) {
        const rect = canvas.getBoundingClientRect();
        mousePos.x = e.touches[0].clientX - rect.left;
        mousePos.y = e.touches[0].clientY - rect.top;
      }
    }, { passive: true });

    viewport.addEventListener('touchend', () => {
      isMouseDown = false;
    });

    // SPRITE COLOR PALETTE & RASTER MAPS
    const PALETTE = {
      W: '#ffffff', // White
      C: '#00e5ff', // Cyan
      B: '#0066ff', // Electric Blue
      R: '#ff2a5f', // Ruby Red
      P: '#ff77a8', // Pink
      G: '#ffd700', // Gold
      O: '#ff9e00', // Orange
      Y: '#facc15', // Yellow
      M: '#00ff9d', // Mint Green
      E: '#e2e8f0', // Silver / Light Gray
      S: '#334155', // Slate
      K: '#0b0f17', // Outline
      V: '#a855f7', // Alien Violet
      D: '#7e22ce'  // Dark Purple
    };

    // 1. Player Fighter Ship (11x11 Bitmap)
    const PLAYER_SPRITE = [
      ['_','_','_','_','_','C','_','_','_','_','_'],
      ['_','_','_','_','K','W','K','_','_','_','_'],
      ['_','_','_','_','K','C','K','_','_','_','_'],
      ['_','_','_','K','C','C','C','K','_','_','_'],
      ['_','_','K','E','C','C','C','E','K','_','_'],
      ['_','K','E','E','C','B','C','E','E','K','_'],
      ['K','E','E','C','B','B','B','C','E','E','K'],
      ['K','C','C','B','B','B','B','B','C','C','K'],
      ['K','K','C','K','K','W','K','K','C','K','K'],
      ['_','K','K','_','K','K','K','_','K','K','_'],
      ['_','_','_','_','O','Y','O','_','_','_','_']
    ];

    // 2. Alien Scout (9x8 Bitmap - Fast, Single shot)
    const ALIEN_SCOUT_SPRITE = [
      ['K','_','_','_','_','_','_','_','K'],
      ['K','V','_','_','_','_','_','V','K'],
      ['K','V','V','K','K','K','V','V','K'],
      ['_','K','V','R','R','R','V','K','_'],
      ['_','K','V','V','V','V','V','K','_'],
      ['_','_','K','D','D','D','K','_','_'],
      ['_','K','_','K','_','K','_','K','_'],
      ['K','_','_','_','_','_','_','_','K']
    ];

    // 3. Alien Cruiser (11x10 Bitmap - Heavy, Twin cannon)
    const ALIEN_CRUISER_SPRITE = [
      ['_','_','_','K','K','K','K','K','_','_','_'],
      ['_','K','K','R','V','V','V','R','K','K','_'],
      ['K','R','V','V','R','R','R','V','V','R','K'],
      ['K','V','R','R','Y','Y','Y','R','R','V','K'],
      ['K','V','V','V','Y','W','Y','V','V','V','K'],
      ['_','K','V','V','R','Y','R','V','V','K','_'],
      ['_','_','K','D','D','D','D','D','K','_','_'],
      ['_','K','R','K','_','_','_','K','R','K','_'],
      ['K','R','R','K','_','_','_','K','R','R','K'],
      ['_','K','K','_','_','_','_','_','K','K','_']
    ];

    // 4. Power-Up: Heart Container (8x7 Bitmap)
    const HEART_ITEM_SPRITE = [
      ['_','K','K','_','_','K','K','_'],
      ['K','P','W','K','K','P','W','K'],
      ['K','R','P','R','R','R','R','K'],
      ['K','R','R','R','R','R','R','K'],
      ['_','K','R','R','R','R','K','_'],
      ['_','_','K','R','R','K','_','_'],
      ['_','_','_','K','K','_','_','_']
    ];

    function drawPixelBitmap(matrix, startX, startY, pixelSize, alpha = 1.0) {
      ctx.save();
      ctx.globalAlpha = alpha;
      const rows = matrix.length;
      for (let r = 0; r < rows; r++) {
        const row = matrix[r];
        const cols = row.length;
        for (let c = 0; c < cols; c++) {
          const key = row[c];
          if (key && key !== '_' && PALETTE[key]) {
            ctx.fillStyle = PALETTE[key];
            ctx.fillRect(
              Math.floor(startX + c * pixelSize),
              Math.floor(startY + r * pixelSize),
              pixelSize,
              pixelSize
            );
          }
        }
      }
      ctx.restore();
    }

    // GAME STATE ENTITIES
    let player = {
      x: W / 2,
      y: H - 80,
      hp: 3, // EXACTLY 3 HP HEARTS
      maxHp: 3,
      speed: 6.5,
      pixelSize: 3,
      width: 33,
      height: 33,
      invulnTimer: 0,
      shootCooldown: 0,
      thrusterFrame: 0
    };

    let playerLasers = [];
    let alienShips = [];
    let alienLasers = [];
    let explosions = [];
    let powerups = [];
    let scorePopups = [];
    let bgStars = [];

    // Background Stars for Arcade Canvas
    function initBgStars() {
      bgStars = [];
      for (let i = 0; i < 45; i++) {
        bgStars.push({
          x: Math.random() * W,
          y: Math.random() * H,
          speed: Math.random() * 1.5 + 0.5,
          size: Math.random() < 0.3 ? 2 : 1,
          color: Math.random() < 0.4 ? '#00e5ff' : '#ffffff',
          alpha: Math.random() * 0.6 + 0.3
        });
      }
    }

    // Player HP HUD Updater
    function updateHeartsHUD() {
      if (heart1El) heart1El.className = player.hp >= 1 ? 'heart-icon' : 'heart-icon empty';
      if (heart2El) heart2El.className = player.hp >= 2 ? 'heart-icon' : 'heart-icon empty';
      if (heart3El) heart3El.className = player.hp >= 3 ? 'heart-icon' : 'heart-icon empty';
    }

    // Reset Game State
    function resetGame() {
      resizeGame();
      initBgStars();
      player.x = W / 2;
      player.y = H - 80;
      player.hp = 3;
      player.invulnTimer = 0;
      player.shootCooldown = 0;
      playerLasers = [];
      alienShips = [];
      alienLasers = [];
      explosions = [];
      powerups = [];
      scorePopups = [];
      score = 0;
      wave = 1;
      kills = 0;
      screenShake = 0;

      updateHeartsHUD();
      if (scoreValEl) scoreValEl.textContent = '00000';
      if (waveValEl) waveValEl.textContent = '1';
    }

    function startGame() {
      initAudio();
      resetGame();
      isPlaying = true;
      startScreen.classList.add('hidden');
      gameOverScreen.classList.add('hidden');
    }

    function triggerGameOver() {
      isPlaying = false;
      playSound('gameover');

      if (score > highScore) {
        highScore = score;
        localStorage.setItem('veira_void_highscore', String(highScore));
        if (highValEl) highValEl.textContent = String(highScore).padStart(5, '0');
      }

      if (finalScoreEl) finalScoreEl.textContent = String(score).padStart(5, '0');
      if (finalWavesEl) finalWavesEl.textContent = String(wave);
      if (finalKillsEl) finalKillsEl.textContent = String(kills);

      gameOverScreen.classList.remove('hidden');
    }

    if (startBtn) startBtn.addEventListener('click', startGame);
    if (restartBtn) restartBtn.addEventListener('click', startGame);

    // Player Shooting Logic (Laser Bolts)
    function shootPlayerLaser() {
      if (player.shootCooldown <= 0) {
        player.shootCooldown = 12; // rate of fire
        playSound('laser');

        // Dual Wing Lasers
        playerLasers.push({
          x: player.x - 10,
          y: player.y - 6,
          vx: 0,
          vy: -10, // Fast player lasers
          width: 3,
          height: 12,
          color: '#00e5ff'
        });

        playerLasers.push({
          x: player.x + 10,
          y: player.y - 6,
          vx: 0,
          vy: -10,
          width: 3,
          height: 12,
          color: '#00e5ff'
        });
      }
    }

    // Alien Spawning Waves
    let alienSpawnTimer = 0;

    function spawnAliens() {
      alienSpawnTimer++;
      const spawnInterval = Math.max(35, 75 - wave * 6);

      if (alienSpawnTimer >= spawnInterval) {
        alienSpawnTimer = 0;
        const isCruiser = Math.random() < 0.28;

        if (isCruiser) {
          alienShips.push({
            type: 'cruiser',
            x: Math.random() * (W - 80) + 40,
            y: -50,
            vx: (Math.random() - 0.5) * 1.5,
            vy: Math.random() * 0.8 + 0.9,
            hp: 4,
            maxHp: 4,
            width: 33,
            height: 30,
            pixelSize: 3,
            sprite: ALIEN_CRUISER_SPRITE,
            shootTimer: Math.floor(Math.random() * 40 + 50),
            shootInterval: 75, // Slower shooting rate
            scoreVal: 300
          });
        } else {
          alienShips.push({
            type: 'scout',
            x: Math.random() * (W - 60) + 30,
            y: -40,
            vx: (Math.random() - 0.5) * 2.2,
            vy: Math.random() * 1.2 + 1.3,
            hp: 2,
            maxHp: 2,
            width: 27,
            height: 24,
            pixelSize: 3,
            sprite: ALIEN_SCOUT_SPRITE,
            shootTimer: Math.floor(Math.random() * 50 + 60),
            shootInterval: 95, // Slower shooting rate
            scoreVal: 120
          });
        }
      }
    }

    // Alien Shooting (SLOWER PLASMA BOLTS for dodgeable skill-based combat)
    function fireAlienLaser(alien) {
      playSound('alien_laser');

      // Aim slowly towards player's position
      const dx = player.x - alien.x;
      const dy = player.y - alien.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;

      // Slow bullet speed (3.0 vs Player's 10.0)
      const bulletSpeed = 3.2;

      if (alien.type === 'cruiser') {
        // Twin slow plasma orbs
        alienLasers.push({
          x: alien.x - 8,
          y: alien.y + 12,
          vx: (dx / dist) * bulletSpeed - 0.3,
          vy: (dy / dist) * bulletSpeed,
          radius: 4,
          color: '#ff2a5f'
        });
        alienLasers.push({
          x: alien.x + 8,
          y: alien.y + 12,
          vx: (dx / dist) * bulletSpeed + 0.3,
          vy: (dy / dist) * bulletSpeed,
          radius: 4,
          color: '#ff2a5f'
        });
      } else {
        // Single slow glowing violet plasma orb
        alienLasers.push({
          x: alien.x,
          y: alien.y + 10,
          vx: (dx / dist) * bulletSpeed,
          vy: (dy / dist) * bulletSpeed,
          radius: 4,
          color: '#a855f7'
        });
      }
    }

    // Explosion Particles
    function spawnExplosion(x, y, color = '#ff9e00', count = 16) {
      playSound('explode');
      screenShake = 6;
      for (let i = 0; i < count; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 4.5 + 1.2;
        explosions.push({
          x: x,
          y: y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          size: Math.random() < 0.5 ? 3 : 2,
          color: Math.random() < 0.4 ? '#ffffff' : (Math.random() < 0.5 ? color : '#ffd700'),
          alpha: 1.0,
          decay: Math.random() * 0.03 + 0.02
        });
      }
    }

    // Floating Score Popup
    function addScorePopup(text, x, y, color = '#ffd700') {
      scorePopups.push({
        text: text,
        x: x,
        y: y,
        vy: -1.6,
        color: color,
        alpha: 1.0
      });
    }

    // Damage Player (3 HP Hearts Logic)
    function damagePlayer() {
      if (player.invulnTimer > 0) return; // Invulnerability frames

      player.hp -= 1;
      player.invulnTimer = 85; // ~1.4 seconds of invulnerability
      screenShake = 14;
      playSound('hurt');
      updateHeartsHUD();

      // Spawn damage sparks
      spawnExplosion(player.x, player.y, '#ff2a5f', 12);
      addScorePopup('-1 HP!', player.x - 20, player.y - 25, '#ff2a5f');

      if (player.hp <= 0) {
        player.hp = 0;
        updateHeartsHUD();
        spawnExplosion(player.x, player.y, '#ff2a5f', 30);
        setTimeout(triggerGameOver, 300);
      }
    }

    // Restore Health Item Pickup
    function restorePlayerHp() {
      if (player.hp < player.maxHp) {
        player.hp++;
        updateHeartsHUD();
        playSound('heart');
        addScorePopup('+1 HP FULL!', player.x - 30, player.y - 25, '#ff2a5f');
      } else {
        // Bonus Points
        score += 500;
        playSound('heart');
        addScorePopup('+500 PTS!', player.x - 25, player.y - 25, '#ffd700');
        if (scoreValEl) scoreValEl.textContent = String(score).padStart(5, '0');
      }
    }

    // MAIN GAME UPDATE LOOP (60 FPS)
    function updateGame() {
      if (!isPlaying) return;

      // 1. Player Controls & Movement
      // Mouse Lerp Smooth Movement
      const dx = mousePos.x - player.x;
      const dy = mousePos.y - player.y;
      player.x += dx * 0.16;
      player.y += dy * 0.16;

      // Keyboard Controls (WASD / Arrows)
      if (keys['KeyA'] || keys['ArrowLeft']) player.x -= player.speed;
      if (keys['KeyD'] || keys['ArrowRight']) player.x += player.speed;
      if (keys['KeyW'] || keys['ArrowUp']) player.y -= player.speed;
      if (keys['KeyS'] || keys['ArrowDown']) player.y += player.speed;

      // Boundaries
      player.x = Math.max(20, Math.min(W - 20, player.x));
      player.y = Math.max(30, Math.min(H - 25, player.y));

      // Shooting
      if (player.shootCooldown > 0) player.shootCooldown--;
      if (autoFireEnabled || isMouseDown || keys['Space']) {
        shootPlayerLaser();
      }

      if (player.invulnTimer > 0) player.invulnTimer--;
      player.thrusterFrame = (player.thrusterFrame + 1) % 6;

      // 2. Background Stars Movement
      for (let i = 0; i < bgStars.length; i++) {
        const s = bgStars[i];
        s.y += s.speed;
        if (s.y > H) {
          s.y = 0;
          s.x = Math.random() * W;
        }
      }

      // 3. Player Lasers Update
      for (let i = playerLasers.length - 1; i >= 0; i--) {
        const l = playerLasers[i];
        l.x += l.vx;
        l.y += l.vy;

        if (l.y < -20) {
          playerLasers.splice(i, 1);
        }
      }

      // 4. Spawn Aliens & Waves
      spawnAliens();

      // Wave Progression
      const currentWaveTarget = wave * 8;
      if (kills >= currentWaveTarget) {
        wave++;
        if (waveValEl) waveValEl.textContent = String(wave);
        addScorePopup('WAVE ' + wave + ' INCOMING!', W / 2 - 60, H / 2 - 20, '#00ff9d');
      }

      // 5. Alien Ships Update & AI
      for (let i = alienShips.length - 1; i >= 0; i--) {
        const a = alienShips[i];
        a.x += a.vx;
        a.y += a.vy;

        // Bounce on horizontal walls
        if (a.x < 30 || a.x > W - 30) a.vx *= -1;

        // Alien Shooting
        a.shootTimer--;
        if (a.shootTimer <= 0 && a.y > 20 && a.y < H - 80) {
          a.shootTimer = a.shootInterval;
          fireAlienLaser(a);
        }

        // Alien Collides with Player
        const distToPlayer = Math.hypot(a.x - player.x, a.y - player.y);
        if (distToPlayer < 24) {
          damagePlayer();
          spawnExplosion(a.x, a.y, '#ff2a5f', 16);
          alienShips.splice(i, 1);
          continue;
        }

        // Alien Hit by Player Lasers
        for (let j = playerLasers.length - 1; j >= 0; j--) {
          const l = playerLasers[j];
          if (
            l.x > a.x - a.width / 2 &&
            l.x < a.x + a.width / 2 &&
            l.y > a.y - a.height / 2 &&
            l.y < a.y + a.height / 2
          ) {
            playerLasers.splice(j, 1);
            a.hp--;

            // Small spark on hit
            for (let k = 0; k < 3; k++) {
              explosions.push({
                x: l.x,
                y: l.y,
                vx: (Math.random() - 0.5) * 3,
                vy: (Math.random() - 0.5) * 3,
                size: 2,
                color: '#00e5ff',
                alpha: 0.8,
                decay: 0.05
              });
            }

            if (a.hp <= 0) {
              // Alien Destroyed!
              spawnExplosion(a.x, a.y, a.type === 'cruiser' ? '#ff2a5f' : '#00e5ff', 20);
              kills++;
              score += a.scoreVal;
              if (scoreValEl) scoreValEl.textContent = String(score).padStart(5, '0');
              addScorePopup('+' + a.scoreVal, a.x - 15, a.y - 15, '#ffd700');

              // Chance to drop 1-UP Health Heart (20% on cruiser, 8% on scout)
              const heartDropChance = a.type === 'cruiser' ? 0.35 : 0.08;
              if (Math.random() < heartDropChance) {
                powerups.push({
                  type: 'heart',
                  x: a.x,
                  y: a.y,
                  vy: 1.2,
                  bob: Math.random() * Math.PI * 2
                });
              }

              alienShips.splice(i, 1);
              break;
            }
          }
        }

        // Out of screen bottom
        if (a.y > H + 50) {
          alienShips.splice(i, 1);
        }
      }

      // 6. Alien Slower Lasers Update & Player Collision
      for (let i = alienLasers.length - 1; i >= 0; i--) {
        const al = alienLasers[i];
        al.x += al.vx;
        al.y += al.vy;

        // Collision with player
        const dist = Math.hypot(al.x - player.x, al.y - player.y);
        if (dist < 15) {
          damagePlayer();
          alienLasers.splice(i, 1);
          continue;
        }

        // Out of bounds
        if (al.y > H + 30 || al.x < -30 || al.x > W + 30 || al.y < -30) {
          alienLasers.splice(i, 1);
        }
      }

      // 7. Powerup Items (❤️ Heart pickups)
      for (let i = powerups.length - 1; i >= 0; i--) {
        const p = powerups[i];
        p.y += p.vy;
        p.bob += 0.06;

        // Collect Heart
        const dist = Math.hypot(p.x - player.x, p.y - player.y);
        if (dist < 22) {
          restorePlayerHp();
          powerups.splice(i, 1);
          continue;
        }

        if (p.y > H + 30) {
          powerups.splice(i, 1);
        }
      }

      // 8. Explosion Particles Update
      for (let i = explosions.length - 1; i >= 0; i--) {
        const exp = explosions[i];
        exp.x += exp.vx;
        exp.y += exp.vy;
        exp.alpha -= exp.decay;
        if (exp.alpha <= 0) {
          explosions.splice(i, 1);
        }
      }

      // 9. Floating Score Popups Update
      for (let i = scorePopups.length - 1; i >= 0; i--) {
        const pop = scorePopups[i];
        pop.y += pop.vy;
        pop.alpha -= 0.025;
        if (pop.alpha <= 0) {
          scorePopups.splice(i, 1);
        }
      }

      if (screenShake > 0) screenShake *= 0.88;
    }

    // MAIN GAME RENDER LOOP (60 FPS)
    function renderGame() {
      ctx.save();

      // Screen Shake on impact
      if (screenShake > 0.5) {
        const shakeX = (Math.random() - 0.5) * screenShake;
        const shakeY = (Math.random() - 0.5) * screenShake;
        ctx.translate(shakeX, shakeY);
      }

      // Clear Black Background
      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, W, H);

      // 1. Draw Starfield
      for (let i = 0; i < bgStars.length; i++) {
        const s = bgStars[i];
        ctx.fillStyle = s.color;
        ctx.globalAlpha = s.alpha;
        ctx.fillRect(Math.floor(s.x), Math.floor(s.y), s.size, s.size);
      }
      ctx.globalAlpha = 1.0;

      // 2. Draw Player Fighter Ship (with Invulnerability Flicker)
      if (isPlaying) {
        const showPlayer = player.invulnTimer <= 0 || Math.floor(player.invulnTimer / 6) % 2 === 0;
        if (showPlayer) {
          const px = Math.floor(player.x - player.width / 2);
          const py = Math.floor(player.y - player.height / 2);

          // Draw Ship
          drawPixelBitmap(PLAYER_SPRITE, px, py, player.pixelSize, 1.0);

          // Draw Thruster Flame Glow
          const flameColor = player.thrusterFrame < 3 ? '#ff9e00' : '#00e5ff';
          ctx.fillStyle = flameColor;
          ctx.fillRect(player.x - 3, py + player.height - 2, 6, 8);
        }
      }

      // 3. Draw Player Lasers
      for (let i = 0; i < playerLasers.length; i++) {
        const l = playerLasers[i];
        ctx.save();
        ctx.fillStyle = l.color;
        ctx.shadowColor = l.color;
        ctx.shadowBlur = 8;
        ctx.fillRect(Math.floor(l.x - l.width / 2), Math.floor(l.y), l.width, l.height);
        ctx.restore();
      }

      // 4. Draw Alien Ships
      for (let i = 0; i < alienShips.length; i++) {
        const a = alienShips[i];
        const ax = Math.floor(a.x - a.width / 2);
        const ay = Math.floor(a.y - a.height / 2);
        drawPixelBitmap(a.sprite, ax, ay, a.pixelSize, 1.0);

        // HP Bar for Cruisers
        if (a.type === 'cruiser' && a.hp < a.maxHp) {
          ctx.fillStyle = 'rgba(0,0,0,0.6)';
          ctx.fillRect(ax, ay - 6, a.width, 3);
          ctx.fillStyle = '#ff2a5f';
          ctx.fillRect(ax, ay - 6, (a.width * a.hp) / a.maxHp, 3);
        }
      }

      // 5. Draw Slower Alien Lasers (Glowing Plasma Orbs)
      for (let i = 0; i < alienLasers.length; i++) {
        const al = alienLasers[i];
        ctx.save();
        ctx.beginPath();
        ctx.arc(al.x, al.y, al.radius, 0, Math.PI * 2);
        ctx.fillStyle = al.color;
        ctx.shadowColor = al.color;
        ctx.shadowBlur = 10;
        ctx.fill();

        // White core
        ctx.beginPath();
        ctx.arc(al.x, al.y, al.radius * 0.5, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();
        ctx.restore();
      }

      // 6. Draw Power-Up Items (❤️ Health Pickups)
      for (let i = 0; i < powerups.length; i++) {
        const p = powerups[i];
        const renderY = p.y + Math.sin(p.bob) * 4;
        drawPixelBitmap(HEART_ITEM_SPRITE, Math.floor(p.x - 12), Math.floor(renderY - 10), 3, 1.0);
      }

      // 7. Draw Explosion Particles
      for (let i = 0; i < explosions.length; i++) {
        const exp = explosions[i];
        ctx.save();
        ctx.fillStyle = exp.color;
        ctx.globalAlpha = Math.max(0, exp.alpha);
        ctx.fillRect(Math.floor(exp.x), Math.floor(exp.y), exp.size, exp.size);
        ctx.restore();
      }

      // 8. Draw Score Popups (Pixel Text)
      ctx.font = "bold 13px 'JetBrains Mono', monospace";
      for (let i = 0; i < scorePopups.length; i++) {
        const pop = scorePopups[i];
        ctx.save();
        ctx.globalAlpha = Math.max(0, pop.alpha);
        ctx.fillStyle = pop.color;
        ctx.shadowColor = '#000000';
        ctx.shadowBlur = 4;
        ctx.fillText(pop.text, pop.x, pop.y);
        ctx.restore();
      }

      ctx.restore();
    }

    // Animation Frame Loop
    function gameLoop() {
      updateGame();
      renderGame();
      requestAnimationFrame(gameLoop);
    }

    // Initial Setup
    resizeGame();
    initBgStars();
    updateHeartsHUD();
    requestAnimationFrame(gameLoop);
  })();
  </script>
"""

# Replace previous background VFX script or insert Minigame engine
if '<!-- ===== 2D PIXEL GAME ART & SCROLL-REACTIVE VFX ENGINE ===== -->' in content:
    content = re.sub(
        r'<!-- ===== 2D PIXEL GAME ART & SCROLL-REACTIVE VFX ENGINE ===== -->\s*<script>.*?</script>',
        minigame_engine_js.strip(),
        content,
        flags=re.DOTALL
    )
elif '<!-- ===== VOID FIGHTER PLAYABLE MINIGAME ENGINE ===== -->' in content:
    content = re.sub(
        r'<!-- ===== VOID FIGHTER PLAYABLE MINIGAME ENGINE ===== -->\s*<script>.*?</script>',
        minigame_engine_js.strip(),
        content,
        flags=re.DOTALL
    )
else:
    content = content.replace('</body>', minigame_engine_js + '\n</body>')

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully added Veira Void Fighter Spaceship minigame with 3 HP hearts & alien combat!')
