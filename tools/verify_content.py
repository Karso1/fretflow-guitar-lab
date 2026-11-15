import json,re
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
songs=json.loads((ROOT/'content/songs.json').read_text())
old=json.loads((ROOT/'content/original-songs.json').read_text())
app=(ROOT/'app.js').read_text()
assert len(songs)==40
assert len({s['id'] for s in songs})==40
for s in songs:
    assert re.fullmatch(r'[A-Za-z0-9_-]{11}',s['youtube']),s['id']
    assert s['scoreUrl'].startswith('https://')
    assert len(s['practice'])==4
    assert all(len(s['analysis'][k])>=40 for k in ['meaning','listen','harmony','rhythm','sing']),s['id']
    assert (ROOT/s['sheet']).is_file()
    with Image.open(ROOT/s['sheet']) as im:
        assert im.size==(1300,1840)
        im.verify()
    for ch in s['chords']:assert f'{ch}:' in app or f"'{ch}':" in app,ch
for o in old:
    s=next(s for s in songs if s['id']==o['id'])
    assert s['originalScoreUrl']==o['url'],o['id']
for icon in set(re.findall(r"ico\('([^']+)'\)",app)):
    assert (ROOT/'assets/icons'/f'{icon}.svg').is_file(),icon
for f in ['index.html','app.js','songs.js','style.css','detail.css','lab.html','lab.css','vendor/motion.js']:
    assert (ROOT/f).is_file(),f
print('PASS: 40 complete records, 40 valid archived PNGs, every practice chord supported, all 14 original chart URLs preserved, core static assets present.')
