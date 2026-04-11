#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML генератор для пранков без зависимостей
"""

def generate_matrix_html(duration=15):
    """Генерация HTML для матрицы"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Matrix</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
        }}
        canvas {{
            display: block;
        }}
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = '01';
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);
        
        function draw() {{
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {{
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {{
                    drops[i] = 0;
                }}
                drops[i]++;
            }}
        }}
        
        setInterval(draw, 33);
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_flood_html(duration=10, char=None):
    """Генерация HTML для заливки"""
    chars = char if char else '#@%&*+='
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Flood</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
        }}
        canvas {{
            display: block;
        }}
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = '{chars}';
        
        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            for (let i = 0; i < 200; i++) {{
                const x = Math.random() * canvas.width;
                const y = Math.random() * canvas.height;
                const char = chars[Math.floor(Math.random() * chars.length)];
                const size = 20 + Math.random() * 40;
                const r = Math.floor(Math.random() * 255);
                const g = Math.floor(100 + Math.random() * 155);
                const b = Math.floor(Math.random() * 100);
                
                ctx.fillStyle = `rgb(${{r}},${{g}},${{b}})`;
                ctx.font = size + 'px monospace';
                ctx.fillText(char, x, y);
            }}
        }}
        
        setInterval(draw, 50);
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_glitch_html(duration=10):
    """Генерация HTML для глитча"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Glitch</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
        }}
        canvas {{
            display: block;
        }}
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = '#@%&*';
        
        function draw() {{
            if (Math.random() < 0.1) {{
                ctx.fillStyle = 'black';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }}
            
            const count = 10 + Math.floor(Math.random() * 20);
            for (let i = 0; i < count; i++) {{
                const x = Math.random() * canvas.width;
                const y = Math.random() * canvas.height;
                const len = 5 + Math.floor(Math.random() * 15);
                let text = '';
                for (let j = 0; j < len; j++) {{
                    text += chars[Math.floor(Math.random() * chars.length)];
                }}
                const size = 20 + Math.random() * 40;
                const r = 200 + Math.floor(Math.random() * 55);
                const g = 200 + Math.floor(Math.random() * 55);
                const b = 200 + Math.floor(Math.random() * 55);
                
                ctx.fillStyle = `rgb(${{r}},${{g}},${{b}})`;
                ctx.font = size + 'px monospace';
                ctx.fillText(text, x, y);
            }}
        }}
        
        setInterval(draw, Math.random() * 90 + 10);
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_chinese_attack_html(duration=15):
    """Генерация HTML для китайской атаки"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Chinese Attack</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
        }}
        .char {{
            position: absolute;
            font-family: SimSun, sans-serif;
            font-weight: bold;
            color: lime;
            user-select: none;
        }}
    </style>
</head>
<body>
    <script>
        const chinese = ['警告', '危险', '病毒', '入侵', '黑客', '攻击', '系统', '错误', '崩溃', '删除', '破坏', '感染'];
        
        for (let i = 0; i < 60; i++) {{
            const div = document.createElement('div');
            div.className = 'char';
            div.textContent = chinese[Math.floor(Math.random() * chinese.length)];
            div.style.fontSize = (30 + Math.random() * 50) + 'px';
            div.style.left = Math.random() * window.innerWidth + 'px';
            div.style.top = Math.random() * window.innerHeight + 'px';
            document.body.appendChild(div);
        }}
        
        function update() {{
            document.querySelectorAll('.char').forEach(el => {{
                el.textContent = chinese[Math.floor(Math.random() * chinese.length)];
                const r = 150 + Math.floor(Math.random() * 105);
                const g = Math.floor(Math.random() * 50);
                const b = Math.floor(Math.random() * 50);
                el.style.color = `rgb(${{r}},${{g}},${{b}})`;
                el.style.left = Math.random() * window.innerWidth + 'px';
                el.style.top = Math.random() * window.innerHeight + 'px';
            }});
        }}
        
        setInterval(update, 80);
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_wave_text_html(text, duration=5):
    """Генерация HTML для волны текста"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Wave Text</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        #text {{
            font-family: monospace;
            font-size: 48px;
            color: cyan;
            display: flex;
        }}
        .char {{
            display: inline-block;
        }}
    </style>
</head>
<body>
    <div id="text"></div>
    <script>
        const text = '{text}';
        const container = document.getElementById('text');
        const chars = [];
        
        for (let i = 0; i < text.length; i++) {{
            const span = document.createElement('span');
            span.className = 'char';
            span.textContent = text[i];
            container.appendChild(span);
            chars.push(span);
        }}
        
        let time = 0;
        function animate() {{
            time += 0.05;
            chars.forEach((char, i) => {{
                const offset = Math.sin(time * 5 + i * 0.5) * 30;
                char.style.transform = `translateY(${{offset}}px)`;
            }});
            requestAnimationFrame(animate);
        }}
        
        animate();
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_rainbow_text_html(text, duration=5):
    """Генерация HTML для радужного текста"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Rainbow Text</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        #text {{
            font-family: monospace;
            font-size: 48px;
            display: flex;
        }}
        .char {{
            display: inline-block;
        }}
    </style>
