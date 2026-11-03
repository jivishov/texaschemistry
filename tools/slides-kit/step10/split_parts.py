#!/usr/bin/env python3
"""Split a built deck back into its parts, using the "<!-- part: NAME start -->" / "<!-- part: NAME end -->" lines the builds write.
   python3 split_parts.py <deck.html> <outdir>      writes <outdir>/<NAME>.html for every part (and 01c-css-42.css for the 4.2 head)
   For 4.2 the head part is 01-head-42: 01-head.html with the title, description and og:title replaced and 01c-css-42.css inserted
   before </style> between "/* part: 01c-css-42 start */" and "/* part: 01c-css-42 end */" lines; the split writes both files."""
import re,sys,os
deck,out=sys.argv[1],sys.argv[2];os.makedirs(out,exist_ok=True);s=open(deck,encoding='utf-8').read()
parts=re.findall(r'<!-- part: (\S+) start -->\n(.*?)<!-- part: \1 end -->\n',s,re.S)
assert parts and ''.join('<!-- part: %s start -->\n%s<!-- part: %s end -->\n'%(n,t,n) for n,t in parts)==s,'markers do not cover the whole file'
for n,t in parts:
    m=re.search(r'/\* part: 01c-css-42 start \*/\n(.*?)/\* part: 01c-css-42 end \*/\n',t,re.S)
    if m:open(os.path.join(out,'01c-css-42.css'),'w',encoding='utf-8').write(m.group(1))
    open(os.path.join(out,n+'.html'),'w',encoding='utf-8').write(t);print(n,len(t))
