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
