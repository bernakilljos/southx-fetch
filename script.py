import requests,os
from bs4 import BeautifulSoup
base='https://moderngov.southwark.gov.uk/'
s=requests.Session(); h={'User-Agent':'Mozilla/5.0'}
os.makedirs('out',exist_ok=True)
# calendar jan
urls={'cal-jan':'mgCalendarMonthView.aspx?M=1&DD=2026&CID=0&OT=&C=-1&MR=0'}
for name,path in urls.items():
 data=s.get(base+path,headers=h).content; open('out/'+name+'.html','wb').write(data)
 soup=BeautifulSoup(data,'html.parser')
 links=[]
 for a in soup.select('a[href*=ieListDocuments]'):
  title=a.get('title',''); txt=a.get_text(' ',strip=True)
  links.append((a['href'],title,txt))
 print('links',links)
 for i,(u,t,txt) in enumerate(links):
  # save meetings; capture all Jan
  d=s.get(base+u.replace('&amp;','&'),headers=h).content
  fname=f'meet{i}.html';open('out/'+fname,'wb').write(d)
  with open('out/index.txt','a') as f:f.write(f'{i}|{u}|{t}|{txt}\n')
  so=BeautifulSoup(d,'html.parser')
  # download every pdf linked agenda reports
  for j,a in enumerate(so.select('a[href]')):
   href=a['href'];
   if '.pdf' not in href.lower() and 'MGConvert2PDF' not in href and 'MZdocuments' not in href: continue
   try:data=s.get(requests.compat.urljoin(base,href),headers=h).content
   except Exception as e: print(e);continue
   open(f'out/meet{i}-{j}.pdf','wb').write(data)
   with open('out/pdfs.txt','a') as f:f.write(f'{i}-{j}|{href}|{a.get_text(" ",strip=True)}|{len(data)}\n')
