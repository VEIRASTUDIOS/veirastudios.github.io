import subprocess

# 1. Android SVG
android_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="androidGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4ae38f" />
      <stop offset="100%" stop-color="#2bbd6e" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="16" flood-color="#3ddc84" flood-opacity="0.35"/>
    </filter>
  </defs>
  <g filter="url(#glow)">
    <!-- Head -->
    <path d="M128,340 L384,340 A128,128 0 0,0 128,340 Z" fill="url(#androidGrad)"/>
    <!-- Eyes -->
    <circle cx="204" cy="286" r="14" fill="#0c121d" />
    <circle cx="308" cy="286" r="14" fill="#0c121d" />
    <!-- Antennae -->
    <line x1="190" y1="216" x2="152" y2="154" stroke="url(#androidGrad)" stroke-width="15" stroke-linecap="round" />
    <line x1="322" y1="216" x2="360" y2="154" stroke="url(#androidGrad)" stroke-width="15" stroke-linecap="round" />
  </g>
</svg>'''

with open('platform_android.svg', 'w') as f:
    f.write(android_svg)

# 2. Apple / iOS SVG
ios_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="appleGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="50%" stop-color="#f0f3f8" />
      <stop offset="100%" stop-color="#c9d4e2" />
    </linearGradient>
    <filter id="appleGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#0071e3" flood-opacity="0.30"/>
    </filter>
  </defs>
  <g filter="url(#appleGlow)" transform="translate(76, 56) scale(0.70)">
    <!-- Leaf -->
    <path d="M323.5,0.7 C347.8,29.8 333.6,71.2 333.6,71.2 C333.6,71.2 295.4,74.7 269.4,44.1 C244.6,14.8 259.9,-27.6 259.9,-27.6 C259.9,-27.6 298.1,-29.4 323.5,0.7 Z" fill="url(#appleGrad)" transform="translate(0, 30)"/>
    <!-- Body -->
    <path d="M370.2,165.7 C370.7,219.7 416.7,237.7 417.2,238 C416.8,239.3 410.6,260.6 395.7,282.4 C382.7,301.2 369.3,320 348,320.4 C327.2,320.8 320.5,308.2 296.8,308.2 C273.1,308.2 265.6,320 245.7,320.8 C225.2,321.6 209.6,300.7 196.4,281.7 C169.5,243.1 149,172.6 176.7,124.6 C190.5,100.7 215.3,85.6 242.2,85.2 C262.3,84.8 281.3,98.8 293.6,98.8 C305.9,98.8 329.1,82 353.4,84.4 C363.6,84.8 392.2,88.5 410.5,115.3 C409,116.2 369.8,139.1 370.2,165.7 Z" fill="url(#appleGrad)" transform="translate(0, 30)"/>
  </g>
</svg>'''

with open('platform_ios.svg', 'w') as f:
    f.write(ios_svg)

# 3. Windows SVG
windows_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="winTL" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00c8ff" />
      <stop offset="100%" stop-color="#0078d4" />
    </linearGradient>
    <linearGradient id="winTR" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00dbff" />
      <stop offset="100%" stop-color="#0086e8" />
    </linearGradient>
    <linearGradient id="winBL" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#009be6" />
      <stop offset="100%" stop-color="#0062b0" />
    </linearGradient>
    <linearGradient id="winBR" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00b0f0" />
      <stop offset="100%" stop-color="#0070c9" />
    </linearGradient>
    <filter id="winGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="10" stdDeviation="16" flood-color="#0078d4" flood-opacity="0.35"/>
    </filter>
  </defs>
  <g filter="url(#winGlow)">
    <!-- Top-Left -->
    <rect x="96" y="96" width="148" height="148" rx="8" fill="url(#winTL)" />
    <!-- Top-Right -->
    <rect x="268" y="96" width="148" height="148" rx="8" fill="url(#winTR)" />
    <!-- Bottom-Left -->
    <rect x="96" y="268" width="148" height="148" rx="8" fill="url(#winBL)" />
    <!-- Bottom-Right -->
    <rect x="268" y="268" width="148" height="148" rx="8" fill="url(#winBR)" />
  </g>
</svg>'''

with open('platform_windows.svg', 'w') as f:
    f.write(windows_svg)

print('SVGs written.')

for name in ['platform_android', 'platform_ios', 'platform_windows']:
    cmd = ['sips', '-s', 'format', 'png', '--resampleWidth', '512', f'{name}.svg', '--out', f'{name}.png']
    subprocess.run(cmd, check=True)
    print(f'Converted {name}.png successfully')
