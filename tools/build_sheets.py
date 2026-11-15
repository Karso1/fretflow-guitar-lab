import json,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
SONGS=json.loads((ROOT/'content/songs.json').read_text())
FONT='/System/Library/Fonts/STHeiti Light.ttc'
def font(n):return ImageFont.truetype(FONT,n)
SHAPES={
 'C':[-1,3,2,0,1,0],'G':[3,2,0,0,0,3],'Am':[-1,0,2,2,1,0],'F':[-1,-1,3,2,1,1],
 'D':[-1,-1,0,2,3,2],'Em':[0,2,2,0,0,0],'Bm':[-1,2,4,4,3,2],'A':[-1,0,2,2,2,0],
 'E':[0,2,2,1,0,0],'Dm':[-1,-1,0,2,3,1],'G7':[3,2,0,0,0,1],'E7':[0,2,0,1,0,0],
 'F#m':[2,4,4,2,2,2],'Am7':[-1,0,2,0,1,0],'D7':[-1,-1,0,2,1,2],
 'Gmaj7':[3,-1,0,0,0,2],'Cmaj7':[-1,3,2,0,0,0],'F#m7b5':[2,-1,2,2,1,0],
 'B7':[-1,2,1,2,0,2],'Em7':[0,2,2,0,3,3],'Dsus4':[-1,-1,0,2,3,3],
 'A7sus4':[-1,0,2,0,3,3],'Cadd9':[-1,3,2,0,3,3],'D6add9/F#':[2,-1,0,2,0,0]
}
INK='#25282f';BLUE='#3758e8';GRAY='#656b79';LINE='#cdd1dc'
def wrapped(draw,txt,x,y,size,width,fill=INK):
    f=font(size);line=''
    for c in txt:
        if draw.textlength(line+c,font=f)>width:
            draw.text((x,y),line,font=f,fill=fill);y+=size*1.7;line=c
        else:line+=c
    if line:draw.text((x,y),line,font=f,fill=fill);y+=size*1.7
    return y
def chord(draw,name,x,y):
    shape=SHAPES[name];start=1
    draw.text((x+52,y),name,font=font(22),fill=INK,anchor='mt')
    for j in range(6):draw.line((x+16*j,y+55,x+16*j,y+167),fill=GRAY,width=1)
    for k in range(6):draw.line((x,y+55+22*k,x+80,y+55+22*k),fill=GRAY,width=3 if k==0 else 1)
    for j,f in enumerate(shape):
        xx=x+j*16
        if f<=0:draw.text((xx,y+30),'×' if f<0 else '○',font=font(18),fill=GRAY,anchor='mt')
        else:
            yy=y+55+(f-start+.5)*22
            draw.ellipse((xx-6,yy-6,xx+6,yy+6),fill=BLUE)
    draw.text((x+40,y+177),'6  5  4  3  2  1',font=font(13),fill=GRAY,anchor='mt')
for s in SONGS:
    im=Image.new('RGB',(1300,1840),'white');d=ImageDraw.Draw(im)
    d.text((80,62),'FretFlow / 吉他练习谱',font=font(24),fill=BLUE)
    d.text((1220,62),f'{s["number"]:02d} / 40',font=font(22),fill=GRAY,anchor='rt')
    y=130
    y=wrapped(d,s['title'],80,y,50,1130)
    d.text((80,y+8),s['artist']+'   |   指型调 '+s['practiceKey']+'   |   '+s['meter'],font=font(23),fill=GRAY)
    y+=70;d.line((80,y,1220,y),fill=LINE,width=2);y+=30
    y=wrapped(d,'原创伴奏练习 / 简化和弦与右手音型，非原版完整谱。',80,y,23,1120)
    y=wrapped(d,'标准调弦 E A D G B e；图中 X 为不弹，O 为空弦。F 采用四弦简易指型。',80,y,20,1120,GRAY)
    y+=18
    unique=list(dict.fromkeys(s['chords']))
    for i,ch in enumerate(unique):chord(d,ch,100+(i%6)*192,y+(i//6)*210)
    y+=(1+(len(unique)-1)//6)*210+20
    d.text((80,y),'和弦连接练习',font=font(28),fill=INK);y+=52
    y=wrapped(d,'下列方格是换位练习顺序，不代表原曲逐小节转录。先保持拍点，再对照外部完整谱。',80,y,21,1120,GRAY)
    y+=12
    for i,ch in enumerate(s['chords']):
        col=i%4;row=i//4;xx=80+col*285;yy=y+row*77
        d.rectangle((xx,yy,xx+275,yy+65),outline=LINE,width=2)
        d.text((xx+18,yy+17),ch,font=font(28),fill=BLUE)
    y+=((len(s['chords'])+3)//4)*77+30
    d.text((80,y),'右手分解 / 原创单小节练习',font=font(28),fill=INK);y+=75
    first=SHAPES[s['chords'][0]];available=[i for i,v in enumerate(first) if v>=0];bass=available[0]
    bass_tab=5-bass
    pattern=[bass_tab,2,1,0,1,2] if s['meter']=='6/8' else [bass_tab,2,1,0,1,2,1,2]
    if s['meter']=='12/8':pattern=[bass_tab,2,1,0,1,2,bass_tab,2,1,0,1,2]
    # string indices here are high-to-low for TAB, inverse of chord arrays.
    tx=150;tw=1030
    for idx,label in enumerate(['e','B','G','D','A','E']):
        yy=y+idx*28;d.text((95,yy-13),label,font=font(20),fill=GRAY);d.line((tx,yy,1180,yy),fill=GRAY,width=1)
    for i,idx in enumerate(pattern):
        xx=tx+70+(tw-140)*i/(len(pattern)-1);yy=y+idx*28
        fret=first[5-idx]
        d.rectangle((xx-11,yy-13,xx+11,yy+13),fill='white')
        d.text((xx,yy),str(fret),font=font(23),fill=BLUE,anchor='mm')
        d.text((xx,y-34),str(i+1),font=font(17),fill=GRAY,anchor='mm')
    y+=190
    y=wrapped(d,'数字是品位；上方数字仅表示拨弦次序。先以 60 BPM 慢练，注意低音清楚、高音轻，保持均匀。',80,y,21,1120,GRAY)
    y+=18
    d.text((80,y),'本曲练习重点',font=font(26),fill=INK);y+=48
    y=wrapped(d,s['focus'],80,y,25,1120)
    for txt in s['practice'][:2]:y=wrapped(d,'• '+txt,80,y+6,20,1120,GRAY)
    d.line((80,1735,1220,1735),fill=LINE,width=2)
    d.text((80,1760),'FretFlow 原创教学资料 · 曲目权利归原作者 · 完整曲谱请查看站内外部来源',font=font(19),fill=GRAY)
    out=ROOT/s['sheet'];out.parent.mkdir(exist_ok=True,parents=True)
    im.quantize(colors=32).save(out,optimize=True)
print('Rendered',len(SONGS),'PNG sheets;',sum((ROOT/s['sheet']).stat().st_size for s in SONGS),'bytes')