</head>
<body>
    <div id="text"></div>
    <script>
        const text = '{text}';
        const container = document.getElementById('text');
        const chars = [];
        const colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple'];
        
        for (let i = 0; i < text.length; i++) {{
            const span = document.createElement('span');
            span.className = 'char';
            span.textContent = text[i];
            container.appendChild(span);
            chars.push(span);
        }}
        
        let time = 0;
        function animate() {{
            time += 0.1;
            chars.forEach((char, i) => {{
                const colorIndex = Math.floor(i + time) % colors.length;
                char.style.color = colors[colorIndex];
            }});
            requestAnimationFrame(animate);
        }}
        
        animate();
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_fullscreen_text_html(text, duration=5):
    """Генерация HTML для полноэкранного текста"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Fullscreen Text</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: red;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        #text {{
            font-family: Arial, sans-serif;
            font-size: 80px;
            font-weight: bold;
            color: white;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div id="text">{text}</div>
    <script>
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_spam_text_html(text, duration=5):
    """Генерация HTML для спама текстом"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Text Spam</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
        }}
        .text {{
            position: absolute;
            font-family: monospace;
            color: white;
            user-select: none;
        }}
    </style>
</head>
<body>
    <script>
        for (let i = 0; i < 50; i++) {{
            const div = document.createElement('div');
            div.className = 'text';
            div.textContent = '{text}';
            div.style.fontSize = (10 + Math.random() * 40) + 'px';
            div.style.left = Math.random() * window.innerWidth + 'px';
            div.style.top = Math.random() * window.innerHeight + 'px';
            document.body.appendChild(div);
        }}
        
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_image_html(image_url, duration=5):
    """Генерация HTML для отображения изображения"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Image Display</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}
    </style>
</head>
<body>
    <img src="{image_url}" alt="Prank Image">
    <script>
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_spam_windows_html(text, count=5, duration=3):
    """Генерация HTML для спама окнами"""
    windows = []
    for i in range(count):
        window_html = f'''
        <div style="
            position: fixed;
            top: {50 + i * 20}px;
            left: {50 + i * 30}px;
            width: 300px;
            height: 200px;
            background: red;
            border: 3px solid yellow;
            z-index: {10000 + i};
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            font-weight: bold;
            color: white;
            font-size: 24px;
            text-align: center;
            transform: rotate({i * 5 - 10}deg);
        ">
            {text} #{i+1}
        </div>
        '''
        windows.append(window_html)
    
    windows_html = ''.join(windows)
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Spam Windows</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
        }}
    </style>
</head>
<body>
    {windows_html}
    <script>
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_typewriter_html(text, duration=5):
    """Генерация HTML для эффекта печатной машинки"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Typewriter Effect</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        #typewriter {{
            font-family: 'Courier New', monospace;
            font-size: 32px;
            color: green;
            white-space: nowrap;
            overflow: hidden;
            border-right: 2px solid green;
            animation: typing {len(text) * 0.1}s steps({len(text)}, end), blink-caret 0.75s step-end infinite;
        }}
        @keyframes typing {{
            from {{ width: 0 }}
            to {{ width: 100% }}
        }}
        @keyframes blink-caret {{
            from, to {{ border-color: transparent }}
            50% {{ border-color: green }}
        }}
    </style>
