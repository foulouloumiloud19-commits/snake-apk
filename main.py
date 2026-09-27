import array,math,os,random,sys,pygame
pygame.init()
try: pygame.display.init()
except: pass
try: pygame.key.stop_text_input()
except: pass
try: pygame.mixer.init(22050,-16,1,512)
except: pass
try:
 I=pygame.display.Info();W=I.current_w or 720;H=I.current_h or 1280
except Exception:
 W,H=720,1280
try:
 screen=pygame.display.set_mode((W,H))
except Exception:
 pygame.display.quit();pygame.display.init();screen=pygame.display.set_mode((W,H))
pygame.display.set_caption("FOULOLOU MILOUD'S RIVAL CENTIPEDE")
HH=84;GH=int(H*.49);PH=H-GH;clock=pygame.time.Clock()
accel=vib=None
try:
 from plyer import accelerometer,vibrator
 accelerometer.enable();accel=accelerometer;vib=vibrator
except: pass
def vibrate(t=.08):
 try:
  if vib:vib.vibrate(t)
 except:pass
CANDS=["/storage/emulated/0/Download/music","/storage/emulated/0/Download",
 os.path.join(os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd(),"music"),
 os.path.join(os.getcwd(),"music")]
MF=CANDS[0];playlist=["AUDIO: OFF"];aidx=0;abtxt="";abtmr=0
def scan_music():
 global playlist,MF,aidx
 playlist=["AUDIO: OFF"]
 for p in CANDS:
  if os.path.isdir(p):
   try:
    z=[f for f in sorted(os.listdir(p)) if f.lower().endswith((".mp3",".wav",".ogg"))]
    if z: MF=p;playlist+=z;break
   except:pass
 aidx=min(aidx,len(playlist)-1)
scan_music()
def stop_music():
 try:pygame.mixer.music.stop()
 except:pass
def chg_trk(step=1):
 global aidx,abtxt,abtmr
 scan_music()
 if len(playlist)<2:abtxt="NO SONGS!";abtmr=90;return
 aidx=(aidx+step)%len(playlist);n=playlist[aidx]
 if n=="AUDIO: OFF":stop_music();abtxt="AUDIO STOPPED"
 else:
  try:
   pygame.mixer.music.load(os.path.join(MF,n));pygame.mixer.music.set_volume(.65);pygame.mixer.music.play(-1);abtxt=f"PLAYING: {n[:16]}"
  except:abtxt=f"CANNOT PLAY: {n[:16]}"
 abtmr=90
def gen(a,b,d,v=.3):
 r=22050;n=int(r*d);x=array.array("h")
 for i in range(n):
  t=i/n;x.append(int(math.sin(2*math.pi*(a+(b-a)*t)*i/r)*(1-t)*v*32767))
 return pygame.mixer.Sound(buffer=x.tobytes())
try:
 snd=[gen(*x) for x in [(450,950,.08,.25),(600,1300,.15,.35),(300,1400,.25,.35),(500,1500,.3,.4),(800,400,.18,.3),(350,100,.4,.4),(220,140,.15,.4),(150,900,.35,.45),(700,200,.2,.35),(320,1600,.45,.45)]]
except:snd=[None]*10
def play(x):
 try:
  if x:x.play()
 except:pass
eat,hunt,bonus,quest,alert,gameover,hit,kill,repulse,levelup=snd
SF="centipede_save.txt"
def load_data():
 try:
  a=open(SF).read().strip().split(",")
  return (int(a[0]),int(a[1])) if len(a)>1 else (0,0)
 except:return 0,0
def save_data(s,c):
 try:open(SF,"w").write(f"{s},{c}")
 except:pass
hisc,coins=load_data()
f28=pygame.font.SysFont("arial",28,True);f46=pygame.font.SysFont("arial",46,True)
f32=pygame.font.SysFont("arial",32,True);f27=pygame.font.SysFont("arial",27,True)
f24=pygame.font.SysFont("arial",24,True);f64=pygame.font.SysFont("arial",64,True)
SKINS=[(f"{i+1}/16 {n}",d,l,g) for i,(n,d,l,g) in enumerate([
("NEON GREEN",(10,150,40),(30,255,90),(140,255,160)),("ULTRA CYAN",(0,140,190),(0,240,255),(170,250,255)),
("HYPER ORANGE",(190,50,0),(255,120,0),(255,200,90)),("GOLDEN SUN",(170,130,0),(255,230,0),(255,255,150)),
("PLASMA VIOLET",(120,20,180),(220,60,255),(245,160,255)),("POLAR ICE",(50,90,125),(150,230,255),(220,250,255)),
("CRIMSON BLOOD",(170,10,35),(255,40,85),(255,130,160)),("RADIOACTIVE",(95,150,0),(210,255,0),(235,255,130)),
("HOT PINK",(170,20,110),(255,55,200),(255,160,235)),("DEEP OCEAN",(10,60,160),(40,160,255),(150,215,255)),
("MAGMA LAVA",(180,40,10),(255,100,20),(255,190,80)),("CHROME WHITE",(110,120,135),(235,245,255),(255,255,255)),
("METALLIC COPPER",(140,65,25),(245,140,70),(255,195,130)),("AQUA MINT",(20,140,125),(50,255,230),(170,255,245)),
("COSMIC DUSK",(80,20,130),(180,80,255),(220,160,255)),("SHADOW ONYX",(35,40,50),(140,155,170),(210,220,235))])]
SL=["SPEED: 1x (SLOW)","SPEED: 2x (NORMAL)","SPEED: 3x (FAST)","SPEED: 4x (TURBO)"]
CM=["CTRL: BUTTONS","CTRL: SWIPE","CTRL: GYRO"];CS=["PAD","SWIPE","GYRO"]
OM=["OBJECTS: ALL ON","OBJECTS: WALLS","OBJECTS: CHASER","OBJECTS: PETS","OBJECTS: OFF"]
DM=["DIFF: EASY (5 LIVES)","DIFF: NORMAL (3 LIVES)","DIFF: HARD (2 LIVES)","DIFF: EXTREME (1 LIFE)"]
scol=0;sspeed=1;sctrl=0;sobj=0;sdiff=1;in_menu=True
wsurf=pygame.Surface((W,GH));random.seed(42)
for y in range(GH):
 f=y/GH;pygame.draw.line(wsurf,(int(32+f*14),int(60+f*22),int(14+f*8)),(0,y),(W,y))
