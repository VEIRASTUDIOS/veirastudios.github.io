import re

HTML_PATH = '/Users/albinkrasniqi/Desktop/SITE/index.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS for Pixel Art Game Canvas and pitch-black styling
pixel_canvas_css = """
    /* ===== 2D RETRO PIXEL ART GAME VFX STYLING ===== */
    #vfx-pixel-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 1;
      image-rendering: pixelated;
      image-rendering: -moz-crisp-edges;
      image-rendering: crisp-edges;
    }

    body {
      background-color: #000000 !important;
      position: relative;
    }

    /* Ambient lighting optimized for deep obsidian & crisp pixel contrast */
    .apple-ambient-mesh {
      opacity: 0.18;
    }

    .bg-grid-pattern {
      opacity: 0.5;
    }
"""

# Replace old canvas CSS or insert new
if '#vfx-pixel-canvas' not in content:
    if '#vfx-particles-canvas' in content:
        # Replace previous canvas styling
        content = re.sub(r'/\* ===== PITCH BLACK & WHITE VFX CANVAS STYLING ===== \*/.*?\.bg-grid-pattern\s*\{\s*opacity:\s*0\.6;\s*\}', pixel_canvas_css.strip(), content, flags=re.DOTALL)
    else:
        content = content.replace('  </style>', pixel_canvas_css + '\n  </style>')

# 2. Update Canvas HTML Element
if '<canvas id="vfx-pixel-canvas"></canvas>' not in content:
    if '<canvas id="vfx-particles-canvas"></canvas>' in content:
        content = content.replace('<canvas id="vfx-particles-canvas"></canvas>', '<canvas id="vfx-pixel-canvas"></canvas>')
        content = content.replace('<!-- White Particles & Animated Scroll Lines VFX Canvas -->', '<!-- 2D Pixel Game Art VFX Canvas -->')
    else:
        content = content.replace('<body>', '<body>\n  <!-- 2D Pixel Game Art VFX Canvas -->\n  <canvas id="vfx-pixel-canvas"></canvas>')

