#!/usr/bin/env python3
"""Split a built deck back into its parts, using the "<!-- part: NAME start -->" / "<!-- part: NAME end -->" lines the builds write.
   python3 split_parts.py <deck.html> <outdir>      writes <outdir>/<NAME>.html for every part, and <outdir>/<CSS>.css for every
   lesson CSS block a part carries between "/* part: CSS start */" and "/* part: CSS end */" lines (the head of a deck whose
   lesson has a css.css, for example 01c-css-42 inside 01-head-42 of 4.2, or css-45 inside 01-head-45 of 4.5).
   A head part is the filled head (title and description in place of {{TITLE}} and {{DESCRIPTION}}, lesson CSS inserted);
   parts/shared/01-head.html is that head with the placeholders and without the lesson CSS."""
import re,sys,os
deck,out=sys.argv[1],sys.argv[2];os.makedirs(out,exist_ok=True);s=open(deck,encoding='utf-8',newline='').read()
parts=re.findall(r'<!-- part: (\S+) start -->\n(.*?)<!-- part: \1 end -->\n',s,re.S)
assert parts and ''.join('<!-- part: %s start -->\n%s<!-- part: %s end -->\n'%(n,t,n) for n,t in parts)==s,'markers do not cover the whole file'
for n,t in parts:
    for c,css in re.findall(r'/\* part: (\S+) start \*/\n(.*?)/\* part: \1 end \*/\n',t,re.S):
        open(os.path.join(out,c+'.css'),'w',encoding='utf-8',newline='').write(css);print(c+'.css',len(css))
    open(os.path.join(out,n+'.html'),'w',encoding='utf-8',newline='').write(t);print(n,len(t))
