/**
 * VEIRA STUDIOS — 3D Effect Intro & Scroll-to-2D Shine Engine
 * Real-time WebGL / Three.js Hard-Surface Emblem that greets visitors with a
 * cinematic 3D effect intro, then flattens into a 2D logo with a brilliant
 * luminous shine effect upon scrolling.
 */

(function() {
  'use strict';

  // Vector coordinates for the 5 polygons extracted from the official Veira Studios emblem
  const EMBLEM_POLYGONS = [
    {
      id: 0, // Starboard outer frame bracket
      name: "s_bracket",
      group: "right",
      points: [
        [0.869, 0.078], [0.762, 0.019], [0.743, 0.0], [0.738, -0.427],
        [0.714, -0.451], [0.150, -0.772], [0.141, -0.786], [0.141, -0.922],
        [0.791, -0.553], [0.835, -0.515], [0.869, -0.432]
      ]
    },
    {
      id: 1, // Stylized "S" face
      name: "s_letter",
      group: "right",
      points: [
        [0.563, 0.184], [0.228, 0.0], [0.204, -0.024], [0.146, -0.131],
        [0.146, -0.306], [0.257, -0.354], [0.282, -0.354], [0.515, -0.223],
        [0.524, -0.228], [0.524, -0.320], [0.510, -0.335], [0.286, -0.461],
        [0.272, -0.456], [0.272, -0.427], [0.262, -0.427], [0.146, -0.495],
        [0.146, -0.578], [0.209, -0.612], [0.243, -0.621], [0.578, -0.432],
        [0.655, -0.306], [0.650, -0.126], [0.544, -0.078], [0.524, -0.078],
        [0.286, -0.214], [0.272, -0.209], [0.272, -0.117], [0.515, 0.024],
        [0.524, 0.019], [0.524, -0.010], [0.534, -0.010], [0.650, 0.058],
        [0.650, 0.136]
      ]
    },
    {
      id: 2, // Stylized "V" inner chevron
      name: "v_inner",
      group: "left",
      points: [
        [-0.655, 0.238], [-0.660, -0.010], [-0.515, -0.451], [-0.481, -0.490],
        [-0.335, -0.568], [-0.150, -0.252], [-0.150, -0.053], [-0.180, -0.029],
        [-0.277, 0.019], [-0.277, -0.160], [-0.403, -0.393], [-0.417, -0.374],
        [-0.534, -0.024], [-0.534, 0.165]
      ]
    },
    {
      id: 3, // Port outer frame / "V" bracket
      name: "v_bracket",
      group: "left",
      points: [
        [-0.874, 0.359], [-0.874, -0.422], [-0.859, -0.481], [-0.835, -0.519],
        [-0.796, -0.553], [-0.083, -0.961], [-0.029, -0.985], [0.029, -0.981],
        [0.058, -0.942], [0.058, -0.563], [0.044, -0.549], [-0.063, -0.490],
        [-0.063, -0.796], [-0.083, -0.811], [-0.709, -0.456], [-0.743, -0.427],
        [-0.748, 0.282], [-0.767, 0.301]
      ]
    },
    {
      id: 4, // Top isometric diamond frame & corner pillars
      name: "top_frame",
      group: "top",
      points: [
        [-0.034, 0.990], [-0.083, 0.971], [-0.811, 0.553], [-0.854, 0.515],
        [-0.859, 0.461], [-0.811, 0.422], [-0.505, 0.252], [-0.456, 0.267],
        [-0.005, 0.524], [0.034, 0.510], [0.340, 0.335], [0.350, 0.316],
        [0.335, 0.301], [0.005, 0.117], [-0.049, 0.136], [-0.277, 0.267],
        [-0.320, 0.252], [-0.408, 0.199], [-0.117, 0.034], [-0.068, -0.005],
        [-0.063, -0.383], [0.058, -0.456], [0.063, -0.005], [0.121, 0.039],
        [0.718, 0.374], [0.743, 0.364], [0.743, 0.112], [0.869, 0.184],
        [0.869, 0.451], [0.845, 0.519], [0.825, 0.539], [0.782, 0.553],
        [0.549, 0.422], [0.485, 0.398], [0.010, 0.665], [-0.015, 0.665],
        [-0.490, 0.398], [-0.553, 0.422], [-0.646, 0.481], [-0.646, 0.495],
        [-0.621, 0.515], [-0.005, 0.864], [0.112, 0.806], [0.573, 0.539],
        [0.704, 0.607], [0.097, 0.961], [0.029, 0.990]
      ]
    }
  ];

  class Veira3DIntroEngine {
    constructor(containerId) {
      this.container = document.getElementById(containerId);
      if (!this.container) return;

      this.canvas = this.container.querySelector('canvas') || document.createElement('canvas');
      if (!this.canvas.parentElement) {
        this.container.appendChild(this.canvas);
      }

      this.overlay2D = document.getElementById('veira-2d-logo-overlay');
      this.statusBadge = document.getElementById('veira-logo-status');
      this.shineSweep = document.getElementById('veira-shine-sweep');

      // State tracking
      this.is2DActive = false;
      this.scrollProgress = 0; // 0 = at top (3D intro), 1 = scrolled (2D mode)
      this.introTime = 0;
      this.isVisible = true;

      // Mouse parallax
      this.mouseNormX = 0;
      this.mouseNormY = 0;

      this.initThree();
      this.buildMeshes();
      this.buildLighting();
      this.setupInteraction();
      this.setupScrollListener();

      this.clock = new THREE.Clock();
      this.animate = this.animate.bind(this);
      requestAnimationFrame(this.animate);
    }

    initThree() {
      const width = this.container.clientWidth || 600;
      const height = this.container.clientHeight || 480;

      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(38, width / height, 0.1, 100);
      this.camera.position.set(0, 0, 5.0);

      this.renderer = new THREE.WebGLRenderer({
        canvas: this.canvas,
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance'
      });
      this.renderer.setSize(width, height);
      this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      if (THREE.ACESFilmicToneMapping) {
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.3;
      }

      // Hierarchy
      this.logoRoot = new THREE.Group();
      this.scene.add(this.logoRoot);

      this.pivotGroup = new THREE.Group();
      this.logoRoot.add(this.pivotGroup);
    }

    buildMeshes() {
      // Titanium PBR metallic chrome material
      this.chromeMaterial = new THREE.MeshStandardMaterial({
        color: 0xf5f8fc,
        metalness: 0.88,
        roughness: 0.18,
        side: THREE.DoubleSide
      });

      const extrudeDepth = 0.22;
      const extrudeSettings = {
        depth: extrudeDepth,
        bevelEnabled: true,
        bevelSegments: 3,
        steps: 1,
        bevelSize: 0.02,
        bevelThickness: 0.022
      };

      EMBLEM_POLYGONS.forEach(polyData => {
        const shape = new THREE.Shape();
        polyData.points.forEach((pt, idx) => {
          const x = pt[0] * 1.35;
          const y = pt[1] * 1.35;
          if (idx === 0) shape.moveTo(x, y);
          else shape.lineTo(x, y);
        });
        shape.closePath();

        const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
        geometry.translate(0, 0, -extrudeDepth / 2);

        const mesh = new THREE.Mesh(geometry, this.chromeMaterial);
        mesh.castShadow = true;

        // Glowing CAD beveled wireframe edges
        const edgesGeo = new THREE.EdgesGeometry(geometry, 25);
        const edgesMat = new THREE.LineBasicMaterial({
          color: 0x00e5ff,
          transparent: true,
          opacity: 0.5,
          linewidth: 1.5
        });
        const edgeLine = new THREE.LineSegments(edgesGeo, edgesMat);
        mesh.add(edgeLine);

        this.pivotGroup.add(mesh);
      });

      // Subtle ambient orbital particle ring
      const partCount = 45;
      const partGeo = new THREE.BufferGeometry();
      const posArray = new Float32Array(partCount * 3);
      for (let i = 0; i < partCount; i++) {
        const theta = (i / partCount) * Math.PI * 2;
        const radius = 2.1 + (Math.random() - 0.5) * 0.4;
        posArray[i * 3] = Math.cos(theta) * radius;
        posArray[i * 3 + 1] = Math.sin(theta) * radius * 0.75 + (Math.random() - 0.5) * 0.3;
        posArray[i * 3 + 2] = (Math.random() - 0.5) * 0.6;
      }
      partGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
      const partMat = new THREE.PointsMaterial({
        color: 0x00e5ff,
        size: 0.035,
        transparent: true,
        opacity: 0.55
      });
      this.particles = new THREE.Points(partGeo, partMat);
      this.logoRoot.add(this.particles);

      // Start initial 3D intro presentation angle
      this.pivotGroup.rotation.y = -0.55;
      this.pivotGroup.rotation.x = 0.22;
    }

    buildLighting() {
      const ambLight = new THREE.AmbientLight(0xffffff, 0.85);
      this.scene.add(ambLight);

      // Key light
      this.keyLight = new THREE.DirectionalLight(0xffffff, 2.2);
      this.keyLight.position.set(4, 5, 5);
      this.scene.add(this.keyLight);

      // Cyan rim light
      this.rimCyan = new THREE.DirectionalLight(0x00e5ff, 2.0);
      this.rimCyan.position.set(-5, 3, -3);
      this.scene.add(this.rimCyan);

      // Amber fill light
      this.fillWarm = new THREE.DirectionalLight(0xff7b00, 1.2);
      this.fillWarm.position.set(3, -4, 2);
      this.scene.add(this.fillWarm);

      // Mouse specular glint light
      this.specularLight = new THREE.PointLight(0xffffff, 1.8, 10);
      this.specularLight.position.set(0, 1.5, 3.5);
      this.scene.add(this.specularLight);
    }

    setupInteraction() {
      // Parallax mouse responsiveness
      const onPointerMove = (e) => {
        const rect = this.container.getBoundingClientRect();
        const clientX = e.clientX || (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
        const clientY = e.clientY || (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
        this.mouseNormX = ((clientX - rect.left) / (rect.width || 1)) * 2 - 1;
        this.mouseNormY = -(((clientY - rect.top) / (rect.height || 1)) * 2 - 1);
      };

      this.container.addEventListener('mousemove', onPointerMove, { passive: true });
      this.container.addEventListener('touchmove', onPointerMove, { passive: true });

      // Resize observer
      window.addEventListener('resize', () => {
        if (!this.container || !this.renderer || !this.camera) return;
        const w = this.container.clientWidth;
        const h = this.container.clientHeight;
        this.camera.aspect = w / h;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(w, h);
      });
    }

    setupScrollListener() {
      let ticking = false;

      const handleScroll = () => {
        if (!ticking) {
          window.requestAnimationFrame(() => {
            const scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;

            // Transition range: 0px -> 140px of scroll
            const threshold = 140;
            const progress = Math.max(0, Math.min(1, scrollY / threshold));
            this.scrollProgress = progress;

            if (progress >= 0.65 && !this.is2DActive) {
              this.activate2DMode();
            } else if (progress < 0.65 && this.is2DActive) {
              this.activate3DMode();
            }

            ticking = false;
          });
          ticking = true;
        }
      };

      window.addEventListener('scroll', handleScroll, { passive: true });
      // Initial check
      handleScroll();
    }

    activate2DMode() {
      this.is2DActive = true;

      // 1. Crossfade 3D canvas out, 2D overlay in
      if (this.canvas) {
        this.canvas.style.opacity = '0';
        this.canvas.style.transition = 'opacity 0.45s ease';
      }
      if (this.overlay2D) {
        this.overlay2D.classList.add('active');
      }

      // 2. Update status indicator
      if (this.statusBadge) {
        this.statusBadge.textContent = '2D SIGNATURE LOGO [ACTIVE]';
        this.statusBadge.style.color = '#00e5ff';
        this.statusBadge.style.borderColor = 'rgba(0, 229, 255, 0.4)';
      }

      // 3. Trigger immediate shine sweep animation
      if (this.shineSweep) {
        this.shineSweep.classList.remove('play-shine');
        void this.shineSweep.offsetWidth; // force reflow
        this.shineSweep.classList.add('play-shine');
      }

      // 4. Also add subtle shine to sticky navbar logo
      const navLogo = document.querySelector('.nav-logo-img');
      if (navLogo) {
        navLogo.classList.add('nav-logo-shining');
      }
    }

    activate3DMode() {
      this.is2DActive = false;

      // 1. Crossfade 3D canvas in, 2D overlay out
      if (this.canvas) {
        this.canvas.style.opacity = '1';
      }
      if (this.overlay2D) {
        this.overlay2D.classList.remove('active');
      }

      // 2. Update status indicator
      if (this.statusBadge) {
        this.statusBadge.textContent = '3D EFFECT INTRO [ACTIVE]';
        this.statusBadge.style.color = '#ff7b00';
        this.statusBadge.style.borderColor = 'rgba(255, 123, 0, 0.4)';
      }

      const navLogo = document.querySelector('.nav-logo-img');
      if (navLogo) {
        navLogo.classList.remove('nav-logo-shining');
      }
    }

    animate() {
      requestAnimationFrame(this.animate);
      if (!this.isVisible) return;

      const delta = Math.min(this.clock.getDelta(), 0.1);
      const time = this.clock.getElapsedTime();
      this.introTime += delta;

      // 3D Intro kinematics vs Flat 2D interpolation based on scroll
      const p = this.scrollProgress; // 0 (3D intro) -> 1 (flat 2D)

      if (p < 0.95) {
        // Subtle sinusoidal levitation in 3D mode
        const levitation = Math.sin(time * 1.6) * 0.06 * (1 - p);
        this.logoRoot.position.y = levitation;
        this.logoRoot.position.z = -p * 0.4;

        // Target rotations:
        // In 3D Intro mode (p = 0): continuous subtle 3D spin + idle tilt + mouse parallax
        // In transition (p -> 1): rotX -> 0, rotY -> 0, rotZ -> 0 (flattens seamlessly into 2D)
        const idleRotY = Math.sin(time * 0.8) * 0.35 - 0.2;
        const targetRotY = (1 - p) * (idleRotY + this.mouseNormX * 0.25);
        const targetRotX = (1 - p) * (0.18 - this.mouseNormY * 0.2);

        this.pivotGroup.rotation.y += (targetRotY - this.pivotGroup.rotation.y) * 0.08;
        this.pivotGroup.rotation.x += (targetRotX - this.pivotGroup.rotation.x) * 0.08;
        this.pivotGroup.rotation.z += (0 - this.pivotGroup.rotation.z) * 0.08;

        // Dynamic specular glint following cursor
        this.specularLight.position.x = this.mouseNormX * 3.2;
        this.specularLight.position.y = this.mouseNormY * 3.2 + 1.2;

        // Particles rotation
        if (this.particles) {
          this.particles.rotation.y = time * 0.06;
          this.particles.material.opacity = (1 - p) * 0.55;
        }

        this.renderer.render(this.scene, this.camera);
      }
    }
  }

  // Robust initialization
  function initVeira3DIntro() {
    if (window.THREE && document.getElementById('veira-3d-chamber') && !window.veira3D) {
      window.veira3D = new Veira3DIntroEngine('veira-3d-chamber');
    }
  }

  if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', initVeira3DIntro);
  } else {
    setTimeout(initVeira3DIntro, 10);
  }
})();
