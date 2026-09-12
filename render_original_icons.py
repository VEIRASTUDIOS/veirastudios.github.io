import subprocess
import os
from PIL import Image

# 1. Official Android Robot Head SVG (Clean, Simple, Official Google #3DDC84)
android_svg = '''<svg width="512" height="512" viewBox="-120 -80 1158 750" xmlns="http://www.w3.org/2000/svg">
  <path fill="#3DDC84" d="M918.6 515.1h-918.6c14.7-155.7 103.7-288.7 235.1-359.9l-76.2-132c-4.3-7.4-1.8-16.8 5.6-21.1s16.8-1.8 21.1 5.6l77.2 133.7c58.9-26.9 125.2-41.9 196.5-41.9s137.6 15 196.5 41.9l77.2-133.7c4.2-7.4 13.7-9.9 21-5.6s9.9 13.7 5.6 21.1l-76.2 132c131.5 71.2 220.5 204.2 235.2 359.9zm-248.5-129c21.3 0 38.6-17.3 38.5-38.5 0-21.2-17.2-38.5-38.5-38.5-21.2 0-38.5 17.2-38.5 38.5 0 21.2 17.2 38.5 38.5 38.5zm-421.7 0c21.3 0 38.6-17.3 38.5-38.5 0-21.2-17.2-38.5-38.5-38.5-21.2 0-38.5 17.2-38.5 38.5 0 21.2 17.2 38.5 38.5 38.5z"/>
</svg>'''

# 2. Official Apple iOS Logo (Clean, Simple, Official Pure White #FFFFFF)
apple_svg = '''<svg width="512" height="512" viewBox="-150 -100 1114 1200" xmlns="http://www.w3.org/2000/svg">
  <path fill="#FFFFFF" d="M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-68.7 141.9-42.8 61.6-87.5 123.1-155.5 123.1s-85.5-39.5-164-39.5c-76.5 0-103.7 40.8-165.9 40.8s-105.6-57-155.5-127C46.7 790.7 0 663 0 541.8c0-194.4 126.4-297.5 250.8-297.5 66.1 0 121.2 43.4 162.7 43.4 39.5 0 101.1-46 176.3-46 28.5 0 130.9 2.6 198.3 99.2zm-234-181.5c31.1-36.9 53.1-88.1 53.1-139.3 0-7.1-.6-14.3-1.9-20.1-50.6 1.9-110.8 33.7-147.1 75.8-28.5 32.4-55.1 83.6-55.1 135.5 0 7.8 1.3 15.6 1.9 18.1 3.2.6 8.4 1.3 13.6 1.3 45.4 0 102.5-30.4 135.5-71.3z"/>
</svg>'''

# 3. Official Windows 11 Logo (Clean, Simple, Official Microsoft Blue #0078D4)
windows_svg = '''<svg width="512" height="512" viewBox="-600 -600 6075 6075" xmlns="http://www.w3.org/2000/svg">
  <path fill="#0078D4" d="M0 0h2311v2310H0zm2564 0h2311v2310H2564zM0 2564h2311v2311H0zm2564 0h2311v2311H2564"/>
</svg>'''

# 4. Official Discord Clyde Logo (Clean, Simple, Official Discord Blurple #5865F2)
discord_svg = '''<svg width="512" height="512" viewBox="-2 -3 28 28" xmlns="http://www.w3.org/2000/svg">
  <path fill="#5865F2" d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z"/>
</svg>'''

svgs = {
    'platform_android.svg': android_svg,
    'platform_ios.svg': apple_svg,
    'platform_windows.svg': windows_svg,
    'discord_icon.svg': discord_svg,
}

for filename, content in svgs.items():
    with open(filename, 'w') as f:
        f.write(content)
    subprocess.run(['qlmanage', '-t', '-s', '512', '-o', '.', filename], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    out_png = filename + '.png'
    target_png = filename.replace('.svg', '.png')
    # Load and save to target
    im = Image.open(out_png).convert('RGBA')
    im.save(target_png, 'PNG')
    os.remove(filename)
    os.remove(out_png)
    print(f'Rendered {target_png}: {im.size}')

# 5. Process macOS Finder icon to 512x512
if os.path.exists('platform_macos.png'):
    im_mac = Image.open('platform_macos.png').convert('RGBA')
    im_mac = im_mac.resize((512, 512), Image.Resampling.LANCZOS)
    im_mac.save('platform_macos.png', 'PNG')
    print('Updated platform_macos.png to 512x512')

print('All 5 official original simple PNG icons generated successfully!')
