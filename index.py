import re



def evl(e):
	e=e.replace("(+","").replace(" ","").replace("-+","-").replace("+-","-")
	i=0
	while (True):
		if (e[i]=="("):
			s=""
			b=0
			sg=e[i-1] if i>=1 else "+"
			oi=int(i-1)
			while (True):
				if (e[i]=="("):b+=1
				elif (e[i]==")"):b-=1
				s+=e[i]
				if (b==0):break
				i+=1
			if (sg=="-"):s=s.replace("-","$").replace("+","-").replace("$","+")
			s=evl(sg+s[1:-1])
			ni=len(e[:oi]+s)
			e=e[:oi]+s+e[i+1:]
			i=ni+0
		i+=1
		if (i>=len(e)):break
	e=e.replace("-+","-").replace("+-","-")
	e=" -".join(" +".join(e.split("+")).split("-")).split(" ")
	d=[]
	for k in e:
		if (k==""):continue
		i=0
		sg=1
		if (k[i]=="-"):
			i+=1
			sg=-1
		elif (k[i]=="+"):
			i+=1
		num,oth=sg,""
		nt=""
		while (True):
			if (k[i].isdigit()):
				nt+=k[i]
			else:
				if (nt!=""):
					num*=int(nt)
					nt=""
				oth+=k[i]
			i+=1
			if (i>len(k)-1):break
		if (nt!=""):num*=int(nt)
		d.append([num,oth])
	o=[]
	for j in range(len(d)-1,-1,-1):
		gs=False
		if (len(o)==0):
			o.append(d[j])
			continue
		for ki in range(0,len(o)):
			k=o[ki]
			s=True
			for l in k[1]+d[j][1]:
				if (d[j][1].count(l)!=k.count(l)):
					s=False
					break
			if (s==True):
				o[ki]=[k[0]+d[j][0],k[1]]
				gs=True
				break
		if (gs==False):o.append(d[j])
	e=""
	for k in o:
		n=str(k[0])
		if (n=="0"):continue
		if (n=="-1" and k[1]!=""):n="-"
		elif (n=="1" and k[1]!=""):n="+"
		elif (n[0]!="-" and n[0].isdigit()):n="+"+n
		e+=n+k[1]
	if (e==""):e="0"
	if (e[0]=="+"):e=e[1:]
	return e
def solve(sq,diagonals=False,log_steps=False,log_sum=False):
	def calc(ts,*args):
		t=""
		for k in args:
			if (k==None):k=0
			t+="+"+str(k)
		if (ts==None):return evl(t[1:])
		t="-("+t[1:]+")"
		return evl(ts+t)
	def idx(a,e):
		i=0
		for o in a:
			if o==e:return i
			i+=1
		return -1
	def get(sq,d,s):
		s=1 if s==False else 0
		ta=[]
		for i in range(0,len(sq[0])):
			a=[]
			for j in sq:a.append(j[i])
			if (a.count(None)==s):ta.append([a,idx(a,None),i])
		for j in range(0,len(sq)):
			a=[]
			for i in sq[j]:a.append(i)
			if (a.count(None)==s):ta.append([a,j,idx(a,None)])
		if d==False:return ta
		i,j,a=0,0,[]
		while (True):
			if (j>len(sq)-1):break
			a.append(sq[j][i])
			j+=1
			i+=1
		if (a.count(None)==s):ta.append([a,idx(a,None),idx(a,None)])
		i,j,a=0,len(sq)-1,[]
		while (True):
			if (j<0):break
			a.append(sq[j][i])
			j-=1
			i+=1
		if (a.count(None)==s):ta.append([a,len(sq)-1-idx(a,None),idx(a,None)])
		return ta
	if (log_steps==True):print(log(sq))
	ts=calc(None,*get(sq,diagonals,True)[0][0])
	mv=[]
	while (True):
		a=get(sq,diagonals,False)
		s=False
		for h in a:
			if (h==None or mv.count(h[1:])>0):continue
			mv.append(h[1:])
			h[0].pop(idx(h[0],None))
			sq[h[1]][h[2]]=calc(ts,*h[0])
			if (log_steps==True):print(log(sq,i=True,h=h[1:]))
			s=True
		if (len(a)==0 or s==False):break
	if (log_sum==True):print(ts)
	return sq
def log(sq,i=False,h=[-1,-1]):
	mw=0
	if (i==False):
		s="Magic square > %sx%s\n"%(len(sq[0]),len(sq))
		s+="\n"
	else:
		s=""
	for j in sq:
		for i in j:
			mw=max(len(str(i).replace("None","-")),mw)
	mw+=2
	for j in range(0,len(sq)):
		for i in range(0,len(sq[j])):
			w=str(sq[j][i])
			if (j==h[0] and i==h[1]):w="="+w+"="
			s+=w.replace("None","-").center(mw," ")+"|"
		s=s[:-1]+"\n"+"-"*((mw+1)*len(sq[j])-1)+"\n"
	s=s[:-(mw+1)*len(sq[j])]
	return s
print(log(solve([["5p+2",0,"4p+1"],["2p",None,None],[None,None,None]],diagonals=True,log_steps=True,log_sum=True)))
print(log(solve([["n","2m",None],["2m+2n",None,None],["m",None,None]],diagonals=True,log_steps=True,log_sum=True)))
print(log(solve([["4a+b","2c",None],[None,"3a+b+c",None],[None,None,"2a+b+2c"]],diagonals=True,log_steps=True,log_sum=True)))
