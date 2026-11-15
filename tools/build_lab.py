import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'content/original.html').read_text()
s=s.replace('</head>','<link rel="stylesheet" href="lab.css"></head>')
s=s.replace('<title>FretFlow · 吉他自由练习室</title>','<title>FretFlow · 指板实验室</title>')
header='''<header class="lab-header"><a class="lab-logo" href="index.html">fret<i>flow</i><b>.</b></a><nav aria-label="吉他实验室导航"><button data-go="fretboard">指板地图</button><button data-go="chords">和弦</button><button data-go="progressions">进行</button><button data-go="practice">训练计划</button><a href="index.html#library">40 首曲库</a></nav></header>'''
s=s.replace('<body>','<body>'+header)
s=s.replace('function go(view){','function go(view){if(view===\'home\'){location.href="index.html";return;}')
s=s.replace("const initial=location.hash.slice(1);","const initial=location.hash.slice(1)||'fretboard';")
s=s.replace("$('progAllSongs').onclick=()=>go('songs')","$('progAllSongs').onclick=()=>location.href='index.html#library'")
s=s.replace('从和弦进行，进入具体歌曲。','我以前添加的歌曲。')
s=s.replace('每首歌提供主要和弦、适用段落和简化练习提示；点击歌曲可打开详情，再到外部曲谱网站查看具体的吉他谱。不会把四和弦练习循环冒充原版完整谱。','这是旧版自选歌曲管理，保留原有本机收藏。新版 40 首曲库含试听、解析与谱图，请点击顶部“40 首曲库”。')
s=re.sub(r'<footer class="footer">[\s\S]*?</footer>','<footer class="footer">FretFlow 吉他实验室 / 标准调弦计算，试听为合成示意音色。练习记录保存在当前浏览器。<br><a href="index.html#library">回到新版曲库：试听、解析与谱图</a></footer>',s,count=1)
s=s.replace('离线可用 · <strong>自动保存练习</strong>','<strong>本机自动保存练习</strong>')
(ROOT/'lab.html').write_text(s)
print('Preserved original music engine in lab.html')
