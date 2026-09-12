import sys

with open('/Users/albinkrasniqi/Desktop/SITE/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

chatbot_css = """
    /* ===== ROBLOX SHOWCASE CARDS ===== */
    .roblox-showcase-row {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 24px;
      margin-bottom: 40px;
    }
    .roblox-img-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      overflow: hidden;
      transition: var(--transition);
      position: relative;
    }
    .roblox-img-card:hover {
      border-color: rgba(249, 115, 22, 0.4);
      transform: translateY(-4px);
      box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 30px rgba(249, 115, 22, 0.15);
    }
    .roblox-img-wrapper {
      position: relative;
      width: 100%;
      height: 260px;
      overflow: hidden;
    }
    .roblox-img-wrapper img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .roblox-img-card:hover .roblox-img-wrapper img {
      transform: scale(1.05);
    }
    .roblox-img-overlay {
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, transparent 40%, rgba(18,18,22,0.95) 100%);
    }
    .roblox-img-caption {
      padding: 24px 28px;
    }
    .roblox-img-title {
      font-size: 20px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 8px;
    }
    .roblox-img-desc {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.5;
    }

    /* ===== ANIME BOT CHATBOT ===== */
    .chatbot-trigger {
      position: fixed;
      bottom: 30px;
      right: 30px;
      z-index: 9999;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
    }
    .trigger-avatar-wrap {
      position: relative;
      width: 64px;
      height: 64px;
      border-radius: 50%;
      padding: 3px;
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
      box-shadow: 0 0 30px rgba(0, 210, 255, 0.5);
      transition: var(--transition);
    }
    .trigger-avatar-wrap:hover {
      transform: scale(1.08);
      box-shadow: 0 0 45px rgba(0, 210, 255, 0.8);
    }
    .trigger-avatar-img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
      background: #000;
    }
    .trigger-unread-dot {
      position: absolute;
      top: 2px;
      right: 2px;
      width: 14px;
      height: 14px;
      background: var(--accent-green);
      border: 2px solid var(--bg-base);
      border-radius: 50%;
      animation: pulse 2s infinite;
    }
    .trigger-pill-callout {
      background: rgba(18, 18, 22, 0.9);
      border: 1px solid var(--border-subtle);
      backdrop-filter: blur(16px);
      padding: 8px 16px;
      border-radius: var(--radius-full);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .chat-window {
      position: fixed;
      bottom: 105px;
      right: 30px;
      width: 400px;
      max-width: calc(100vw - 40px);
      height: 570px;
      max-height: calc(100vh - 140px);
      background: rgba(14, 14, 18, 0.95);
      border: 1px solid rgba(0, 210, 255, 0.3);
      border-radius: 24px;
      box-shadow: 0 25px 60px rgba(0,0,0,0.8), 0 0 40px rgba(0, 210, 255, 0.18);
      backdrop-filter: blur(25px);
      z-index: 10000;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      opacity: 0;
      transform: translateY(20px) scale(0.95);
      pointer-events: none;
      transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .chat-window.open {
      opacity: 1;
      transform: translateY(0) scale(1);
      pointer-events: all;
    }

    .chat-header {
      padding: 16px 20px;
      background: rgba(255, 255, 255, 0.03);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .chat-header-profile {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .chat-header-avatar {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      object-fit: cover;
      border: 2px solid var(--accent-cyan);
    }
    .chat-header-info .name {
      font-size: 15px;
      font-weight: 800;
      color: var(--text-main);
    }
    .chat-header-info .status {
      font-size: 11px;
      color: var(--accent-green);
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .chat-header-info .status-dot-sm {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent-green);
    }
    .chat-close-btn {
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 20px;
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 6px;
      transition: var(--transition);
    }
    .chat-close-btn:hover { color: var(--text-main); background: rgba(255,255,255,0.1); }

    .chat-messages {
      flex: 1;
      padding: 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .chat-msg {
      display: flex;
      gap: 10px;
      max-width: 88%;
    }
    .chat-msg.bot { align-self: flex-start; }
    .chat-msg.user { align-self: flex-end; flex-direction: row-reverse; }

    .msg-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      object-fit: cover;
      flex-shrink: 0;
    }
    .msg-bubble {
      padding: 12px 16px;
      border-radius: 18px;
      font-size: 13.5px;
      line-height: 1.5;
    }
    .chat-msg.bot .msg-bubble {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      border-top-left-radius: 4px;
    }
    .chat-msg.user .msg-bubble {
      background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
      color: #fff;
      border-top-right-radius: 4px;
      box-shadow: 0 4px 15px rgba(0, 113, 227, 0.3);
    }

    .typing-indicator {
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 10px 14px;
      background: rgba(255, 255, 255, 0.04);
      border-radius: 16px;
      width: fit-content;
      border-top-left-radius: 4px;
    }
    .typing-dot {
      width: 6px;
      height: 6px;
      background: var(--text-muted);
      border-radius: 50%;
      animation: typingBounce 1.4s infinite ease-in-out both;
    }
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typingBounce {
      0%, 80%, 100% { transform: scale(0); }
      40% { transform: scale(1); }
    }

    .chat-chips {
      padding: 10px 16px;
      display: flex;
      gap: 8px;
      overflow-x: auto;
      border-top: 1px solid var(--border-subtle);
      background: rgba(0,0,0,0.25);
    }
    .chat-chips::-webkit-scrollbar { height: 4px; }
    .chat-chip {
      white-space: nowrap;
      padding: 7px 14px;
      border-radius: var(--radius-full);
      background: rgba(0, 210, 255, 0.08);
      border: 1px solid rgba(0, 210, 255, 0.25);
      color: var(--accent-cyan);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
    }
    .chat-chip:hover {
      background: rgba(0, 210, 255, 0.18);
      transform: translateY(-1px);
    }

    .chat-input-area {
      padding: 14px 16px;
      background: rgba(10, 10, 12, 0.95);
      border-top: 1px solid var(--border-subtle);
      display: flex;
      gap: 10px;
    }
    .chat-input {
      flex: 1;
      padding: 10px 16px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-full);
      color: var(--text-main);
      font-size: 13px;
      outline: none;
    }
    .chat-input:focus { border-color: var(--accent-cyan); }
    .chat-send-btn {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
      border: none;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: var(--transition);
    }
    .chat-send-btn:hover { transform: scale(1.05); }

    .email-highlight {
      display: block;
      margin-top: 8px;
      padding: 10px 14px;
      background: rgba(249, 115, 22, 0.15);
      border: 1px solid rgba(249, 115, 22, 0.4);
      border-radius: 10px;
      color: #fb923c;
      font-weight: 800;
      font-size: 12.5px;
      letter-spacing: 0.04em;
    }
"""

roblox_showcase_html = """
      <!-- Roblox Visual Image Showcase -->
      <div class="roblox-showcase-row">
        <div class="roblox-img-card">
          <div class="roblox-img-wrapper">
            <img src="roblox_studio_showcase.png" alt="Roblox Studio Combat & Physics Systems" />
            <div class="roblox-img-overlay"></div>
          </div>
          <div class="roblox-img-caption">
            <div class="roblox-img-title">Custom Luau Physics &amp; Combat Rigs</div>
            <div class="roblox-img-desc">High-precision raycast hitboxes, R6/R15 custom animation blending, and server-validated combat mechanics built for competitive gameplay.</div>
          </div>
        </div>

        <div class="roblox-img-card">
          <div class="roblox-img-wrapper">
            <img src="roblox_analytics_showcase.png" alt="Roblox Server Lag & Retention Dashboard" />
            <div class="roblox-img-overlay"></div>
          </div>
          <div class="roblox-img-caption">
            <div class="roblox-img-title">120 FPS Audit &amp; LiveOps Engine</div>
            <div class="roblox-img-desc">Memory leak detection, server network micro-profiling, and monetization loop tuning to maximize Robux yield and retention.</div>
          </div>
        </div>
      </div>
"""

chatbot_html = """
  <!-- ===== ANIME AI ASSISTANT CHATBOT ===== -->
  <div class="chatbot-trigger" id="chat-trigger">
    <div class="trigger-pill-callout">
      <span>Talk to Aira ✨</span>
    </div>
    <div class="trigger-avatar-wrap">
      <img src="anime_bot_avatar.png" alt="Aira Anime AI Assistant" class="trigger-avatar-img" />
      <span class="trigger-unread-dot"></span>
    </div>
  </div>

  <div class="chat-window" id="chat-window">
    <div class="chat-header">
      <div class="chat-header-profile">
        <img src="anime_bot_avatar.png" alt="Aira" class="chat-header-avatar" />
        <div class="chat-header-info">
          <div class="name">Aira</div>
          <div class="status"><span class="status-dot-sm"></span> Online • Veira Studio AI</div>
        </div>
      </div>
      <button class="chat-close-btn" id="chat-close">✕</button>
    </div>

    <div class="chat-messages" id="chat-messages">
      <div class="chat-msg bot">
        <img src="anime_bot_avatar.png" alt="Aira" class="msg-avatar" />
        <div class="msg-bubble">
          Konnichiwa! 👋 I'm <strong>Aira</strong>, Veira Studios' AI Assistant. I'm here to answer your questions about our 360° game production, Roblox LiveOps, 120 FPS lag optimization, and project proposals!
          <span class="email-highlight">✉️ CONTACT US AT THIS EMAIL: VEIRAPARTNERSHIP@GMAIL.COM</span>
        </div>
      </div>
    </div>

    <!-- Quick Questions Chips -->
    <div class="chat-chips">
      <div class="chat-chip" onclick="askChip('What full-cycle game services do you offer?')">🎮 Full-Cycle Services</div>
      <div class="chat-chip" onclick="askChip('Tell me about Roblox Luau & LiveOps')">🟠 Roblox Dev &amp; LiveOps</div>
      <div class="chat-chip" onclick="askChip('How do you fix lag & boost FPS?')">⚡ Lag &amp; FPS Optimization</div>
      <div class="chat-chip" onclick="askChip('What are your pricing packages?')">💰 Pricing Packages</div>
      <div class="chat-chip" onclick="askChip('How do I contact the team directly?')">📧 Contact Info</div>
    </div>

    <div class="chat-input-area">
      <input type="text" id="chat-user-input" class="chat-input" placeholder="Ask Aira about studio proposals..." onkeypress="if(event.key==='Enter') sendChatMessage()" />
      <button class="chat-send-btn" onclick="sendChatMessage()">➔</button>
    </div>
  </div>

  <script>
    // Chatbot Toggle Logic
    const chatTrigger = document.getElementById('chat-trigger');
    const chatWindow = document.getElementById('chat-window');
    const chatClose = document.getElementById('chat-close');
    const chatMessages = document.getElementById('chat-messages');

    chatTrigger.addEventListener('click', () => chatWindow.classList.add('open'));
    chatClose.addEventListener('click', () => chatWindow.classList.remove('open'));

    const studioResponses = {
      services: `We offer full-cycle game production across all major platforms:<br />
• <strong>360° Turnkey Production</strong> (Concept → Release)<br />
• <strong>Multiplatform Builds</strong> (PC, macOS, Android)<br />
• <strong>Custom Engine Plugins &amp; C++/C# Extensions</strong><br />
• <strong>120 FPS Optimization &amp; Draw Call Tuning</strong><br />
• <strong>2D/3D Art, Rigging &amp; Character Animation</strong><br />
• <strong>Custom Soundtrack &amp; Adaptive Audio FX</strong><br /><br />
<span class="email-highlight">✉️ CONTACT US AT THIS EMAIL: VEIRAPARTNERSHIP@GMAIL.COM</span>`,
      
      roblox: `Our Roblox Center of Excellence specializes in:<br />
• <strong>Luau Custom Frameworks</strong> (Knit / ProfileService)<br />
• <strong>Monetization &amp; Gacha Economy Tuning</strong><br />
• <strong>Custom R6/R15 Rigs &amp; Particle VFX</strong><br />
• <strong>High-Player Server Lag &amp; Micro-Profile Audits</strong><br /><br />
<span class="email-highlight">✉️ CONTACT US AT THIS EMAIL: VEIRAPARTNERSHIP@GMAIL.COM</span>`,
      
      fps: `Our performance optimization sprint addresses:<br />
• Draw call reduction (-60% to -90%)<br />
• Memory leak detection &amp; GC profiling<br />
• Custom shader optimization &amp; GPU profiling<br />
• Unlocking smooth 120 FPS target locks!<br /><br />
<span class="email-highlight">✉️ CONTACT US AT THIS EMAIL: VEIRAPARTNERSHIP@GMAIL.COM</span>`,
      
      pricing: `We offer 3 clear engagement packages:<br />
1. <strong>Targeted Support</strong>: Standalone plugin, asset suite, or 1-week lag fix.<br />
2. <strong>Co-Development</strong>: Dedicated engineers &amp; artists embedded in your team.<br />
3. <strong>360° Turnkey Build</strong>: Full game build from prototype to store launch.<br /><br />
<span class="email-highlight">✉️ CONTACT US AT THIS EMAIL: VEIRAPARTNERSHIP@GMAIL.COM</span>`,
      
      contact: `For official proposals, partnership inquiries, or custom quotes, reach our executive team directly:<br /><br />
<span class="email-highlight">✉️ CONTACT US AT THIS EMAIL: VEIRAPARTNERSHIP@GMAIL.COM</span>`,

      default: `I am specialized exclusively in Veira Studios game development proposals and studio capabilities! For non-studio questions or custom business inquiries, please reach out to us directly:<br /><br />
<span class="email-highlight">✉️ CONTACT US AT THIS EMAIL: VEIRAPARTNERSHIP@GMAIL.COM</span>`
    };

    function askChip(text) {
      document.getElementById('chat-user-input').value = text;
      sendChatMessage();
    }

    function sendChatMessage() {
      const input = document.getElementById('chat-user-input');
      const query = input.value.trim();
      if (!query) return;

      appendMsg('user', query);
      input.value = '';

      showTyping();

      setTimeout(() => {
        hideTyping();
        const responseText = getStudioResponse(query);
        appendMsg('bot', responseText);
      }, 800);
    }

    function appendMsg(sender, text) {
      const msgDiv = document.createElement('div');
      msgDiv.className = 'chat-msg ' + sender;
      
      if (sender === 'bot') {
        msgDiv.innerHTML = '<img src="anime_bot_avatar.png" class="msg-avatar" /><div class="msg-bubble">' + text + '</div>';
      } else {
        msgDiv.innerHTML = '<div class="msg-bubble">' + text + '</div>';
      }
      
      chatMessages.appendChild(msgDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    let typingElem = null;
    function showTyping() {
      typingElem = document.createElement('div');
      typingElem.className = 'chat-msg bot';
      typingElem.innerHTML = '<img src="anime_bot_avatar.png" class="msg-avatar" /><div class="typing-indicator"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>';
      chatMessages.appendChild(typingElem);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function hideTyping() {
      if (typingElem) { typingElem.remove(); typingElem = null; }
    }

    function getStudioResponse(query) {
      const q = query.toLowerCase();
      if (q.includes('service') || q.includes('full') || q.includes('offer') || q.includes('build') || q.includes('360')) {
        return studioResponses.services;
      }
      if (q.includes('roblox') || q.includes('luau') || q.includes('r6') || q.includes('r15') || q.includes('gacha')) {
        return studioResponses.roblox;
      }
      if (q.includes('lag') || q.includes('fps') || q.includes('optimize') || q.includes('speed') || q.includes('memory')) {
        return studioResponses.fps;
      }
      if (q.includes('price') || q.includes('cost') || q.includes('pack') || q.includes('tier') || q.includes('budget')) {
        return studioResponses.pricing;
      }
      if (q.includes('contact') || q.includes('email') || q.includes('reach') || q.includes('hire') || q.includes('inquiry')) {
        return studioResponses.contact;
      }
      return studioResponses.default;
    }
  </script>
"""

# Insert CSS into <style>
content = content.replace('  </style>', chatbot_css + '\n  </style>')

# Replace Roblox grid start
content = content.replace('<div class="roblox-grid">', roblox_showcase_html + '\n      <div class="roblox-grid">')

# Append chatbot before </body>
content = content.replace('</body>', chatbot_html + '\n</body>')

with open('/Users/albinkrasniqi/Desktop/SITE/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully updated index.html!')
