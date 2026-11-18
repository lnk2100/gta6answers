from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]; dist=root/'dist'
class Page(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]; self.h1=0; self.description=False; self.canonical=False; self.main=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1': self.h1+=1
  if tag=='main': self.main=True
  if tag=='meta' and a.get('name')=='description': self.description=bool(a.get('content'))
  if tag=='link' and a.get('rel')=='canonical': self.canonical=True
  for key in ('href','src'):
   if a.get(key,'').startswith('/'): self.links.append(a[key])
files=list(dist.rglob('*.html'))
for f in files:
 p=Page(); p.feed(f.read_text()); assert p.h1==1 and p.description and p.canonical and p.main,f
 for link in p.links:
  path=dist/urlsplit(link).path.lstrip('/')
  if path.is_dir(): path=path/'index.html'
  assert path.is_file(),(f,link)
ET.parse(dist/'sitemap.xml')
articles=json.loads((root/'content/articles.json').read_text()); assert len({a['slug'] for a in articles})==len(articles)
for a in articles:
 assert a['status'] in ['Verified','Reported','Editorial','Unconfirmed','Pre-release']
 if a['status'] in ('Verified','Reported'): assert a.get('source')
 assert a.get('source') in json.loads((root/'content/site.json').read_text())['sources']
 assert a.get('updated') and a.get('spoiler')
print(f'PASS: {len(files)} HTML documents; internal links/assets, one H1, description, canonical, main landmark, sitemap XML, article slugs and evidence labels.')