</head>
<body>
    <div id="typewriter">{text}</div>
    <script>
        setTimeout(() => window.close(), {(duration + 2) * 1000}); // Additional time after typing
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_zoom_html(text, duration=5):
    """Генерация HTML для эффекта приближения"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Zoom Effect</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        #zoom {{
            font-family: Arial, sans-serif;
            font-weight: bold;
            color: yellow;
            transform-origin: center;
            animation: zoom {duration}s ease-out forwards;
        }}
        @keyframes zoom {{
            0% {{ transform: scale(0.1); opacity: 0; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
    </style>
</head>
<body>
    <div id="zoom">{text}</div>
    <script>
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_shake_html(text, duration=5):
    """Генерация HTML для эффекта тряски"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Shake Effect</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        #shake {{
            font-family: Arial, sans-serif;
            font-weight: bold;
            color: white;
            animation: shake {duration}s linear;
        }}
        @keyframes shake {{
            0%, 100% {{ transform: translate(0, 0); }}
            10%, 30%, 50%, 70%, 90% {{ transform: translate(-5px, -5px); }}
            20%, 40%, 60%, 80% {{ transform: translate(5px, 5px); }}
        }}
    </style>
</head>
<body>
    <div id="shake">{text}</div>
    <script>
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_frame_text_html(text, duration=5):
    """Генерация HTML для текста в рамке"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Text in Frame</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: red;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        #frame {{
            padding: 50px;
            background: black;
            border: 5px solid white;
            font-family: 'Courier New', monospace;
            font-size: 24px;
            color: white;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
        }}
    </style>
</head>
<body>
    <div id="frame">{text}</div>
    <script>
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_fill_screen_html(text, duration=5):
    """Генерация HTML для заполнения экрана текстом"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Fill Screen</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: black;
        }}
        .text {{
            position: absolute;
            font-family: 'Courier New', monospace;
            color: white;
            user-select: none;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <script>
        const text = '{text}';
        const rows = Math.floor(window.innerHeight / 30);
        const cols = Math.floor(window.innerWidth / 12);
        
        for (let row = 0; row < rows; row++) {{
            for (let col = 0; col < cols; col++) {{
                const div = document.createElement('div');
                div.className = 'text';
                div.textContent = text;
                div.style.fontSize = (10 + Math.random() * 20) + 'px';
                div.style.left = (col * 12) + 'em';
                div.style.top = (row * 3) + 'em';
                
                const r = Math.floor(Math.random() * 100);
                const g = Math.floor(150 + Math.random() * 105);
                const b = Math.floor(Math.random() * 100);
                div.style.color = `rgb(${{r}},${{g}},${{b}})`;
                
                document.body.appendChild(div);
            }}
        }}
        
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_ascii_art_html(ascii_art, duration=7, color="white"):
    """Генерация HTML для ASCII-арта"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ASCII Art</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            overflow: auto;
            background: black;
            color: {color};
            font-family: monospace;
            font-size: 14px;
            line-height: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        #art {{
            white-space: pre;
            text-align: center;
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <pre id="art">{ascii_art}</pre>
    <script>
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
        document.documentElement.requestFullscreen().catch(() => {{}});
    </script>
</body>
</html>'''

def generate_minimize_windows_html(duration=5):
    """Генерация HTML для команды свертывания окон (скрипт на JS)"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Minimize Windows Command</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
            font-family: Arial, sans-serif;
            font-size: 24px;
        }}
    </style>
</head>
<body>
    <div>Executing minimize windows command...</div>
    <script>
        // Выполнение команды через встроенную интеграцию с системой
        // (в реальности это будет выполнено на сервере)
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
    </script>
</body>
</html>'''

def generate_window_dance_html(cycles=5, duration=5):
    """Генерация HTML для танца окон (скрипт на JS)"""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Window Dance Command</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: yellow;
            font-family: Arial, sans-serif;
            font-size: 24px;
        }}
    </style>
</head>
<body>
    <div>Executing window dance command ({{cycles}} cycles)...</div>
    <script>
        setTimeout(() => window.close(), {duration * 1000});
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') window.close();
        }});
    </script>
</body>
</html>'''

