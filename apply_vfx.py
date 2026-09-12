import re

HTML_PATH = '/Users/albinkrasniqi/Desktop/SITE/index.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS tokens and canvas styling
canvas_css = """
    /* ===== PITCH BLACK & WHITE VFX CANVAS STYLING ===== */
    #vfx-particles-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 1;
    }

    body {
      background-color: #000000 !important;
      position: relative;
    }

    /* Ambient lighting optimized for deep obsidian contrast */
    .apple-ambient-mesh {
      opacity: 0.25;
    }

    .bg-grid-pattern {
      opacity: 0.6;
    }
"""

# Insert canvas CSS before </style>
if '#vfx-particles-canvas' not in content:
    content = content.replace('  </style>', canvas_css + '\n  </style>')

# 2. Insert canvas element right after <body>
canvas_html = '  <!-- White Particles & Animated Scroll Lines VFX Canvas -->\n  <canvas id="vfx-particles-canvas"></canvas>'
if '<canvas id="vfx-particles-canvas"></canvas>' not in content:
    content = content.replace('<body>', '<body>\n' + canvas_html)

# 3. Add the complete VFX animation engine before </body>
vfx_engine_js = """
  <!-- ===== WHITE PARTICLES & SCROLL-REACTIVE VFX ENGINE ===== -->
  <script>
  (function() {
    'use strict';
    const canvas = document.getElementById('vfx-particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let width = 0;
    let height = 0;
    let dpr = 1;
    let particles = [];
    let meteors = [];
    let waveLines = [];
    let animId = null;

    // Smooth scroll velocity tracking
    let currentScrollY = window.scrollY || window.pageYOffset || 0;
    let targetScrollY = currentScrollY;
    let lastReportedScrollY = currentScrollY;
    let smoothedScrollVelocity = 0;
    let scrollVelocityDamped = 0;
    let scrollDir = 1;
    let lastScrollTime = performance.now();

    // Mouse tracking with inertia
    const mouse = {
      x: -9999,
      y: -9999,
      targetX: -9999,
      targetY: -9999,
      radius: 160,
      active: false
    };

    window.addEventListener('mousemove', (e) => {
      mouse.targetX = e.clientX;
      mouse.targetY = e.clientY;
      mouse.active = true;
    }, { passive: true });

    window.addEventListener('mouseleave', () => {
      mouse.active = false;
      mouse.targetX = -9999;
      mouse.targetY = -9999;
    }, { passive: true });

    // Window scroll handler
    window.addEventListener('scroll', () => {
      targetScrollY = window.scrollY || window.pageYOffset || 0;
      const now = performance.now();
      const dt = Math.max(1, now - lastScrollTime);
      lastScrollTime = now;
      
      const rawDelta = targetScrollY - lastReportedScrollY;
      lastReportedScrollY = targetScrollY;
      
      if (Math.abs(rawDelta) > 0.5) {
        scrollDir = Math.sign(rawDelta);
      }

      // Fast scroll burst: spawn luminous shooting star / warp trail
      if (Math.abs(rawDelta) > 22 && Math.random() < 0.4) {
        spawnMeteor(rawDelta);
      }
    }, { passive: true });

    // Responsive Canvas Resizing
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

      initParticles();
      initWaveLines();
    }

    // Particle Object (Multi-tier visual depth)
    class WhiteParticle {
      constructor(layer) {
        this.layer = layer; // 0: Deep Star Dust, 1: Constellation Node, 2: Foreground Spark
        this.reset(true);
      }

      reset(initial = false) {
        this.x = Math.random() * width;
        if (initial) {
          this.y = Math.random() * height;
        } else {
          this.y = scrollDir >= 0 ? height + 10 : -10;
        }

        if (this.layer === 0) {
          // Deep ambient stars
          this.size = Math.random() * 0.9 + 0.6;
          this.baseSpeedX = (Math.random() - 0.5) * 0.12;
          this.baseSpeedY = (Math.random() - 0.5) * 0.18 - 0.06;
          this.baseAlpha = Math.random() * 0.4 + 0.15;
          this.twinkleSpeed = Math.random() * 0.02 + 0.008;
          this.parallax = 0.08;
        } else if (this.layer === 1) {
          // Midground constellation node
          this.size = Math.random() * 1.5 + 1.2;
          this.baseSpeedX = (Math.random() - 0.5) * 0.3;
          this.baseSpeedY = (Math.random() - 0.5) * 0.35 - 0.12;
          this.baseAlpha = Math.random() * 0.35 + 0.45;
          this.twinkleSpeed = Math.random() * 0.03 + 0.015;
          this.parallax = 0.22;
        } else {
          // Foreground radiant white spark
          this.size = Math.random() * 2.2 + 2.0;
          this.baseSpeedX = (Math.random() - 0.5) * 0.5;
          this.baseSpeedY = (Math.random() - 0.5) * 0.5 - 0.2;
          this.baseAlpha = Math.random() * 0.3 + 0.7;
          this.twinkleSpeed = Math.random() * 0.04 + 0.02;
          this.parallax = 0.42;
        }

        this.twinklePhase = Math.random() * Math.PI * 2;
        this.alpha = this.baseAlpha;
        this.vx = this.baseSpeedX;
        this.vy = this.baseSpeedY;
      }

      update(scrollVel) {
        this.twinklePhase += this.twinkleSpeed;
        const pulse = Math.sin(this.twinklePhase) * 0.22;
        const scrollGlow = Math.min(Math.abs(scrollVel) * 0.012, 0.3);
        this.alpha = Math.max(0.1, Math.min(1.0, this.baseAlpha + pulse + scrollGlow));

        // Parallax vertical movement driven by scroll inertia
        const scrollDisplacement = -scrollVel * this.parallax;

        this.x += this.vx;
        this.y += this.vy + scrollDisplacement;

        // Interactive mouse physics
        if (mouse.active) {
          const dx = mouse.x - this.x;
          const dy = mouse.y - this.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < mouse.radius && dist > 0) {
            const force = (mouse.radius - dist) / mouse.radius;
            const push = this.layer === 2 ? force * 4.0 : force * 2.2;
            this.x -= (dx / dist) * push;
            this.y -= (dy / dist) * push;
          }
        }

        // Screen boundary wrapping
        if (this.x < -25) this.x = width + 25;
        if (this.x > width + 25) this.x = -25;
        if (this.y < -35) this.y = height + 35;
        if (this.y > height + 35) this.y = -35;
      }

      draw(scrollVel) {
        const speedMag = Math.abs(scrollVel);

        // When scrolling rapidly, stretch into glowing speed warp lines
        if (speedMag > 1.2 && (this.layer === 1 || this.layer === 2)) {
          const streakLen = Math.min(speedMag * (this.layer === 2 ? 3.0 : 1.8), 50);
          const streakDir = -Math.sign(scrollVel || 1);

          ctx.save();
          ctx.beginPath();
          ctx.moveTo(this.x, this.y);
          ctx.lineTo(this.x + this.vx * 2, this.y + streakDir * streakLen);

          const grad = ctx.createLinearGradient(
            this.x, this.y,
            this.x + this.vx * 2, this.y + streakDir * streakLen
          );
          grad.addColorStop(0, `rgba(255, 255, 255, ${this.alpha})`);
          grad.addColorStop(1, 'rgba(255, 255, 255, 0)');

          ctx.strokeStyle = grad;
          ctx.lineWidth = this.size * (this.layer === 2 ? 1.1 : 0.8);
          ctx.lineCap = 'round';
          ctx.stroke();

          // Luminous particle core
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.size * 0.9, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(255, 255, 255, ${Math.min(1, this.alpha + 0.25)})`;
          ctx.shadowColor = 'rgba(255, 255, 255, 0.95)';
          ctx.shadowBlur = this.layer === 2 ? 14 : 7;
          ctx.fill();
          ctx.restore();
        } else {
          // Standard high-definition glowing particle
          ctx.save();
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);

          if (this.layer === 2) {
            ctx.fillStyle = `rgba(255, 255, 255, ${this.alpha})`;
            ctx.shadowColor = 'rgba(255, 255, 255, 0.95)';
            ctx.shadowBlur = 10;
          } else if (this.layer === 1) {
            ctx.fillStyle = `rgba(240, 245, 255, ${this.alpha})`;
            ctx.shadowColor = 'rgba(255, 255, 255, 0.6)';
            ctx.shadowBlur = 4;
          } else {
            ctx.fillStyle = `rgba(215, 225, 255, ${this.alpha})`;
          }
          ctx.fill();
          ctx.restore();
        }
      }
    }

    // Class: Cybernetic Wave / Flow Line that undulates and shifts with scroll depth
    class FlowWaveLine {
      constructor(yRatio, amplitude, frequency, speed, alpha) {
        this.yRatio = yRatio;
        this.amplitude = amplitude;
        this.frequency = frequency;
        this.speed = speed;
        this.baseAlpha = alpha;
        this.phase = Math.random() * Math.PI * 2;
      }

      update(scrollVel) {
        // Continuous organic motion + scroll velocity reaction
        this.phase += this.speed + scrollVel * 0.007;
      }

      draw(scrollVel, time) {
        const baseY = height * this.yRatio + Math.sin(time * 0.4 + this.yRatio * 6) * 25;
        const dynAmp = this.amplitude + Math.min(Math.abs(scrollVel) * 1.6, 40);
        const alphaBoost = Math.min(Math.abs(scrollVel) * 0.02, 0.28);
        const curAlpha = Math.min(0.65, this.baseAlpha + alphaBoost);

        ctx.save();
        ctx.beginPath();

        const step = 24;
        for (let x = 0; x <= width + step; x += step) {
          const angle = (x * this.frequency) + this.phase + (currentScrollY * 0.0018);
          const y = baseY + Math.sin(angle) * dynAmp + Math.cos(angle * 0.45) * (dynAmp * 0.35);
          if (x === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }

        const grad = ctx.createLinearGradient(0, 0, width, 0);
        grad.addColorStop(0, 'rgba(255, 255, 255, 0)');
        grad.addColorStop(0.2, `rgba(255, 255, 255, ${curAlpha * 0.45})`);
        grad.addColorStop(0.5, `rgba(255, 255, 255, ${curAlpha})`);
        grad.addColorStop(0.8, `rgba(255, 255, 255, ${curAlpha * 0.45})`);
        grad.addColorStop(1, 'rgba(255, 255, 255, 0)');

        ctx.strokeStyle = grad;
        ctx.lineWidth = 1.1;
        ctx.stroke();
        ctx.restore();
      }
    }

    // Shooting star / Meteor trail on scroll bursts
    class Meteor {
      constructor(direction) {
        this.x = Math.random() * width;
        this.y = direction >= 0 ? -30 : height + 30;
        this.len = Math.random() * 90 + 70;
        this.speed = (Math.random() * 14 + 18) * (direction >= 0 ? 1 : -1);
        this.angle = (Math.random() - 0.5) * 0.25;
        this.alpha = 1.0;
        this.size = Math.random() * 1.6 + 1.2;
      }

      update() {
        this.x += Math.sin(this.angle) * Math.abs(this.speed);
        this.y += this.speed;
        this.alpha -= 0.026;
      }

      draw() {
        if (this.alpha <= 0) return;
        ctx.save();
        const tailX = this.x - Math.sin(this.angle) * this.len * Math.sign(this.speed);
        const tailY = this.y - this.len * Math.sign(this.speed);

        const grad = ctx.createLinearGradient(this.x, this.y, tailX, tailY);
        grad.addColorStop(0, `rgba(255, 255, 255, ${this.alpha})`);
        grad.addColorStop(1, 'rgba(255, 255, 255, 0)');

        ctx.strokeStyle = grad;
        ctx.lineWidth = this.size;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(tailX, tailY);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size * 1.6, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${this.alpha})`;
        ctx.shadowColor = 'rgba(255, 255, 255, 1)';
        ctx.shadowBlur = 14;
        ctx.fill();
        ctx.restore();
      }
    }

    function spawnMeteor(delta) {
      if (meteors.length < 5) {
        meteors.push(new Meteor(Math.sign(delta)));
      }
    }

    function initParticles() {
      particles = [];
      // Calculate responsive particle density
      const area = width * height;
      const layer0Count = Math.min(Math.floor(area / 18000), 55); // Background stars
      const layer1Count = Math.min(Math.floor(area / 16000), 50); // Midground constellation nodes
      const layer2Count = Math.min(Math.floor(area / 32000), 25); // Foreground sparks

      for (let i = 0; i < layer0Count; i++) particles.push(new WhiteParticle(0));
      for (let i = 0; i < layer1Count; i++) particles.push(new WhiteParticle(1));
      for (let i = 0; i < layer2Count; i++) particles.push(new WhiteParticle(2));
    }

    function initWaveLines() {
      waveLines = [
        new FlowWaveLine(0.18, 22, 0.0022, 0.008, 0.12),
        new FlowWaveLine(0.42, 28, 0.0018, -0.006, 0.16),
        new FlowWaveLine(0.68, 24, 0.0025, 0.009, 0.14),
        new FlowWaveLine(0.88, 30, 0.0016, -0.007, 0.11)
      ];
    }

    // Main 60-120 FPS Animation Loop
    function animate(now) {
      const timeSec = now * 0.001;

      // Smooth scroll interpolation (Lerp)
      const scrollDiff = targetScrollY - currentScrollY;
      currentScrollY += scrollDiff * 0.12;
      
      // Calculate instant scroll velocity with smooth damping
      const instantVelocity = scrollDiff * 0.12;
      smoothedScrollVelocity += (instantVelocity - smoothedScrollVelocity) * 0.15;
      scrollVelocityDamped = smoothedScrollVelocity;

      // Mouse smooth interpolation
      if (mouse.active) {
        mouse.x += (mouse.targetX - mouse.x) * 0.2;
        mouse.y += (mouse.targetY - mouse.y) * 0.2;
      }

      // Clear Canvas Frame
      ctx.clearRect(0, 0, width, height);

      // 1. Draw Undulating Scroll-Reactive Cybernetic Wave Lines
      for (let i = 0; i < waveLines.length; i++) {
        waveLines[i].update(scrollVelocityDamped);
        waveLines[i].draw(scrollVelocityDamped, timeSec);
      }

      // 2. Update & Draw All Particles
      const activeNodes = [];
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.update(scrollVelocityDamped);
        p.draw(scrollVelocityDamped);
        if (p.layer >= 1) {
          activeNodes.push(p);
        }
      }

      // 3. Connective Constellation Lines Between Nearby White Nodes
      const maxConnectDist = 120;
      const maxConnectDistSq = maxConnectDist * maxConnectDist;
      const scrollBoost = Math.min(Math.abs(scrollVelocityDamped) * 0.02, 0.18);

      for (let a = 0; a < activeNodes.length; a++) {
        const p1 = activeNodes[a];
        for (let b = a + 1; b < activeNodes.length; b++) {
          const p2 = activeNodes[b];
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const distSq = dx * dx + dy * dy;

          if (distSq < maxConnectDistSq) {
            const dist = Math.sqrt(distSq);
            const lineAlpha = (1 - dist / maxConnectDist) * 0.24 * ((p1.alpha + p2.alpha) * 0.5) + scrollBoost;
            
            ctx.save();
            ctx.strokeStyle = `rgba(255, 255, 255, ${Math.min(0.55, lineAlpha)})`;
            ctx.lineWidth = 0.85;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
            ctx.restore();
          }
        }

        // Connect particle to mouse cursor if within proximity
        if (mouse.active) {
          const mdx = mouse.x - p1.x;
          const mdy = mouse.y - p1.y;
          const mDistSq = mdx * mdx + mdy * mdy;
          const mouseConnectDist = 135;
          if (mDistSq < mouseConnectDist * mouseConnectDist) {
            const mDist = Math.sqrt(mDistSq);
            const mAlpha = (1 - mDist / mouseConnectDist) * 0.42 * p1.alpha;
            ctx.save();
            ctx.strokeStyle = `rgba(255, 255, 255, ${mAlpha})`;
            ctx.lineWidth = 1.0;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.stroke();
            ctx.restore();
          }
        }
      }

      // 4. Update & Draw Meteors / Light Bursts
      for (let i = meteors.length - 1; i >= 0; i--) {
        const m = meteors[i];
        m.update();
        m.draw();
        if (m.alpha <= 0 || m.y < -100 || m.y > height + 100) {
          meteors.splice(i, 1);
        }
      }

      animId = requestAnimationFrame(animate);
    }

    // Performance optimization: pause animation when tab is not visible
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        if (animId) cancelAnimationFrame(animId);
      } else {
        lastScrollTime = performance.now();
        animId = requestAnimationFrame(animate);
      }
    });

    // Initialize Engine
    resize();
    window.addEventListener('resize', resize, { passive: true });
    animId = requestAnimationFrame(animate);
  })();
  </script>
"""

# Insert script before </body>
if 'WHITE PARTICLES & SCROLL-REACTIVE VFX ENGINE' not in content:
    content = content.replace('</body>', vfx_engine_js + '\n</body>')

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully injected Black background & White animated particle/line scroll VFX engine into index.html!')
