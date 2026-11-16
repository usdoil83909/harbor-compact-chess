import json,os,sys,urllib.error as e,urllib.request as r
E=os.environ.get("MAKEFUN_ENV_URL")
if"--selftest"in sys.argv:E=1
if not E:sys.exit("E")
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':2e4}
N=(18,33,31,14,-14,-31,-33,-18)
K=(1,-1,16,-16,17,15,-15,-17)
S=(17,15,-15,-17,16,-16,1,-1)
W='PNBRQK';w='pnbrqk'
def O(j):return 0<=j<128and not(j&8)
def P(F):
 b=[0]*128;t=F.split()[0];r=7;x=0
 for c in t:
  if c=='/':r-=1;x=0
  elif c.isdigit():x+=int(c)
  else:b[r*16+x]=c;x+=1
 s=F.split();return b,s[1],s[2],0,0,0
def J(n,k,o,t):
 for d in N:
  j=k+d
  if O(j)and abs((j%16)-(k%16))<=2and n[j]and n[j]in o and n[j].lower()=='n':return 0
 for d in K:
  j=k+d
  if O(j)and abs((j%16)-(k%16))<=1and n[j]and n[j]in o and n[j].lower()=='k':return 0
 for d in S:
  j=k
  while 1:
   j+=d
   if not O(j):break
   if n[j]:
    if n[j]in o and n[j].lower()in('qb'if abs(d)in(15,17)else'qr'):return 0
    break
 for d in(-15,-17)if t=='w'else(15,17):
  j=k+d
  if O(j)and(n[j]=='p'if t=='w'else n[j]=='P'):return 0
 return 1
def M(b,t,c,h):
 m=[];o=W if t=='w'else w;O_=o.swapcase();K_='k'if t=='w'else'K';p=16 if t=='w'else -16
 for i,q in enumerate(b):
  if not q or q not in o:continue
  v=q.lower()
  if v=='p':
   j=i+p
   if O(j)and not b[j]:m+=[(i,j,'')]
   if(i//16==1and t=='w'or i//16==6and t!='w')and not b[i+p]and not b[i+2*p]:m+=[(i,i+2*p,'')]
   for d in(15,17)if t=='w'else(-15,-17):
    j=i+d
    if O(j)and abs((j%16)-(i%16))==1and b[j]and b[j]in O_ and b[j]!=K_:m+=[(i,j,'')]
  elif v=='n':
   for d in N:
    j=i+d
    if O(j)and abs((j%16)-(i%16))<=2and(not b[j]or(b[j]in O_ and b[j]!=K_)):m+=[(i,j,'')]
  elif v=='k':
   for d in K:
    j=i+d
    if O(j)and abs((j%16)-(i%16))<=1and(not b[j]or(b[j]in O_ and b[j]!=K_)):m+=[(i,j,'')]
  else:
   for d in S if v=='q'else(16,-16,1,-1)if v=='r'else(17,15,-15,-17):
    j=i
    while 1:
     j+=d
     if not O(j):break
     if b[j]:
      if b[j]in O_ and b[j]!=K_:m+=[(i,j,'')]
      break
     m+=[(i,j,'')]
 l=[];o=w if t=='w'else W
 for f,T,p in m:
  n=b[:];c=n[f];n[T]=c+p;n[f]=0;q=c.lower();k=n.index('K'if t=='w'else'k')
  if J(n,k,o,t):l+=[(f,T,p,h)]
 return l
def H(b,t):
 s=0
 for i,p in enumerate(b):
  if not p:continue
  v=V[p.lower()]*(1 if p.isupper()==(t=='w')else-1)
  if p.lower()=='p':v+=(10 if 3<=i//16<=4 and 3<=i%16<=4 else-10)*(1 if p.isupper()==(t=='w')else-1)
  if p.lower()=='n':v+=(10 if 2<=i//16<=5 and 2<=i%16<=5 else-10)*(1 if p.isupper()==(t=='w')else-1)
  s+=v
 return s
C=0;L=4000
def N_(b,t,a,B,d,c,h):
 global C
 if C>=L or d<=0:return H(b,t)
 C+=1
 m=M(b,t,c,h)
 if not m:
  o=w if t=='w'else W
  k=b.index('K'if t=='w'else'k')
  return -20000-d if J(b,k,o,t)==0 else 0
 m.sort(key=lambda x:-(V[b[x[1]].lower()]if b[x[1]]else 0));v=-20000
 for f,T,p,h in m:
  n=b[:];c=n[f];n[T]=c+p;n[f]=0
  u=-N_(n,'b'if t=='w'else'w',-B,-a,d-1,c,h)
  if u>v:v=u
  if v>a:a=v
  if a>=B:break
 return v
def U(f):
 b,t,c,_,h,_=P(f);m=None;d=-20000
 for i in range(1,64):
  global C;C=0
  M_=M(b,t,c,h)
  M_.sort(key=lambda x:-(V[b[x[1]].lower()]if b[x[1]]else 0))
  for x,y,p,h in M_:
   n=b[:];c=n[x];n[y]=c+p;n[x]=0
   u=-N_(n,'b'if t=='w'else'w',-20000,-d,i-1,c,h)
   if u>d:d,m=u,(x,y,p)
   if C>=L:break
  if C>=L:break
 if not m:return''
 x,y,p=m
 A="abcdefgh";return A[x%16]+str(1+x//16)+A[y%16]+str(1+y//16)+(p if p else'')
def P_(f,d):
 b,t,c,_,h,_=P(f)
 def r(b,t,c,h,d):
  if d==0:return 1
  n=0
  for x,y,p,h in M(b,t,c,h):
   u=b[:];c=u[x];u[y]=c+p;u[x]=0
   n+=r(u,'b'if t=='w'else'w',c,h,d-1)
  return n
 return r(b,t,c,h,d)
F="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
if E==1:print(P_(F,1),P_(F,2),P_(F,3));sys.exit()
def post(p,j):
 q=r.Request(E+p,data=json.dumps(j).encode())
 try:
  with r.urlopen(q)as x:return json.load(x)
 except e.HTTPError as x:sys.exit(f"{p}:{x.code}")
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":U(g["fen"])})
 print(g['game'],g['outcome'],g['reason'],file=sys.stderr)
print(g.get('wins'),g.get('draws'),g.get('losses'),file=sys.stderr)