for _ in range(75):
 x=random.randint(15,W-15);y=random.randint(HH+15,GH-15)
 for dx,dy in [(-3,-7),(0,-9),(3,-7)]:pygame.draw.line(wsurf,(55,105,26),(x,y),(x+dx,y+dy),2)
for _ in range(30):pygame.draw.circle(wsurf,random.choice([(255,240,100),(255,140,180),(240,240,255),(140,200,255)]),(random.randint(20,W-20),random.randint(HH+20,GH-20)),2)
for _ in range(18):pygame.draw.ellipse(wsurf,(80,85,75),(random.randint(25,W-25),random.randint(HH+25,GH-25),random.randint(6,12),random.randint(4,7)))
pygame.draw.lines(wsurf,(125,95,50),False,[(-20,int(GH*.72)),(int(W*.32),int(GH*.58)),(int(W*.65),int(GH*.62)),(W+20,int(GH*.32))],int(W*.13))
random.seed()
psurf=pygame.Surface((W,PH));psurf.fill((11,14,20))
for x in range(0,W,38):pygame.draw.line(psurf,(18,26,38),(x,0),(x,PH))
for y in range(0,PH,38):pygame.draw.line(psurf,(18,26,38),(0,y),(W,y))
msurf=pygame.Surface((W,H))
for y in range(H):
 f=y/H;pygame.draw.line(msurf,(int(8+f*22),int(10+f*14),int(24+f*40)),(0,y),(W,y))
mx,my=int(W*.5),int(H*.42)
for r,c in [(135,(30,45,75)),(125,(45,68,105)),(115,(230,242,255)),(105,(255,255,255))]:pygame.draw.circle(msurf,c,(mx,my),r)
pygame.draw.circle(msurf,(255,255,255),(mx-12,my-12),105);random.seed(101)
for _ in range(45):pygame.draw.circle(msurf,(255,255,255),(random.randint(10,W-10),random.randint(15,int(H*.85))),random.choice([1,2,2]))
random.seed()
for bx,by,bw,bh in [(0,int(H*.72),70,350),(60,int(H*.68),90,400),(140,int(H*.75),80,320),(W-220,int(H*.74),75,340),(W-150,int(H*.66),85,420),(W-70,int(H*.71),75,360)]:
 pygame.draw.rect(msurf,(14,18,30),(bx,by,bw,bh));pygame.draw.rect(msurf,(0,180,255),(bx,by,bw,bh),1)
 for yy in range(by+16,by+bh-40,24):
  for xx in range(bx+12,bx+bw-14,18):
   if (xx+yy)%5:pygame.draw.rect(msurf,(0,240,255),(xx,yy,8,12))
