import sys

with open('/Users/albinkrasniqi/Desktop/SITE/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Canvas CSS
canvas_css = """
    /* ===== VFX PARTICLES CANVAS ===== */
    #vfx-particles {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 0;
    }
"""

content = content.replace('  </style>', canvas_css + '\n  </style>')

# 2. Add Canvas HTML element right after <body>
canvas_html = '<canvas id="vfx-particles"></canvas>'
content = content.replace('<body>', '<body>\n  ' + canvas_html)

# 3. Add Canvas JS animation engine script before </body>
particles_js = """
  <!-- ===== VFX PARTICLES ANIMATION ENGINE ===== -->
  <script>
    (function() {
      const canvas = document.getElementById('vfx-particles');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');

      let width = canvas.width = window.innerWidth;
      let height = canvas.height = window.innerHeight;

      window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
      }, { passive: true });

      // Interactive mouse position
      const mouse = { x: -1000, y: -1000, radius: 150 };
      window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
      }, { passive: true });

      const particleColors = [
        'rgba(0, 210, 255, ',   // Neon Cyan
        'rgba(0, 113, 227, ',   // Electric Blue
        'rgba(139, 92, 246, ',  // Purple
        'rgba(249, 115, 22, '   // Neon Orange
      ];

      const count = Math.min(Math.floor((width * height) / 14000), 80);
      const particles = [];

      class Particle {
        constructor() {
          this.reset(true);
        }

        reset(initial = false) {
          this.x = Math.random() * width;
          this.y = initial ? Math.random() * height : height + 10;
          this.size = Math.random() * 2.5 + 1;
          this.speedY = Math.random() * 0.6 + 0.2;
          this.speedX = (Math.random() - 0.5) * 0.4;
          this.color = particleColors[Math.floor(Math.random() * particleColors.length)];
          this.alpha = Math.random() * 0.6 + 0.2;
          this.maxAlpha = this.alpha;
          this.pulse = Math.random() * 0.02 + 0.005;
          this.angle = Math.random() * Math.PI * 2;
        }

        update() {
          this.angle += 0.02;
          this.x += this.speedX + Math.sin(this.angle) * 0.3;
          this.y -= this.speedY;

          // Mouse repulsion force
          const dx = mouse.x - this.x;
          const dy = mouse.y - this.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < mouse.radius) {
            const force = (mouse.radius - dist) / mouse.radius;
            this.x -= (dx / dist) * force * 3;
            this.y -= (dy / dist) * force * 3;
          }

          // Fade out near top
          if (this.y < 50) {
            this.alpha -= 0.01;
          }

          if (this.y < -10 || this.alpha <= 0) {
            this.reset(false);
          }
        }

        draw() {
          ctx.save();
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
          ctx.fillStyle = this.color + this.alpha + ')';
          ctx.shadowColor = this.color + '0.8)';
          ctx.shadowBlur = this.size * 4;
          ctx.fill();
          ctx.restore();
        }
      }

      for (let i = 0; i < count; i++) {
        particles.push(new Particle());
      }

      function animate() {
        ctx.clearRect(0, 0, width, height);

        for (let i = 0; i < particles.length; i++) {
          particles[i].update();
          particles[i].draw();
        }

        // Draw connective constellation lines between nearby particles
        for (let a = 0; a < particles.length; a++) {
          for (let b = a + 1; b < particles.length; b++) {
            const dx = particles[a].x - particles[b].x;
            const dy = particles[a].y - particles[b].y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 110) {
              const lineAlpha = (1 - dist / 110) * 0.15 * particles[a].alpha;
              ctx.strokeStyle = `rgba(0, 210, 255, ${lineAlpha})`;
              ctx.lineWidth = 0.8;
              ctx.beginPath();
              ctx.moveTo(particles[a].x, particles[a].y);
              ctx.lineTo(particles[b].x, particles[b].y);
              ctx.stroke();
            }
          }
        }

        requestAnimationFrame(animate);
      }

      animate();
    })();
  </script>
"""

content = content.replace('</body>', particles_js + '\n</body>')

with open('/Users/albinkrasniqi/Desktop/SITE/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added VFX moving particles background to index.html!')
