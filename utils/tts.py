"""
TTS 点读模块
使用浏览器原生 Web Speech API（SpeechSynthesis）
iPad Safari / Chrome 完全支持，零成本无需API key
通过 streamlit.components.v1.html 注入 JS 实现
"""

import streamlit.components.v1 as components


def tts_button(text: str, label: str = "🔊 点我听", rate: float = 0.85,
               key: str = "tts", button_style: str = "") -> None:
    """
    渲染一个点击即播放语音的按钮。
    text: 要朗读的英文文本
    rate: 语速 0.5(慢)~1.0(正常)，默认0.85适合孩子跟读
    """
    # 过滤掉 **bold** 标记，只读纯文本
    import re
    clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # 转义单引号防止JS注入
    clean = clean.replace("'", "\\'")

    html = f"""
    <button onclick="
      var u = new SpeechSynthesisUtterance('{clean}');
      u.lang = 'en-GB';
      u.rate = {rate};
      u.pitch = 1.1;
      var voices = window.speechSynthesis.getVoices();
      var enVoice = voices.find(v => v.lang.startsWith('en'));
      if (enVoice) u.voice = enVoice;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
    "
    style="
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: white;
      border: none;
      border-radius: 12px;
      padding: 10px 20px;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(102,126,234,0.4);
      transition: transform 0.15s ease, box-shadow 0.15s ease;
      font-family: 'Nunito', sans-serif;
      {button_style}
    "
    onmouseover="this.style.transform='translateY(-2px)'"
    onmouseout="this.style.transform='translateY(0)'"
    >{label}</button>
    """
    components.html(html, height=56)


def tts_button_small(text: str, label: str = "🔊", rate: float = 0.85) -> None:
    """小型朗读按钮，用于句子旁边内联"""
    import re
    clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    clean = clean.replace("'", "\\'")

    html = f"""
    <button onclick="
      var u = new SpeechSynthesisUtterance('{clean}');
      u.lang = 'en-GB'; u.rate = {rate}; u.pitch = 1.1;
      var voices = window.speechSynthesis.getVoices();
      var enVoice = voices.find(v => v.lang.startsWith('en'));
      if (enVoice) u.voice = enVoice;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
    "
    style="
      background: #eef2ff; color: #667eea;
      border: 2px solid #667eea; border-radius: 8px;
      padding: 4px 12px; font-size: 0.9rem;
      font-weight: 700; cursor: pointer;
    ">{label}</button>
    """
    components.html(html, height=44)


def auto_play(text: str, rate: float = 0.85) -> None:
    """进入页面自动朗读（用于翻页后自动读新词）"""
    import re
    clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    clean = clean.replace("'", "\\'")

    html = f"""
    <script>
    (function() {{
      function speak() {{
        var u = new SpeechSynthesisUtterance('{clean}');
        u.lang = 'en-GB'; u.rate = {rate}; u.pitch = 1.1;
        var voices = window.speechSynthesis.getVoices();
        var enVoice = voices.find(v => v.lang.startsWith('en'));
        if (enVoice) u.voice = enVoice;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
      }}
      if (window.speechSynthesis.getVoices().length > 0) {{
        setTimeout(speak, 300);
      }} else {{
        window.speechSynthesis.addEventListener('voiceschanged', function() {{
          setTimeout(speak, 300);
        }}, {{once: true}});
      }}
    }})();
    </script>
    """
    components.html(html, height=0)