pr=pygame.Rect(int(W*.30),int(GH*.54),int(W*.40),int(GH*.28))
PT=[((20,80,150),(35,140,210),(140,230,255),(60,48,25)),((15,110,120),(30,180,170),(160,255,240),(50,52,28)),((70,25,120),(120,45,180),(220,150,255),(55,35,45)),((15,90,60),(30,160,100),(140,255,190),(50,45,20)),((120,40,20),(200,75,30),(255,190,120),(65,38,18))]
cpt=npt=0;ptrans=0
def lerp(a,b,t):return tuple(int(x+(y-x)*t) for x,y in zip(a,b))
def draw_pond(s,t):
 global cpt,npt,ptrans
 ptrans+=.003
 if ptrans>=1:ptrans=0;cpt=npt;npt=random.choice([i for i in range(5) if i!=npt])
 a,b=PT[cpt],PT[npt];bank=lerp(a[3],b[3],ptrans);deep=lerp(a[0],b[0],ptrans);mid=lerp(a[1],b[1],ptrans);gl=lerp(a[2],b[2],ptrans)
 pygame.draw.ellipse(s,bank,(pr.x-7,pr.y-5,pr.w+14,pr.h+10));pygame.draw.ellipse(s,deep,pr);pygame.draw.ellipse(s,mid,(pr.x+8,pr.y+6,pr.w-16,pr.h-12))
 for i,z in enumerate((1.5,2.3,.8)):
  e=int(((t*z+i*1.8)%3)*9);pygame.draw.ellipse(s,gl,(pr.centerx-30-e,pr.centery-12-e//2,60+e*2,24+e),1)
 x=pr.centerx-22+int(math.sin(t*1.5)*5);pygame.draw.ellipse(s,(255,255,255),(x,pr.centery-10,32,8));pygame.draw.ellipse(s,gl,(x-4,pr.centery-12,40,12),1)
TS=[((52,138,44),(28,92,32),(16,58,22)),((240,160,20),(200,100,15),(140,60,10)),((255,130,170),(220,80,130),(150,40,80)),((80,210,235),(35,150,180),(15,90,120)),((190,90,255),(130,40,200),(80,20,130))]
csidx=0;sstm=400;ttrees=[(int(W*.12),int(GH*.24),32),(int(W*.88),int(GH*.20),30),(int(W*.14),int(GH*.82),28),(int(W*.86),int(GH*.82),29),(int(W*.50),int(GH*.18),26)]
def upd_trees(l):
 global csidx,sstm
 sstm-=1
 if sstm<=0:csidx=(csidx+1)%5;sstm=max(180,450-l*30)
def draw_tree(s,x,y,r):
 top,mid,dark=TS[csidx];pygame.draw.ellipse(s,(15,26,8),(x-int(r*1.3),y+4,int(r*2.6),int(r*1.1)));pygame.draw.rect(s,(65,38,16),(x-6,y-28,12,34),border_radius=4)
 for rr,c,dx,dy in [(r,dark,0,-28),(int(r*.82),mid,-4,-32),(int(r*.52),top,-6,-35)]:pygame.draw.circle(s,c,(x+dx,y+dy),rr)
QP=[("HUNT 2 RABBITS","HUNT_RABBIT",2),("EAT 4 APPLES","EAT_APPLE",4),("USE 2 BOOSTS","USE_BOOST",2),("HUNT 2 SQUIRRELS","HUNT_SQUIRREL",2),("DEFEAT 1 RIVAL","KILL_RIVAL",1)]
aq={"desc":QP[0][0],"type":QP[0][1],"target":QP[0][2],"count":0};qbtmr=0;qbtxt=""
def prog_quest(t,n=1):
 global aq,coins,qbtxt,qbtmr
 if aq["type"]==t:
  aq["count"]+=n
  if aq["count"]>=aq["target"]:
   coins+=50;qbtxt="QUEST COMPLETE! +50 COINS";qbtmr=120;z=random.choice(QP);aq={"desc":z[0],"type":z[1],"target":z[2],"count":0};play(quest);vibrate(.2)
parts=[]
def emit(x,y,c,n=10):
 for _ in range(n):
  a=random.random()*math.tau;v=random.uniform(1.5,4);parts.append([float(x),float(y),math.cos(a)*v,math.sin(a)*v,random.uniform(2,4),random.randint(12,20),c])
def upd_parts(s):
 for p in parts[:]:
  p[0]+=p[2];p[1]+=p[3];p[4]=max(.5,p[4]-.16);p[5]-=1
  if p[5]<=0:parts.remove(p)
  else:pygame.draw.circle(s,p[6],(int(p[0]),int(p[1])),int(p[4]))
AT=["RABBIT","MOUSE","SQUIRREL"];ACOL={"RABBIT":((255,245,245),(255,140,160),20),"SQUIRREL":((230,110,30),(170,65,15),22),"MOUSE":((160,155,165),(90,85,95),18)}
def mk_animal():
 t=random.choice(AT);bc,dc,z=ACOL[t]
 return {"type":t,"x":float(random.randint(70,W-70)),"y":float(random.randint(HH+30,GH-70)),"angle":random.random()*math.tau,"speed":random.uniform(.7,1.4),"turn_timer":random.randint(60,180),"hop_timer":random.random()*5,"body_col":bc,"detail_col":dc,"size":z}
animals=[mk_animal() for _ in range(random.randint(3,4))]
def upd_anim(hx,hy):
 for a in animals:
  a["turn_timer"]-=1;a["hop_timer"]+=.12
  if a["turn_timer"]<=0:a["angle"]+=random.uniform(-1.2,1.2);a["turn_timer"]=random.randint(50,150)
  d=math.hypot(a["x"]-hx,a["y"]-hy);v=a["speed"]*.5 if pr.collidepoint(int(a["x"]),int(a["y"])) else a["speed"]
  if mt>0 and d<140:q=math.atan2(hy-a["y"],hx-a["x"]);a["x"]+=math.cos(q)*3.5;a["y"]+=math.sin(q)*3.5
  elif d<95:q=math.atan2(a["y"]-hy,a["x"]-hx);a["angle"]=q;a["x"]+=math.cos(q)*v*2.2;a["y"]+=math.sin(q)*v*2.2
  else:a["x"]+=math.cos(a["angle"])*v;a["y"]+=math.sin(a["angle"])*v
  a["x"]=max(30,min(W-30,a["x"]));a["y"]=max(HH+25,min(GH-30,a["y"]))
def draw_animal(s,a):
 x,y,z=int(a["x"]),int(a["y"]),a["size"];h=int(math.sin(a["hop_timer"]*3.5)*3);bc,dc=a["body_col"],a["detail_col"]
 pygame.draw.ellipse(s,(14,24,8),(x-z,y+z//2,z*2,z//2+3))
 pygame.draw.ellipse(s,bc,(x-z,y-z//2+h,z*2,int(z*1.3)))
 if a["type"]=="RABBIT":
  for ex in (-7,1):pygame.draw.ellipse(s,bc,(x+ex,y-z-14+h,7,18))
  pygame.draw.circle(s,(255,255,255),(x-z+2,y+h),5);pygame.draw.circle(s,(20,20,20),(x+6,y-6+h),3)
 elif a["type"]=="SQUIRREL":
  pygame.draw.circle(s,bc,(x+z-4,y-4+h),int(z*.65));pygame.draw.ellipse(s,dc,(x-z-12,y-z-8+h,16,26));pygame.draw.circle(s,bc,(x-z-4,y-z+h),8);pygame.draw.circle(s,(10,10,10),(x+z-1,y-6+h),3)
 else:
  pygame.draw.ellipse(s,bc,(x-z,y-z//2+h,int(z*1.9),z))
  for ex in (2,12):pygame.draw.circle(s,dc,(x+ex,y-z+2+h),6)
  pygame.draw.line(s,dc,(x-z,y+h),(x-z-14,y-4+h),3);pygame.draw.circle(s,(10,10,10),(x+z-2,y-2+h),2)
pw={"x":-100,"y":-100,"type":"REPULSE","active":False,"timer":160,"duration":340};ft=st=mt=dpt=rt=0
def upd_pw():
 global ft,st,mt,dpt,rt
 ft=max(0,ft-1);st=max(0,st-1);mt=max(0,mt-1);dpt=max(0,dpt-1);rt=max(0,rt-1);pw["timer"]-=1
 if pw["timer"]<=0:
  pw["active"]=not pw["active"]
  if pw["active"]:pw["type"]=random.choice(["MAGNET","MUSHROOM","FREEZE","SHIELD","REPULSE"]);pw["x"]=random.randint(60,W-60);pw["y"]=random.randint(HH+30,GH-60);pw["timer"]=pw["duration"]
  else:pw["timer"]=random.randint(200,380)
def draw_pw(s,t):
 if not pw["active"]:return
 x,y=int(pw["x"]),int(pw["y"]);p=int(abs(math.sin(t*5))*4);z=pw["type"];c={"REPULSE":(200,50,255),"MAGNET":(255,70,70),"MUSHROOM":(255,215,0),"FREEZE":(0,220,255),"SHIELD":(255,215,0)}[z]
 pygame.draw.circle(s,c,(x,y),15+p,2);pygame.draw.circle(s,tuple(v//3 for v in c),(x,y),13)
 if z=="REPULSE":pygame.draw.line(s,(255,255,255),(x-5,y),(x+5,y),2);pygame.draw.line(s,(255,255,255),(x,y-5),(x,y+5),2)
 elif z=="FREEZE":pygame.draw.line(s,(255,255,255),(x-7,y),(x+7,y),2);pygame.draw.line(s,(255,255,255),(x,y-7),(x,y+7),2)
 elif z=="SHIELD":pygame.draw.circle(s,(255,255,255),(x,y),7,2)
 elif z=="MUSHROOM":pygame.draw.circle(s,(255,255,255),(x-4,y-6),2);pygame.draw.circle(s,(255,255,255),(x+4,y-6),2);pygame.draw.rect(s,(255,250,220),(x-4,y-4,8,10))
 else:pygame.draw.arc(s,(255,40,40),(x-10,y-10,20,20),0,math.pi,4)
AC=[(d,l,g) for d,l,g in [((140,15,30),(255,40,60),(255,130,150)),((10,120,40),(0,255,110),(130,255,170)),((0,100,150),(0,235,255),(170,245,255)),((140,100,0),(255,220,0),(255,250,130)),((160,40,0),(255,110,0),(255,185,80)),((90,15,140),(210,50,255),(235,150,255)),((140,10,90),(255,45,190),(255,150,225)),((15,115,105),(40,255,220),(160,255,240))]]
apos=[int(W*.5),int(GH*.38)];acidx=0;actmr=120
def upd_apple(hx,hy):
 global acidx,actmr
 actmr-=1
 if actmr<=0:acidx=(acidx+1)%len(AC);actmr=random.randint(90,160)
 if mt>0:
  dx,dy=hx-apos[0],hy-apos[1];d=math.hypot(dx,dy)
  if 5<d<170:apos[0]+=dx/d*4.5;apos[1]+=dy/d*4.5
def rsp_apple():
 global apos,acidx
 apos=[random.randint(45,W-45),random.randint(HH+25,GH-45)];acidx=random.randrange(len(AC))
def draw_apple(s,pos,r=16):
 x,y=map(int,pos);d,l,g=AC[acidx];pygame.draw.circle(s,g,(x,y),r+4,1);pygame.draw.circle(s,d,(x,y),r);pygame.draw.circle(s,l,(x-3,y-3),int(r*.75));pygame.draw.circle(s,(255,255,255),(x-5,y-5),max(2,int(r*.3)));pygame.draw.line(s,(80,45,20),(x,y-r+2),(x+3,y-r-6),2)
walls=[pygame.Rect(int(W*.25),int(GH*.38),int(W*.15),14),pygame.Rect(int(W*.65),int(GH*.26),14,int(GH*.18)),pygame.Rect(int(W*.44),int(GH*.82),int(W*.16),14)]
wstates=[{"timer":random.randint(100,200),"visible":False,"duration":350} for _ in walls]
def upd_walls():
 for q in wstates:
  q["timer"]-=1
  if q["timer"]<=0:q["visible"]=not q["visible"];q["timer"]=q["duration"] if q["visible"] else random.randint(180,360)
def draw_wall(s,r):pygame.draw.rect(s,(120,115,110),r,border_radius=4);pygame.draw.rect(s,(255,60,50),r,2,border_radius=4)
chaser={"x":30.,"y":float(HH+30),"speed":1.6,"visible":False,"timer":200,"duration":360}
def upd_chaser(hx,hy):
 q=chaser;q["timer"]-=1
 if q["timer"]<=0:
  q["visible"]=not q["visible"]
  if q["visible"]:play(alert);q["timer"]=q["duration"];q["x"],q["y"]=random.choice([(35.,HH+25),(W-35.,HH+25),(35.,GH-35.),(W-35.,GH-35.)])
  else:q["timer"]=random.randint(250,450)
 if q["visible"]:
  v=q["speed"]*(.45 if ft>0 else 1);dx,dy=hx-q["x"],hy-q["y"];d=math.hypot(dx,dy)
  if d>2:q["x"]+=dx/d*v;q["y"]+=dy/d*v
  return d<24
 return False
RCP=[((130,20,160),(230,40,255),(255,120,255)),((180,20,30),(255,70,70),(255,150,150)),((20,120,160),(40,230,255),(140,255,255)),((160,90,0),(255,170,0),(255,230,100)),((20,140,60),(50,255,120),(160,255,180))]
class Rival:
 def __init__(self):self.reset()
 def reset(self):
  x=random.choice((40.,W-40.));self.pts=[[x,random.uniform(HH+35,GH-70)+i*8] for i in range(16)];self.ang=random.random()*math.tau;self.speed=2.4;self.score=0;self.cd,self.cl,self.cg=random.choice(RCP);self.alive=True;self.rtmr=0
 def die(self):self.alive=False;self.rtmr=random.randint(200,380)
 def update(self,head):
  global qbtxt,qbtmr
  if not self.alive:
   self.rtmr-=1
   if self.rtmr<=0:self.reset();qbtxt="A NEW RIVAL HAS ENTERED!";qbtmr=90;play(alert)
   return
  hx,hy=self.pts[0]
  if rt>0 and math.hypot(hx-head[0],hy-head[1])<185:
   a=math.atan2(hy-head[1],hx-head[0]);f=max(5,(185-math.hypot(hx-head[0],hy-head[1]))*.12);self.ang=a;self.pts.insert(0,[max(20,min(W-20,hx+math.cos(a)*(self.speed+f))),max(HH+20,min(GH-20,hy+math.sin(a)*(self.speed+f)))]);self.pts.pop();emit(hx,hy,(200,80,255),2);return
  targets=[(apos[0],apos[1],"A",None)]+[(a["x"],a["y"],"P",a) for a in animals];tx,ty,typ,obj=min(targets,key=lambda q:math.hypot(hx-q[0],hy-q[1]))
  ta=math.atan2(ty-hy,tx-hx);self.ang=(self.ang+((ta-self.ang+math.pi)%math.tau-math.pi)*.16)%math.tau
  nx=max(20,min(W-20,hx+math.cos(self.ang)*self.speed));ny=max(HH+20,min(GH-20,hy+math.sin(self.ang)*self.speed));self.pts.insert(0,[nx,ny]);stole=False
  if math.hypot(nx-apos[0],ny-apos[1])<22:stole=True;rsp_apple();self.score+=1;self.speed=min(4.2,self.speed+.12);qbtxt="RIVAL STOLE THE APPLE!";qbtmr=90;play(alert)
  elif typ=="P" and obj in animals and math.hypot(nx-obj["x"],ny-obj["y"])<24:stole=True;animals.remove(obj);animals.append(mk_animal());self.score+=1;self.speed=min(4.2,self.speed+.12);qbtxt="RIVAL STOLE YOUR PREY!";qbtmr=90;play(alert)
  if not stole:self.pts.pop()
 def draw(self,s):
  if not self.alive:return
  for x,y in reversed(self.pts):pygame.draw.circle(s,self.cd,(int(x),int(y)),11);pygame.draw.circle(s,self.cl,(int(x-1),int(y-2)),8)
  x,y=map(int,self.pts[0]);pygame.draw.circle(s,self.cg,(x,y),15,2);pygame.draw.circle(s,self.cd,(x,y),13);pygame.draw.circle(s,self.cl,(x-2,y-2),9)
  for a in (self.ang+.7,self.ang-.7):pygame.draw.circle(s,(255,30,30),(x+int(math.cos(a)*11),y+int(math.sin(a)*11)),4)
rival=Rival()
class Snake:
 def __init__(self):self.reset()
 def reset(self):
  self.pts=[[W//2,int(GH*.32)+i*9] for i in range(24)];self.ang=self.tang=-math.pi/2;self.score=0;self.lvl=1;self.nls=1000;self.step=1000;self.alive=True;self.boost=self.hits=0;self.ml=[5,3,2,1][sdiff];self.iv=0;self.wp=self.lp=0;self.cc=dict(zip(("dark","light","glow"),SKINS[scol][1:]))
  rival.reset()
 def getc(self):
  if dpt>0:
   c=int((math.sin(tm*8)+1)*127);return (c,255-c,200),(255,230,80),(255,255,180)
  return self.cc["dark"],self.cc["light"],self.cc["glow"]
 def hit(self):
  global gameover
  if self.iv or st:return False
  self.hits+=1;self.iv=60;vibrate(.12);play(hit)
  if self.hits>=self.ml:self.alive=False;play(gameover);return True
  return False
 def update(self):
  global st,ft,mt,dpt,rt,coins,qbtxt,qbtmr,lbtmr,lbx,lbtxt,lbsub
  if not self.alive or self.pause:return
  self.iv=max(0,self.iv-1);self.boost=max(0,self.boost-1);self.wp+=.28;self.lp+=.45
  self.ang=(self.ang+((self.tang-self.ang+math.pi)%math.tau-math.pi)*.38)%math.tau;v=[2.5,3.8,5,6.4][sspeed]+(self.lvl-1)*.12-self.hits*.15
  if pr.collidepoint(int(self.pts[0][0]),int(self.pts[0][1])):v*=.65
  if self.boost:v*=1.8
  v=max(1.6,v);w=math.sin(self.wp)*1.8;hx=self.pts[0][0]+math.cos(self.ang)*v-math.sin(self.ang)*w;hy=self.pts[0][1]+math.sin(self.ang)*v+math.cos(self.ang)*w;r=17+self.hits*3
  if hx<r or hx>W-r or hy<HH+r or hy>GH-r:self.hit();return
  if sobj in (0,1):
   hr=pygame.Rect(int(hx-r),int(hy-r),r*2,r*2)
   if any(q["visible"] and hr.colliderect(wall) for q,wall in zip(wstates,walls)):self.hit();return
  if sobj in (0,2) and upd_chaser(hx,hy):self.hit();return
  if rival.alive and any(math.hypot(hx-x,hy-y)<r+14 for x,y in rival.pts):
   rival.die();pts=200 if dpt else 100;self.score+=pts;coins+=25;emit(hx,hy,(255,120,255),16);play(kill);vibrate(.18);qbtxt=f"DEVOURED RIVAL! +{pts} PTS";qbtmr=110;prog_quest("KILL_RIVAL")
  if any(math.hypot(hx-x,hy-y)<r for x,y in self.pts[16:]):self.hit();return
  self.pts.insert(0,[hx,hy]);ate=False
  if math.hypot(hx-apos[0],hy-apos[1])<r+14:
   pts=20 if dpt else 10;self.score+=pts;coins+=2;d,l,g=AC[acidx];self.cc={"dark":d,"light":l,"glow":g};play(eat);vibrate(.04);emit(*apos,l,6);rsp_apple();prog_quest("EAT_APPLE");ate=True
  if sobj in (0,3):
   for a in animals[:]:
    if math.hypot(hx-a["x"],hy-a["y"])<r+a["size"]:
     self.score+=100 if dpt else 50;coins+=10;play(hunt);vibrate(.08);emit(a["x"],a["y"],(255,230,100),10);prog_quest({"RABBIT":"HUNT_RABBIT","SQUIRREL":"HUNT_SQUIRREL"}.get(a["type"],""),1);animals.remove(a);animals.append(mk_animal());ate=True;break
  if self.score>=self.nls:
   self.lvl+=1;self.step+=100;self.nls+=self.step;lbtmr=160;lbx=-W;lbtxt=f"LEVEL UP! LEVEL {self.lvl}";lbsub=f"+100 COINS & LIFE REPAIRED! (NEXT: {self.nls}P)";coins+=100;self.hits=max(0,self.hits-1);play(levelup);vibrate(.25)
  if pw["active"] and math.hypot(hx-pw["x"],hy-pw["y"])<r+15:
   z=pw["type"];vals={"REPULSE":("rt",320),"MAGNET":("mt",300),"MUSHROOM":("dpt",250),"FREEZE":("ft",200),"SHIELD":("st",200)}
   globals()[vals[z][0]]=vals[z][1];play(repulse if z=="REPULSE" else bonus);pw["active"]=False;pw["timer"]=random.randint(220,400)
  if not ate:self.pts.pop()
 def draw(self,s):
  d,l,g=self.getc();R=17+self.hits*3
  for i in range(1,len(self.pts)):
   x,y=self.pts[i];a=math.atan2(self.pts[i-1][1]-y,self.pts[i-1][0]-x);w=math.sin(self.lp+i*.65)*6
   for sg in (1,-1):
    q=a+sg*math.pi/2.2;k=(x+math.cos(q)*(R+12)*.6,y+math.sin(q)*(R+12)*.6);t=(x+math.cos(q)*(R+12)+math.cos(a)*sg*w,y+math.sin(q)*(R+12)+math.sin(a)*sg*w);pygame.draw.line(s,d,(int(x),int(y)),tuple(map(int,k)),4);pygame.draw.line(s,l,tuple(map(int,k)),tuple(map(int,t)),3)
  for i,(x,y) in enumerate(reversed(self.pts[1:]),1):
   rr=max(5,int(R*(.35+.65*math.sin((1-i/len(self.pts))*math.pi/2))));pygame.draw.circle(s,d,(int(x),int(y)),rr);pygame.draw.circle(s,l,(int(x-2),int(y-3)),max(3,int(rr*.72)));pygame.draw.circle(s,(255,255,255),(int(x-3),int(y-4)),max(1,int(rr*.28)))
  hx,hy=self.pts[0];L=R*1.5;Q=R*1.3;tip=(hx+math.cos(self.ang)*L,hy+math.sin(self.ang)*L);left=(hx+math.cos(self.ang+2.3)*Q,hy+math.sin(self.ang+2.3)*Q);right=(hx+math.cos(self.ang-2.3)*Q,hy+math.sin(self.ang-2.3)*Q)
  if rt:pygame.draw.circle(s,(210,80,255),(int(hx),int(hy)),int(55+math.sin(tm*12)*8),3)
  if st:pygame.draw.circle(s,(255,215,0),(int(hx),int(hy)),int(L+8),4)
  if mt:pygame.draw.circle(s,(255,80,80),(int(hx),int(hy)),int(L+12),2)
  pygame.draw.polygon(s,d,[tip,left,(hx,hy),right]);pygame.draw.polygon(s,l,[tip,(left[0]*.85+hx*.15,left[1]*.85+hy*.15),(right[0]*.85+hx*.15,right[1]*.85+hy*.15)])
  for sg in (.4,-.4):
   q=(tip[0]+math.cos(self.ang+sg)*26,tip[1]+math.sin(self.ang+sg)*26);pygame.draw.line(s,l,tip,q,3);pygame.draw.circle(s,(255,255,255),tuple(map(int,q)),3)
  for sg in (.9,-.9):
   q=(tip[0]+math.cos(self.ang+sg)*12,tip[1]+math.sin(self.ang+sg)*12);pygame.draw.line(s,(255,40,50),tip,q,3)
  for sg in (1,-1):
   ex=int(hx+math.cos(self.ang)*L*.42+math.cos(self.ang+sg*math.pi/2)*Q*.62);ey=int(hy+math.sin(self.ang)*L*.42+math.sin(self.ang+sg*math.pi/2)*Q*.62);pygame.draw.circle(s,(255,230,20),(ex,ey),5);pygame.draw.circle(s,(10,10,10),(ex,ey),3)
snake=Snake();snake.pause=False
CR=56;SR=42;cy1=GH+int(PH*.13);cy2=GH+int(PH*.28);cmenu=(int(W*.18),cy1);cmode=(int(W*.50),cy1);cskin=(int(W*.82),cy1);cspeed=(int(W*.24),cy2);cmusic=(int(W*.76),cy2);cnitro=(W-64,GH+int(PH*.54));cpause=(64,GH+int(PH*.54));dcx=W//2;dcy=GH+int(PH*.54);DOR=int(W*.31);DSR=int(DOR*.34);scx=float(dcx);scy=float(dcy);drag=False;bpr=pygame.Rect(W-110,16,94,52);touch_start=None
def draw_dpad(s):
 pygame.draw.circle(s,(14,20,30),(dcx,dcy),DOR);pygame.draw.circle(s,(0,190,240),(dcx,dcy),DOR,4);pygame.draw.circle(s,(22,55,85),(dcx,dcy),int(DOR*.72),2)
 if drag:pygame.draw.line(s,(0,255,240),(dcx,dcy),(int(scx),int(scy)),3)
 pygame.draw.circle(s,(12,18,28),(int(scx),int(scy)),DSR+2);pygame.draw.circle(s,(0,240,255),(int(scx),int(scy)),DSR,3);pygame.draw.circle(s,(25,65,100),(int(scx),int(scy)),DSR-4)
tm=0.;running=True;lbtmr=0;lbx=-W;lbtxt=lbsub="";qbtmr=0;qbtxt="";abtmr=0;abtxt="";bsurf=pygame.Surface((min(int(W*.88),530),50),pygame.SRCALPHA)
while running:
 clock.tick(60);tm+=.05
 if not drag:scx+=(dcx-scx)*.35;scy+=(dcy-scy)*.35
 if not in_menu and sctrl==2 and accel:
  try:
   a=accel.acceleration
   if a and a[0] is not None and a[1] is not None and (abs(a[0])>1.2 or abs(a[1])>1.2):snake.tang=math.atan2(-a[1],a[0])
  except:pass
 for e in pygame.event.get():
  if e.type==pygame.QUIT:running=False
  elif e.type==pygame.KEYDOWN:
   if e.key==pygame.K_UP:snake.tang=-math.pi/2
   elif e.key==pygame.K_DOWN:snake.tang=math.pi/2
   elif e.key==pygame.K_LEFT:snake.tang=math.pi
   elif e.key==pygame.K_RIGHT:snake.tang=0
   elif e.key==pygame.K_SPACE:
    if in_menu:in_menu=False;snake.reset()
    else:snake.pause=not snake.pause
  elif e.type==pygame.MOUSEBUTTONDOWN:
   touch_start=e.pos;x,y=e.pos
   if in_menu:
    mw=min(530,W-140);mx0=W//2-mw//2;my0=95;gap=10;mh=max(50,int((H-my0-160-6*gap)/7)-14);rs=[pygame.Rect(mx0,my0+(mh+gap)*i,mw,mh) for i in range(7)]
    if rs[0].collidepoint(x,y):in_menu=False;snake.reset()
    elif rs[1].collidepoint(x,y):scol=(scol+1)%16;snake.reset()
    elif rs[2].collidepoint(x,y):sspeed=(sspeed+1)%4
    elif rs[3].collidepoint(x,y):sctrl=(sctrl+1)%3
    elif rs[4].collidepoint(x,y):sobj=(sobj+1)%5
    elif rs[5].collidepoint(x,y):chg_trk()
    elif rs[6].collidepoint(x,y):sdiff=(sdiff+1)%4;snake.ml=[5,3,2,1][sdiff]
   else:
    if bpr.collidepoint(x,y):snake.pause=not snake.pause;continue
    if math.hypot(x-cmenu[0],y-cmenu[1])<=CR+8:in_menu=True;continue
    if not snake.alive:snake.reset()
    elif math.hypot(x-cpause[0],y-cpause[1])<=SR+6:snake.pause=not snake.pause
    elif math.hypot(x-cnitro[0],y-cnitro[1])<=SR+6:snake.boost=50;prog_quest("USE_BOOST");play(alert)
    elif math.hypot(x-cmode[0],y-cmode[1])<=CR+8:sctrl=(sctrl+1)%3
    elif math.hypot(x-cskin[0],y-cskin[1])<=CR+8:scol=(scol+1)%16;snake.reset()
    elif math.hypot(x-cspeed[0],y-cspeed[1])<=CR+8:sspeed=(sspeed+1)%4
    elif math.hypot(x-cmusic[0],y-cmusic[1])<=CR+8:chg_trk()
    elif math.hypot(x-dcx,y-dcy)<=DSR+12:drag=True
    elif sctrl==0 and math.hypot(x-dcx,y-dcy)<=DOR+20:
     dx,dy=x-dcx,y-dcy;snake.tang=0 if abs(dx)>abs(dy) and dx>0 else math.pi if abs(dx)>abs(dy) else math.pi/2 if dy>0 else -math.pi/2
  elif e.type==pygame.MOUSEMOTION and drag:
   x,y=e.pos;dx,dy=x-dcx,y-dcy;d=math.hypot(dx,dy);m=DOR-DSR
   if d>m:scx,scy=dcx+dx/d*m,dcy+dy/d*m
   else:scx,scy=x,y
   if d>8:snake.tang=math.atan2(dy,dx)
  elif e.type==pygame.MOUSEBUTTONUP:
   drag=False
   if not in_menu and sctrl==1 and touch_start:
    dx,dy=e.pos[0]-touch_start[0],e.pos[1]-touch_start[1]
    if math.hypot(dx,dy)>25:snake.tang=0 if abs(dx)>abs(dy) and dx>0 else math.pi if abs(dx)>abs(dy) else math.pi/2 if dy>0 else -math.pi/2
   touch_start=None
 screen.fill((8,12,18))
 if in_menu:
  screen.blit(msurf,(0,0));c=int(235+math.sin(tm*4)*20);title=f46.render("REAL CENTIPEDE",True,(0,min(255,c),160));screen.blit(title,(W//2-title.get_width()//2,28))
  mw=min(530,W-140);mx0=W//2-mw//2;my0=95;gap=10;mh=max(50,int((H-my0-160-6*gap)/7)-14)
  items=[("START GAME",(255,255,255),(0,180,80)),(SKINS[scol][0],SKINS[scol][2],(36,18,28)),(SL[sspeed],(255,230,0),(40,34,10)),(CM[sctrl],(0,230,255),(10,32,44)),(OM[sobj],(170,255,50),(24,40,12)),(f"AUDIO: {playlist[aidx][:14]}",(255,80,210),(40,14,36)),(DM[sdiff],(255,60,60),(44,12,12))]
  for i,(txt,fg,bg) in enumerate(items):
   r=pygame.Rect(mx0,my0+(mh+gap)*i,mw,mh);pygame.draw.rect(screen,bg,r,border_radius=14);pygame.draw.rect(screen,fg,r,2,border_radius=14);z=f46 if i==0 else f32;t=z.render(txt,True,fg);screen.blit(t,(r.centerx-t.get_width()//2,r.centery-t.get_height()//2))
 else:
  if sobj in (0,1):upd_walls()
  if sobj in (0,3):upd_anim(*snake.pts[0])
  upd_trees(snake.lvl);upd_pw();upd_apple(*snake.pts[0]);snake.update();rival.update(snake.pts[0])
  screen.blit(wsurf,(0,0));draw_pond(screen,tm)
  for x,y,r in ttrees:draw_tree(screen,x,y,r)
  if sobj in (0,1):
   for i,r in enumerate(walls):
    if wstates[i]["visible"]:draw_wall(screen,r)
  if sobj in (0,3):
   for a in animals:draw_animal(screen,a)
  if sobj in (0,2) and chaser["visible"]:
   x,y=int(chaser["x"]),int(chaser["y"]);pygame.draw.circle(screen,(255,30,30),(x,y),14);pygame.draw.circle(screen,(255,255,255),(x,y),4)
  draw_pw(screen,tm);draw_apple(screen,apos);rival.draw(screen);snake.draw(screen);upd_parts(screen)
  if lbtmr>0:
   lbtmr-=1;lbx+=((W//2-bsurf.get_width()//2 if 'bsurf' in globals() else W//2-250) if lbtmr>30 else W+50-lbx)*.16
  pygame.draw.rect(screen,(12,16,24),(0,0,W,HH));pygame.draw.line(screen,(0,255,170),(0,HH),(W,HH),4)
  t=f28.render("FOULOLOU MILOUD",True,(0,255,190));screen.blit(t,(16,HH//2-t.get_height()//2))
  t=f24.render(f"[LVL {snake.lvl} -> {snake.nls}P] COINS: {coins}",True,(255,230,80));screen.blit(t,(W//2-t.get_width()//2,HH//2-t.get_height()//2))
  t=f24.render(f"SC:{snake.score} LIVES: {max(0,snake.ml-snake.hits)}",True,(255,255,255));screen.blit(t,(bpr.left-t.get_width()-18,HH//2-t.get_height()//2))
  pygame.draw.rect(screen,(25,35,50),bpr,border_radius=10);pygame.draw.rect(screen,(0,210,255),bpr,2,border_radius=10);t=f24.render("PLAY" if snake.pause else "PAUSE",True,(0,210,255));screen.blit(t,(bpr.centerx-t.get_width()//2,bpr.centery-t.get_height()//2))
  screen.blit(psurf,(0,GH));pygame.draw.line(screen,(0,210,255),(0,GH),(W,GH),3)
  for p,l,c in [(cmenu,"MENU",(255,215,0)),(cmode,CS[sctrl],(0,230,255)),(cskin,"SKIN",SKINS[scol][2]),(cspeed,"SPEED",(255,230,0)),(cmusic,"MUSIC",(255,80,220))]:
   pygame.draw.circle(screen,(16,24,38),p,CR);pygame.draw.circle(screen,c,p,CR,3);z=f27.render(l,True,c);screen.blit(z,(p[0]-z.get_width()//2,p[1]-z.get_height()//2))
  for p,l,c in [(cpause,"PLAY" if snake.pause else "PAUSE",(180,255,200) if snake.pause else (140,240,255)),(cnitro,"BOOST",(255,160,40))]:
   pygame.draw.circle(screen,(18,26,40),p,SR);pygame.draw.circle(screen,c,p,SR,3);z=f24.render(l,True,c);screen.blit(z,(p[0]-z.get_width()//2,p[1]-z.get_height()//2))
  if sctrl==0:draw_dpad(screen)
  else:
   z=f46.render("SWIPE SCREEN TO STEER" if sctrl==1 else "TILT PHONE TO STEER",True,(0,230,255) if sctrl==1 else (255,215,0));screen.blit(z,(dcx-z.get_width()//2,dcy-25))
  if qbtmr>0:qbtmr-=1;z=f24.render(qbtxt,True,(255,80,80) if "STOLE" in qbtxt else (0,255,140));screen.blit(z,(W//2-z.get_width()//2,GH+10))
  elif abtmr>0:abtmr-=1;z=f24.render(abtxt,True,(255,235,60));screen.blit(z,(W//2-z.get_width()//2,GH+10))
  if snake.pause:
   z=f64.render("PAUSED",True,(0,220,255));screen.blit(z,(W//2-z.get_width()//2,GH//2-30))
  if not snake.alive:
   hisc=max(hisc,snake.score);save_data(hisc,coins);z=f64.render("GAME OVER",True,(255,40,40));screen.blit(z,(W//2-z.get_width()//2,GH//2-25));z=f24.render("TAP ANYWHERE TO RETRY",True,(255,255,255));screen.blit(z,(W//2-z.get_width()//2,GH//2+40))
 pygame.display.flip()
pygame.quit();sys.exit()