# 3. Complete 2D Pixel Game Art & Scroll-Reactive Engine JS
pixel_engine_js = """
  <!-- ===== 2D PIXEL GAME ART & SCROLL-REACTIVE VFX ENGINE ===== -->
  <script>
  (function() {
    'use strict';
    const canvas = document.getElementById('vfx-pixel-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.imageSmoothingEnabled = false;

    let width = 0;
    let height = 0;
    let dpr = 1;
    let animId = null;

    // Smooth scroll velocity tracking
    let currentScrollY = window.scrollY || window.pageYOffset || 0;
    let targetScrollY = currentScrollY;
    let lastReportedScrollY = currentScrollY;
    let smoothedScrollVelocity = 0;
    let scrollDir = 1;
    let lastScrollTime = performance.now();

    // Mouse tracking
    const mouse = {
      x: -9999,
      y: -9999,
      targetX: -9999,
      targetY: -9999,
      active: false
    };

    // Color palette mapping
    const PALETTE = {
      W: '#ffffff', // Crisp White
      G: '#ffd700', // Gold
      O: '#ff9e00', // Orange Gold
      D: '#b36b00', // Dark Bronze / Gold Shade
      K: '#0d0f14', // Pixel Outline Black
      C: '#00e5ff', // Neon Cyan
      B: '#0066ff', // Electric Blue
      R: '#ff2a5f', // Crimson / Ruby Red
      P: '#ff77a8', // Pink Glint
      M: '#00ff9d', // Mint Green
      E: '#d1d5db', // Silver / Light Gray
      S: '#475569', // Dark Slate
      V: '#a855f7', // Mystic Purple
      L: '#d8b4fe', // Light Lavender
      Y: '#facc15'  // Bright Yellow
    };

    // 1. Pixel Coin (4 Animation Frames)
    const SPRITE_COIN = [
      [
        ['_','K','K','K','K','_'],
        ['K','G','W','G','G','K'],
        ['K','G','G','G','D','K'],
        ['K','G','G','D','D','K'],
        ['K','G','D','D','D','K'],
        ['_','K','K','K','K','_'],
      ],
      [
        ['_','K','K','K','_','_'],
        ['K','G','W','G','K','_'],
        ['K','G','G','D','K','_'],
        ['K','G','D','D','K','_'],
        ['K','G','D','D','K','_'],
        ['_','K','K','K','_','_'],
      ],
      [
        ['_','_','K','K','_','_'],
        ['_','_','K','W','K','_'],
        ['_','_','K','G','K','_'],
        ['_','_','K','G','K','_'],
        ['_','_','K','D','K','_'],
        ['_','_','K','K','_','_'],
      ],
      [
        ['_','_','K','K','K','_'],
        ['_','K','G','W','G','K'],
        ['_','K','G','G','D','K'],
        ['_','K','G','D','D','K'],
        ['_','K','G','D','D','K'],
        ['_','_','K','K','K','_'],
      ]
    ];

    // 2. Pixel Heart (8x7)
    const SPRITE_HEART = [
      ['_','K','K','_','_','K','K','_'],
      ['K','P','W','K','K','P','W','K'],
      ['K','R','P','R','R','R','R','K'],
      ['K','R','R','R','R','R','R','K'],
      ['_','K','R','R','R','R','K','_'],
      ['_','_','K','R','R','K','_','_'],
      ['_','_','_','K','K','_','_','_']
    ];

    // 3. Pixel Cyan Mana Gem (7x7)
    const SPRITE_GEM = [
      ['_','_','_','K','_','_','_'],
      ['_','_','K','W','K','_','_'],
      ['_','K','W','C','C','K','_'],
      ['K','W','C','C','B','B','K'],
      ['_','K','C','B','B','K','_'],
      ['_','_','K','B','K','_','_'],
      ['_','_','_','K','_','_','_']
    ];

    // 4. Pixel 8-Bit Power Star (7x7)
    const SPRITE_STAR = [
      ['_','_','_','K','_','_','_'],
      ['_','_','K','W','K','_','_'],
      ['K','K','G','W','G','K','K'],
      ['_','K','G','G','G','K','_'],
      ['K','K','G','G','G','K','K'],
      ['_','K','D','_','D','K','_'],
      ['_','K','_','_','_','K','_']
    ];

    // 5. Pixel Gamepad Controller (10x6)
    const SPRITE_CONTROLLER = [
      ['_','K','K','K','K','K','K','K','K','_'],
      ['K','S','S','S','S','S','S','S','S','K'],
      ['K','S','W','S','S','S','R','S','C','K'],
      ['K','W','W','W','S','S','S','Y','S','K'],
      ['K','S','W','S','S','S','M','S','S','K'],
      ['_','K','K','_','_','_','_','K','K','_']
    ];

    // 6. Pixel Mana Potion (7x9)
    const SPRITE_POTION = [
      ['_','_','K','W','K','_','_'],
      ['_','_','K','S','K','_','_'],
      ['_','K','K','K','K','K','_'],
      ['K','E','W','E','E','E','K'],
      ['K','C','W','C','C','C','K'],
      ['K','B','C','C','C','B','K'],
      ['K','B','B','C','B','B','K'],
      ['K','K','B','B','B','K','K'],
      ['_','_','K','K','K','_','_']
    ];

    // 7. Pixel Sci-Fi Combat Ship (9x9) with Animated Thruster
    const SPRITE_SHIP = [
      ['_','_','_','_','K','_','_','_','_'],
      ['_','_','_','K','W','K','_','_','_'],
      ['_','_','_','K','C','K','_','_','_'],
      ['_','_','K','C','C','C','K','_','_'],
      ['_','K','E','C','C','C','E','K','_'],
      ['K','E','E','C','B','C','E','E','K'],
      ['K','E','C','B','B','B','C','E','K'],
      ['K','K','C','K','K','K','C','K','K'],
      ['_','K','K','_','_','_','K','K','_']
    ];

    const SPRITE_SHIP_FLAME = [
      [
        ['_','_','_','_','_','_','_','_','_'],
        ['_','_','_','_','O','_','_','_','_'],
        ['_','_','_','O','Y','O','_','_','_'],
        ['_','_','_','_','Y','_','_','_','_'],
        ['_','_','_','_','W','_','_','_','_']
      ],
      [
        ['_','_','_','_','_','_','_','_','_'],
        ['_','_','_','O','O','O','_','_','_'],
        ['_','_','_','_','Y','_','_','_','_'],
        ['_','_','_','_','W','_','_','_','_']
      ]
    ];

    // 8. Pixel 8-Bit Sword (8x8)
    const SPRITE_SWORD = [
      ['_','_','_','_','_','_','W','K'],
      ['_','_','_','_','_','W','E','K'],
      ['_','_','_','_','W','E','K','_'],
      ['_','_','_','W','E','K','_','_'],
      ['_','K','G','E','K','_','_','_'],
      ['K','C','G','K','_','_','_','_'],
      ['K','G','C','K','_','_','_','_'],
      ['_','K','K','_','_','_','_','_']
    ];

    // 9. Pixel Loot Chest (8x7)
    const SPRITE_CHEST = [
      ['_','K','K','K','K','K','K','_'],
      ['K','D','G','G','G','G','D','K'],
      ['K','G','K','G','G','K','G','K'],
      ['K','K','K','G','G','K','K','K'],
      ['K','D','D','G','G','D','D','K'],
      ['K','D','D','D','D','D','D','K'],
      ['_','K','K','K','K','K','K','_']
    ];

    // Draw helper: renders a 2D bitmap matrix with square pixels
    function drawPixelBitmap(matrix, startX, startY, pixelSize, alpha = 1.0) {
      if (!matrix || !matrix.length) return;
      ctx.save();
      ctx.globalAlpha = alpha;
      const rows = matrix.length;
      for (let r = 0; r < rows; r++) {
        const row = matrix[r];
        const cols = row.length;
        for (let c = 0; c < cols; c++) {
          const colorKey = row[c];
          if (colorKey && colorKey !== '_' && PALETTE[colorKey]) {
            ctx.fillStyle = PALETTE[colorKey];
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

    // Mini 3x5 Pixel Font Engine
    const PIXEL_FONT = {
      '0': ['111','101','101','101','111'],
      '1': ['010','110','010','010','111'],
      '2': ['111','001','111','100','111'],
      '3': ['111','001','111','001','111'],
      '4': ['101','101','111','001','001'],
      '5': ['111','100','111','001','111'],
      '6': ['111','100','111','101','111'],
      '7': ['111','001','010','010','010'],
      '8': ['111','101','111','101','111'],
      '9': ['111','101','111','001','111'],
      '+': ['000','010','111','010','000'],
      '-': ['000','000','111','000','000'],
      'X': ['101','101','010','101','101'],
      'P': ['111','101','111','100','100'],
      'L': ['100','100','100','100','111'],
      'V': ['101','101','101','101','010'],
      'U': ['101','101','101','101','111'],
      'C': ['111','100','100','100','111'],
      'R': ['111','101','111','110','101'],
      'I': ['111','010','010','010','111'],
      'T': ['111','010','010','010','010'],
      '!': ['010','010','010','000','010'],
      ' ': ['000','000','000','000','000']
    };

    function drawPixelText(text, startX, startY, pixelSize, color, alpha = 1.0) {
      ctx.save();
      ctx.globalAlpha = alpha;
      let curX = startX;
      const upper = String(text).toUpperCase();

      for (let i = 0; i < upper.length; i++) {
        const char = upper[i];
        const glyph = PIXEL_FONT[char] || PIXEL_FONT[' '];
        
        // Draw shadow first
        ctx.fillStyle = '#000000';
        for (let r = 0; r < 5; r++) {
          for (let c = 0; c < 3; c++) {
            if (glyph[r][c] === '1') {
              ctx.fillRect(
                Math.floor(curX + c * pixelSize + pixelSize),
                Math.floor(startY + r * pixelSize + pixelSize),
                pixelSize,
                pixelSize
              );
            }
          }
        }

        // Draw foreground
        ctx.fillStyle = color;
        for (let r = 0; r < 5; r++) {
          for (let c = 0; c < 3; c++) {
            if (glyph[r][c] === '1') {
              ctx.fillRect(
                Math.floor(curX + c * pixelSize),
                Math.floor(startY + r * pixelSize),
                pixelSize,
                pixelSize
              );
            }
          }
        }
        curX += 4 * pixelSize;
      }
      ctx.restore();
    }

    // Entities Arrays
    let pixelStars = [];
    let gameSprites = [];
    let pixelPopups = [];
    let pixelPuffs = [];
    let pixelSparks = [];
    let pixelSpeedStreaks = [];

    // 1. Retro Pixel Stars (Background Starfield)
    class PixelStar {
      constructor() {
        this.reset(true);
      }

      reset(initial = false) {
        this.x = Math.random() * width;
        this.y = initial ? Math.random() * height : (scrollDir >= 0 ? height + 10 : -10);
        this.type = Math.random() < 0.2 ? 'cross' : (Math.random() < 0.5 ? 'med' : 'tiny');
        this.pixelSize = this.type === 'cross' ? 2 : (this.type === 'med' ? 2 : 1);
        this.baseSpeedY = -Math.random() * 0.2 - 0.05;
        this.parallax = this.type === 'cross' ? 0.25 : 0.08;
        this.twinklePhase = Math.random() * Math.PI * 2;
        this.twinkleSpeed = Math.random() * 0.03 + 0.01;
      }

      update(scrollVel) {
        this.twinklePhase += this.twinkleSpeed;
        this.y += this.baseSpeedY - scrollVel * this.parallax;

        if (this.x < -10) this.x = width + 10;
        if (this.x > width + 10) this.x = -10;
        if (this.y < -20) this.y = height + 20;
        if (this.y > height + 20) this.y = -20;
      }

      draw() {
        // Step brightness to authentic 8-bit levels
        const raw = (Math.sin(this.twinklePhase) + 1) * 0.5;
        const stepAlpha = raw < 0.33 ? 0.25 : (raw < 0.66 ? 0.6 : 0.95);
        ctx.save();
        ctx.fillStyle = `rgba(255, 255, 255, ${stepAlpha})`;

        const px = Math.floor(this.x);
        const py = Math.floor(this.y);
        const s = this.pixelSize;

        if (this.type === 'cross') {
          // 4-pointed cross star
          ctx.fillRect(px, py - s, s, s);
          ctx.fillRect(px - s, py, s * 3, s);
          ctx.fillRect(px, py + s, s, s);
        } else if (this.type === 'med') {
          ctx.fillRect(px, py, s * 2, s * 2);
        } else {
          ctx.fillRect(px, py, s, s);
        }
        ctx.restore();
      }
    }

    // 2. Floating 2D Game Sprites (Coins, Gems, Ships, Hearts, Stars, Potions, Controllers, Chests)
    class GameSprite {
      constructor(type, x, y) {
        this.type = type;
        this.x = x || Math.random() * width;
        this.y = y || Math.random() * height;
        this.pixelSize = Math.random() < 0.4 ? 3 : 2;
        this.baseSpeedX = (Math.random() - 0.5) * 0.4;
        this.baseSpeedY = -Math.random() * 0.35 - 0.15;
        this.parallax = this.pixelSize === 3 ? 0.38 : 0.22;
        
        this.bobPhase = Math.random() * Math.PI * 2;
        this.bobSpeed = Math.random() * 0.03 + 0.02;
        this.bobAmp = Math.random() * 14 + 8;
        
        this.animFrame = 0;
        this.animTimer = 0;
        this.alpha = Math.random() * 0.25 + 0.75;
      }

      update(scrollVel) {
        this.bobPhase += this.bobSpeed;
        this.animTimer++;
        if (this.animTimer > 8) {
          this.animTimer = 0;
          this.animFrame = (this.animFrame + 1) % 4;
        }

        // Parallax vertical movement
        this.x += this.baseSpeedX;
        this.y += this.baseSpeedY - scrollVel * this.parallax;

        // If it's a ship and we are scrolling fast, emit pixel thruster smoke
        if (this.type === 'ship' && Math.abs(scrollVel) > 1.2 && Math.random() < 0.35) {
          pixelPuffs.push(new PixelPuff(
            this.x + 4 * this.pixelSize,
            this.y + 9 * this.pixelSize,
            (Math.random() - 0.5) * 1.5,
            Math.random() * 2 + 1,
            Math.random() < 0.5 ? '#ff9e00' : '#00e5ff'
          ));
        }

        // Screen wrap
        if (this.x < -60) this.x = width + 60;
        if (this.x > width + 60) this.x = -60;
        if (this.y < -80) this.y = height + 80;
        if (this.y > height + 80) this.y = -80;
      }

      draw(scrollVel) {
        const renderY = this.y + Math.sin(this.bobPhase) * this.bobAmp;
        const renderX = Math.floor(this.x);
        const ry = Math.floor(renderY);

        switch (this.type) {
          case 'coin':
            drawPixelBitmap(SPRITE_COIN[this.animFrame], renderX, ry, this.pixelSize, this.alpha);
            break;
          case 'heart':
            drawPixelBitmap(SPRITE_HEART, renderX, ry, this.pixelSize, this.alpha);
            break;
          case 'gem':
            drawPixelBitmap(SPRITE_GEM, renderX, ry, this.pixelSize, this.alpha);
            break;
          case 'star':
            drawPixelBitmap(SPRITE_STAR, renderX, ry, this.pixelSize, this.alpha);
            break;
          case 'controller':
            drawPixelBitmap(SPRITE_CONTROLLER, renderX, ry, this.pixelSize, this.alpha);
            break;
          case 'potion':
            drawPixelBitmap(SPRITE_POTION, renderX, ry, this.pixelSize, this.alpha);
            break;
          case 'sword':
            drawPixelBitmap(SPRITE_SWORD, renderX, ry, this.pixelSize, this.alpha);
            break;
          case 'chest':
            drawPixelBitmap(SPRITE_CHEST, renderX, ry, this.pixelSize, this.alpha);
            break;
          case 'ship':
            drawPixelBitmap(SPRITE_SHIP, renderX, ry, this.pixelSize, this.alpha);
            // Draw animated thruster flame behind ship
            const flameFrame = Math.abs(scrollVel) > 1.5 ? (Math.random() < 0.5 ? 0 : 1) : (this.animFrame % 2);
            drawPixelBitmap(SPRITE_SHIP_FLAME[flameFrame], renderX, ry + 7 * this.pixelSize, this.pixelSize, this.alpha);
            break;
        }
      }
    }

    // 3. Floating Retro RPG Popup Text ("+100 XP", "CRIT!", "LEVEL UP", "+500")
    class PixelPopup {
      constructor(text, x, y, color) {
        this.text = text;
        this.x = x;
        this.y = y;
        this.color = color || '#ffd700';
        this.pixelSize = 2;
        this.vy = -1.8;
        this.alpha = 1.0;
        this.life = 0;
        this.maxLife = 55;
      }

      update() {
        this.y += this.vy;
        this.vy *= 0.95;
        this.life++;
        if (this.life > 30) {
          this.alpha -= 0.04;
        }
      }

      draw() {
        if (this.alpha <= 0) return;
        drawPixelText(this.text, this.x, this.y, this.pixelSize, this.color, this.alpha);
      }
    }

    // 4. Pixel Dust & Smoke Puffs
    class PixelPuff {
      constructor(x, y, vx, vy, color) {
        this.x = x;
        this.y = y;
        this.vx = vx || (Math.random() - 0.5) * 1.5;
        this.vy = vy || (Math.random() - 0.5) * 1.5;
        this.color = color || '#ffffff';
        this.size = Math.random() < 0.5 ? 3 : 2;
        this.alpha = 0.9;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;
        this.alpha -= 0.035;
      }

      draw() {
        if (this.alpha <= 0) return;
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.globalAlpha = this.alpha;
        const s = this.size;
        ctx.fillRect(Math.floor(this.x), Math.floor(this.y), s * 2, s * 2);
        ctx.restore();
      }
    }

    // 5. Pixel Exploding Spark Particles (On Click / Level Burst)
    class PixelSpark {
      constructor(x, y, color) {
        this.x = x;
        this.y = y;
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 4.5 + 1.5;
        this.vx = Math.cos(angle) * speed;
        this.vy = Math.sin(angle) * speed;
        this.color = color || '#ffd700';
        this.size = Math.random() < 0.5 ? 3 : 2;
        this.alpha = 1.0;
        this.gravity = 0.12;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;
        this.vy += this.gravity;
        this.alpha -= 0.028;
      }

      draw() {
        if (this.alpha <= 0) return;
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.globalAlpha = this.alpha;
        ctx.fillRect(Math.floor(this.x), Math.floor(this.y), this.size, this.size);
        ctx.restore();
      }
    }

    // 6. Pixel Speed Dash Lines on Scrolling
    class PixelSpeedStreak {
      constructor(scrollDelta) {
        this.x = Math.random() * width;
        this.y = scrollDelta >= 0 ? -30 : height + 30;
        this.speed = (Math.random() * 12 + 16) * Math.sign(scrollDelta);
        this.len = Math.floor(Math.random() * 4 + 3); // Number of pixel blocks
        this.pixelSize = 3;
        this.alpha = 0.85;
        this.color = Math.random() < 0.4 ? '#00e5ff' : (Math.random() < 0.5 ? '#ffffff' : '#ffd700');
      }

      update() {
        this.y += this.speed;
        this.alpha -= 0.035;
      }

      draw() {
        if (this.alpha <= 0) return;
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.globalAlpha = this.alpha;
        const s = this.pixelSize;
        const px = Math.floor(this.x);
        const py = Math.floor(this.y);
        
        for (let i = 0; i < this.len; i++) {
          const stepAlpha = (1 - i / this.len) * this.alpha;
          ctx.globalAlpha = stepAlpha;
          ctx.fillRect(px, py - i * s * Math.sign(this.speed), s, s);
        }
        ctx.restore();
      }
    }

    // Click anywhere for a game dev retro 2D pixel burst!
    window.addEventListener('click', (e) => {
      const phrases = ['+100 XP', 'LEVEL UP!', 'CRIT!', '+500', 'COMBO x2', 'MAX!', 'DEV MODE'];
      const text = phrases[Math.floor(Math.random() * phrases.length)];
      const colors = ['#ffd700', '#00e5ff', '#00ff9d', '#ff2a5f', '#ff9e00', '#ffffff'];
      const color = colors[Math.floor(Math.random() * colors.length)];

      pixelPopups.push(new PixelPopup(text, e.clientX - 25, e.clientY - 15, color));

      // Spawn 14 pixel spark debris
      for (let i = 0; i < 14; i++) {
        pixelSparks.push(new PixelSpark(e.clientX, e.clientY, color));
      }
      
      // Spawn pixel puffs
      for (let i = 0; i < 5; i++) {
        pixelPuffs.push(new PixelPuff(e.clientX, e.clientY, (Math.random() - 0.5) * 3, (Math.random() - 0.5) * 3, '#ffffff'));
      }
    });

    // Mouse Move & Sparkles
    window.addEventListener('mousemove', (e) => {
      mouse.targetX = e.clientX;
      mouse.targetY = e.clientY;
      mouse.active = true;

      // Leave trailing micro pixel sparkles
      if (Math.random() < 0.35) {
        pixelPuffs.push(new PixelPuff(
          e.clientX + (Math.random() - 0.5) * 16,
          e.clientY + (Math.random() - 0.5) * 16,
          (Math.random() - 0.5) * 0.8,
          -Math.random() * 1.2,
          Math.random() < 0.5 ? '#00e5ff' : '#ffd700'
        ));
      }
    }, { passive: true });

    // Scroll Handler
    window.addEventListener('scroll', () => {
      targetScrollY = window.scrollY || window.pageYOffset || 0;
      const rawDelta = targetScrollY - lastReportedScrollY;
      lastReportedScrollY = targetScrollY;

      if (Math.abs(rawDelta) > 0.5) {
        scrollDir = Math.sign(rawDelta);
      }

      // Fast scroll reactions
      if (Math.abs(rawDelta) > 16) {
        if (pixelSpeedStreaks.length < 8) {
          pixelSpeedStreaks.push(new PixelSpeedStreak(rawDelta));
        }

        if (Math.random() < 0.25) {
          const words = ['+50 XP', '+200 XP', 'BOOST!'];
          pixelPopups.push(new PixelPopup(
            words[Math.floor(Math.random() * words.length)],
            Math.random() * (width - 150) + 50,
            Math.random() * (height - 100) + 50,
            '#00ff9d'
          ));
        }
      }
    }, { passive: true });

    // Canvas Resize
    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr, dpr);
      ctx.imageSmoothingEnabled = false;

      initSprites();
    }

    function initSprites() {
      pixelStars = [];
      gameSprites = [];

      // 1. Background pixel stars
      const starCount = Math.min(Math.floor((width * height) / 16000), 65);
      for (let i = 0; i < starCount; i++) {
        pixelStars.push(new PixelStar());
      }

      // 2. 2D Retro Game Collectibles / Sprites
      const types = ['coin', 'gem', 'star', 'heart', 'ship', 'controller', 'potion', 'sword', 'chest'];
      const totalSprites = Math.min(Math.floor((width * height) / 45000), 24);

      for (let i = 0; i < totalSprites; i++) {
        const type = types[i % types.length];
        gameSprites.push(new GameSprite(type));
      }
    }

    // Main 60-120 FPS Render Loop
    function animate() {
      // Smooth scroll interpolation
      const scrollDiff = targetScrollY - currentScrollY;
      currentScrollY += scrollDiff * 0.12;
      const instantVelocity = scrollDiff * 0.12;
      smoothedScrollVelocity += (instantVelocity - smoothedScrollVelocity) * 0.15;
      const scrollVel = smoothedScrollVelocity;

      // Clear frame
      ctx.clearRect(0, 0, width, height);

      // 1. Update & Draw Background Pixel Stars
      for (let i = 0; i < pixelStars.length; i++) {
        pixelStars[i].update(scrollVel);
        pixelStars[i].draw();
      }

      // 2. Update & Draw Pixel Speed Streaks
      for (let i = pixelSpeedStreaks.length - 1; i >= 0; i--) {
        const s = pixelSpeedStreaks[i];
        s.update();
        s.draw();
        if (s.alpha <= 0 || s.y < -100 || s.y > height + 100) {
          pixelSpeedStreaks.splice(i, 1);
        }
      }

      // 3. Update & Draw 2D Game Sprites (Coins, Gems, Ships, Hearts, etc.)
      for (let i = 0; i < gameSprites.length; i++) {
        gameSprites[i].update(scrollVel);
        gameSprites[i].draw(scrollVel);
      }

      // 4. Update & Draw Pixel Dust Puffs
      for (let i = pixelPuffs.length - 1; i >= 0; i--) {
        const p = pixelPuffs[i];
        p.update();
        p.draw();
        if (p.alpha <= 0) {
          pixelPuffs.splice(i, 1);
        }
      }

      // 5. Update & Draw Exploding Pixel Sparks
      for (let i = pixelSparks.length - 1; i >= 0; i--) {
        const sp = pixelSparks[i];
        sp.update();
        sp.draw();
        if (sp.alpha <= 0 || sp.y > height + 50) {
          pixelSparks.splice(i, 1);
        }
      }

      // 6. Update & Draw Floating Retro RPG Text Popups
      for (let i = pixelPopups.length - 1; i >= 0; i--) {
        const pop = pixelPopups[i];
        pop.update();
        pop.draw();
        if (pop.alpha <= 0) {
          pixelPopups.splice(i, 1);
        }
      }

      animId = requestAnimationFrame(animate);
    }

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        if (animId) cancelAnimationFrame(animId);
      } else {
        lastScrollTime = performance.now();
        animId = requestAnimationFrame(animate);
      }
    });

    resize();
    window.addEventListener('resize', resize, { passive: true });
    animId = requestAnimationFrame(animate);
  })();
  </script>
"""

# Replace the previous VFX engine script with the new pixel art engine
if '<!-- ===== WHITE PARTICLES & SCROLL-REACTIVE VFX ENGINE ===== -->' in content:
    content = re.sub(
        r'<!-- ===== WHITE PARTICLES & SCROLL-REACTIVE VFX ENGINE ===== -->\s*<script>.*?</script>',
        pixel_engine_js.strip(),
        content,
        flags=re.DOTALL
    )
elif '<!-- ===== 2D PIXEL GAME ART & SCROLL-REACTIVE VFX ENGINE ===== -->' in content:
    content = re.sub(
        r'<!-- ===== 2D PIXEL GAME ART & SCROLL-REACTIVE VFX ENGINE ===== -->\s*<script>.*?</script>',
        pixel_engine_js.strip(),
        content,
        flags=re.DOTALL
    )
else:
    content = content.replace('</body>', pixel_engine_js + '\n</body>')

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully applied 2D Pixel Game Art effects and scroll reactions to index.html!')
