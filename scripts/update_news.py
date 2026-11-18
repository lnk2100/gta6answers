"""Collect source headlines only. Preserve existing data on fetch/parser failure."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone
import json, re, subprocess
ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://www.rockstargames.com/VI'
class NewsLinks(HTMLParser):
 def __init__(self): super().__init__(); self.current=None; self.parts=[]; self.items=[]
 def handle_starttag(self,tag,attrs):
  href=dict(attrs).get('href','')
  if tag=='a' and urlparse(href).hostname=='www.rockstargames.com' and urlparse(href).path.startswith('/newswire/article/'):
   self.current=href.split('?')[0];self.parts=[]
 def handle_data(self,data):
  if self.current:self.parts.append(data)
 def handle_endtag(self,tag):
  if tag=='a' and self.current:
   title=' '.join(' '.join(self.parts).split())
   date=re.search(r'\s([A-Z][a-z]+ \d{1,2}, \d{4})$',title)
   published=date.group(1) if date else None
   if date:title=title[:date.start()]
   if title and len(title)<240:self.items.append({'title':title,'url':self.current,'published':published,'source':'Rockstar Games'})
   self.current=None

def collect(markup):
 parser=NewsLinks();parser.feed(markup)
 items=list({i['url']:i for i in parser.items}.values())[:12]
 if not items:raise ValueError('Official page contains no usable news links. Keeping previous feed; investigate source changes.')
 return items

def main():
 response=subprocess.run(['curl','--silent','--show-error','--fail','--location','--proto','=https','--proto-redir','=https','--max-time','45','--retry','2',SOURCE],capture_output=True,text=True,check=True)
 items=collect(response.stdout)
 path=ROOT/'content/official-news.json'
 previous=json.loads(path.read_text()) if path.exists() else {}
 if previous.get('items')==items:
  print('No headline changes. No deployment needed.');return
 payload={'sourceUrl':SOURCE,'updated':datetime.now(timezone.utc).isoformat(timespec='seconds'),'items':items}
 temp=path.with_suffix('.tmp');temp.write_text(json.dumps(payload,indent=2)+'\n');temp.replace(path)
 print(f'Saved {len(items)} official news links.')
if __name__=='__main__':main()
