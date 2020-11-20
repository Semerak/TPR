
# coding: utf-8

# In[ ]:


import itertools
from fractions import Fraction

#==========================================  I  ======================================================

def strategies(table_raw):
    table= Table(table_raw)

    print(table)

    for m in methods:
        print(f"{m.__name__}: \t{m(table)}")

class Cell:
    def __init__(self,i,j,a,b):
        self.i=i
        self.j=j
        self.a=a
        self.b=b
    def index(self):
        return f"(a{self.i}, b{self.j})"
    def __repr__(self):
        return self.index()+ " ["+str(self.a)+" "+str(self.b)+"]"
    def __str__(self):
        return self.index()
    
class Table:
    def __init__(self,t):
        self.Table=[]
        raw_id=0
        for raw in t:
            raw_id+=1
            Raw=Set()
            col_id=0
            for cell in raw:
                col_id+=1
                Raw.append(Cell(raw_id,col_id,cell[0],cell[1]))
            self.Table.append(Raw)
            
    def __str__(self):
        res="\t"+"\t".join([f"b{i+1}" for i in range(len(self.Table[0]))])+"\n"
        res+="\n".join([f"a{raw[0].i}\t" + "\t".join([f"{cell.a}, {cell.b}" for cell in raw]) for raw in self.Table])
        return res+"\n"
        
    def get(self,i,j):
        return self.Table[i-1][j-1]
    
    def raw(self,i):
        return self.Table[i-1]
    
    def col(self,j):
        c=Set()
        c.extend([raw[j-1] for raw in self.Table])
        return c
        
    def Tran(self):
        t=[]
        for j in range(len(self.Table[0])):
            t.append(self.col(j+1))
        return t
    def getSet(self):
        res=Set()
        for raw in self.Table:
            res.extend(raw)
        return res
    
    def getLists(self):
        return [[[cell.a,cell.b] for cell in raw] for raw in self.Table]
    
class Set:
    def __init__(self):
        self.set=[]
        
    def __iter__(self):
        self.iterator=-1
        return self
    
    def __next__(self):
        self.iterator+=1
        if self.iterator>=len(self.set):
            raise StopIteration
        return self.set[self.iterator]
        
    def __getitem__(self,i):
        return self.set[i]
    
    def __repr__(self):
        return str(self.set)
    
    def __str__(self):
        if len(self.set)==0:
            return "Ø"
        res="{"
        
        #for cell in self.set:
        #    res+=cell.index()+" "
        
        res+=", ".join([cell.index() for cell in self.set])
        res+="}"
        return res
    def __len__(self):
        return len(self.set)
    
    def append(self,cell):
        self.set.append(cell)
    
    def extend(self,cells):
        self.set.extend(cells)
    
    def pop(self,i):
        return self.set.pop(i)
        
    def a(self):
        return [c.a for c in self.set]
    
    def b(self):
        return [c.b for c in self.set]
    
    def contains(self,cell):
        for c in self.set:
            if c.i==cell.i and c.j==cell.j and c.a==cell.a and c.b==cell.b :
                return True
        return False 
    
def intersection(A: Set,B: Set):
    res=Set()
    for a in A:
        if B.contains(a):
            res.append(a)
    return res

def complement(A: Set,B: Set):
    res=Set()
    for a in A:
        if not( a in B):
            res.append(a)
    return res

def equalCell(c1: Cell,c2:Cell):
    if c1.a==c2.a and c1.b == c2.b:
        return True
    return False

def betterCell(c1: Cell,c2:Cell):
    if (c1.a>=c2.a and c1.b>c2.b) or (c1.a>c2.a and c1.b>=c2.b):
        return True
    return False

def worseCell(c1: Cell,c2:Cell):
    if (c1.a<=c2.a and c1.b<c2.b) or (c1.a<c2.a and c1.b<=c2.b):
        return True
    return False

def uncomparebleCell(c1: Cell,c2:Cell):
    if (c1.a<c2.a and c1.b>c2.b) or (c1.a>c2.a and c1.b<c2.b):
        return True
    return False

def compareCell(c1: Cell,c2:Cell):
    res=""
    if equalCell(c1,c2): res+="equal"
    if betterCell(c1,c2): res+="better"
    if worseCell(c1,c2): res+="worse"
    if uncomparebleCell(c1,c2): res+="uncomp"
    return res

def dominSet(s1: Set,s2: Set,par):
    if len(s1)!=len(s2):
        return False
    strait=False
    if par=="a":
        for i in range(len(s1)):
            if s1[i].a>s2[i].a:
                strait=True
            elif s1[i].a<s2[i].a:
                return False
        if strait:
            return True
    if par=="b":
        for i in range(len(s1)):
            if s1[i].b>s2[i].b:
                strait=True
            elif s1[i].b<s2[i].b:
                return False
        if strait:
            return True
    return False
        
def equalSet(s1:Set, s2:Set,par):
    if par=="a":
        return s1.a()==s2.a()
    if par=="b":
        return s1.b()==s2.b()
    
def clearCols(t):
    t_copy=Table([])
    t_copy.Table=t.Tran()
    i=0
    while i <len(t_copy.Table):
        j=0
        while j<len(t_copy.Table):
            if i!=j:
                if dominSet(t_copy.raw(i+1),t_copy.raw(j+1),"b"):
                    t_copy.Table.pop(j)
                    if i>j:
                        i=-1
                else:
                    j+=1
            else:
                j+=1
        i+=1
    t_copy.Table=t_copy.Tran()
    return t_copy

def clearRaws(t):
    t_copy=Table([])
    t_copy.Table=t.Table
    i=0
    while i <len(t_copy.Table):
        j=0
        while j<len(t_copy.Table):
            if i!=j:
                if dominSet(t_copy.raw(i+1),t_copy.raw(j+1),"a"):
                    t_copy.Table.pop(j)
                    if i>j:
                        i=-1
                else:
                    j+=1
            else:
                j+=1
        i+=1
    return t_copy

                

def D1(table):
    res=Set()
    for raw1 in table.Table:
        domin=True
        for raw2 in table.Table:
            if raw1 != raw2:
                if not(dominSet(raw1,raw2,"a"))and not(equalSet(raw1,raw2,"a")):
                    domin=False
        if domin:
            res.extend(raw1)
    return res

def D2(table):
    res=Set()
    for col1 in table.Tran():
        domin=True
        for col2 in table.Tran():
            if col1 != col2:
                if not(dominSet(col1,col2,"b"))and not(equalSet(col1,col2,"b")):
                    domin=False
        if domin:
            res.extend(col1)
    return res            

def D(table):
    return intersection(D1(table),D2(table))

def ND1(table):
    t0=Table(table.getLists())
    t=clearRaws(t0)
    return t.getSet()

def ND2(table):
    t0=Table(table.getLists())
    t=clearCols(t0)
    return t.getSet()

def ND(table):
    s1=ND1(table)
    s2=ND2(table)
    return intersection(ND1(table),ND2(table))

def O1(table):
    maxval=max([ min(raw.a()) for raw in table.Table])
    res=Set()
    for raw in table.Table:
        if maxval == min(raw.a()):
            res.extend(raw)
    return res

def O2(table):
    maxval=max([ min(col.b()) for col in table.Tran()])
    res=Set()
    for col in table.Tran():
        if maxval == min(col.b()):
            res.extend(col)
    return res

def O(table):
    return intersection(O1(table),O2(table))

def IR(table):
    alpha1=max([ min(raw.a()) for raw in table.Table])
    alpha2=max([ min(col.b()) for col in table.Tran()])
    res=Set()
    for raw in table.Table:
        for cell in raw:
            if cell.a>=alpha1 and cell.b >=alpha2:
                res.append(cell)
    return res

def PO(table):
    cur_set=table.getSet()
    i=-1
    while i<len(cur_set)-1:
        i+=1
        j=0
        if i!=j:
            while j<len(cur_set):
                if betterCell(cur_set[i],cur_set[j]):  # якщо можлива рівність, то тут потрібно додати умову equalCell(cur_set[i],cur_set[j])
                    cur_set.pop(j)
                    if i>j:
                        i-=1
                else:
                    j+=1
    return cur_set

def П(table):
    return intersection(IR(table),PO(table))

def SPO(table):
    return intersection(PO(table),O(table))

def OP1(table):
    return intersection(PO(table),O1(table))

def OP2(table):
    return intersection(PO(table),O2(table))

def OPi(table):
    print(f"OP1: {OP1(table)}")
    print(f"OP2: {OP2(table)}")
    
def NE(table):
    res=Set()
    for cell in table.getSet():
        if cell.a==max(table.col(cell.j).a()) and cell.b == max(table.raw(cell.i).b()):
            res.append(cell)
    return res

def SNE(table):
    return intersection(NE(table),PO(table))

def SE(table):        
    t=Table(table.getLists())
    size=[0,0]
    
    while size != [len(t.Table),len(t.Tran())]:
        size=[len(t.Table),len(t.Tran())]
        t=clearRaws(t)
        t=clearCols(t)

    for raw1 in t.Table:
        for raw2 in t.Table:
            if raw1!=raw2:
                if not(dominSet(raw1,raw2,"a")) and not(dominSet(raw2,raw1,"a")) and not(equalSet(raw1,raw2,"a")):
                    return Set()
                
    
    for col1 in t.Tran():
        for col2 in t.Tran():
            if col1!=col2:
                if not(dominSet(col1,col2,"b")) and not(dominSet(col2,col1,"b")) and not(equalSet(col1,col2,"b")):
                    return Set()
    
    return t.getSet()
            
def ShE1(table):
    tab_res=[]
    for raw in table.Table:
        raw_res=Set()
        maxval=max(raw.b())
        for cell in raw:
            if cell.b==maxval:
                raw_res.append(cell)
        tab_res.append(raw_res)
    table2=Table([])
    table2.Table=tab_res
    cell_set=table2.getSet()
    maxval=max(cell_set.a())
    good_cells_rows=[]
    res=Set()
    for cell in cell_set:
        if cell.a==maxval:
            good_cells_rows.append(cell.i)
    for cell in cell_set:
        if cell.i in good_cells_rows:
            res.append(cell)
    return res

def ShE2(table):
    tab_res=[]
    for col in table.Tran():
        col_res=Set()
        maxval=max(col.a())
        for cell in col:
            if cell.a==maxval:
                col_res.append(cell)
        tab_res.append(col_res)
    table2=Table([])
    table2.Table=tab_res
    cell_set=table2.getSet()
    maxval=max(cell_set.b())
    good_cells_cols=[]
    res=Set()
    
    #v1
    #for cell in cell_set:
    #    if cell.b==maxval:
    #        good_cells_cols.append(cell.j)
    #for cell in cell_set:
    #    if cell.j in good_cells_cols:
    #        res.append(cell)
    
    #v2
    for cell in cell_set:
        if cell.b==maxval:
            res.append(cell)
    
    return res

methods=[D1,D2,D,ND1,ND2,ND,O1,O2,O,IR,PO,П,SPO,OP1,OP2,NE,SNE,SE,ShE1,ShE2]



#==========================================  II  ======================================================

def _distribution(queue,B,C):
    res=[0 for i in queue]
    for q in queue:
        if B[q-1]<C:
            res[q-1]=B[q-1]
            C-=B[q-1]
        else:
            res[q-1]=C
            C=0
    return res

def distribution(K,B,C):
    print("K = ",K)
    print("B = ",B)
    print("C = ",C)
    print()
    
    queue=range(1,K+1)
    print("\t\t\t   1  2  3")
    n=0
    sums=[Fraction(0,1) for i in range(K)]
    for q in itertools.permutations(queue):
        n+=1
        dis=_distribution(q,B,C)
        for i in range(K):
            sums[i]+=dis[i]
        print(q,"\t|\t (",",  ".join(map(str,dis)),")")

    end_sums=[s/n for s in sums]
    print("\t\t\t"," +".join(map(str,end_sums))," = ", sum(end_sums))
    print()
    print("Вектор Шеплі: (", ", ".join(map(str,end_sums)),")")
    
#==========================================  III  ======================================================

def sort_B(B):
    B_dic=[dict(index=i,val=B[i]) for i in range(len(B))]

    B_dic_sorted=sorted(B_dic,key= lambda b: b["val"])

    B_=[Fraction(b["val"],1) for b in B_dic_sorted]
    B_order=[b["index"] for b in B_dic_sorted]
    return B_, B_order

def order_X(X,order):
    dic=[dict(index=order[i],val=X[i]) for i in range(len(X))]
    dic_sorted=sorted(dic,key= lambda x: x["index"])
    return [d["val"] for d in dic_sorted]

def print_problem(B,C):
    print("B = (",", ".join(map(str,B)),")")
    print("C = ",C)
    print()


def podushnyi_podatok(B,C):
    print_problem(B,C)
    B_,B_order=sort_B(B)
    lenB=len(B_)
    cur_C=C
    X=[]
    def calc_xi(lamb,bi):
        return min(lamb,bi)
    for i_ in range(len(B_)):
        i=i_+1
        print(f"{i})")
        if i==1:
            print(f"\tλ ≤ b{index(1)}")
        elif i==lenB:
            print(f"\tb{index(i)} < λ")
        else:
            print(f"\tb{index(i-1)} < λ ≤ b{index(i)}")

        print(f"\t{lenB-i+1}*λ = {cur_C}")
        lamb=cur_C/(lenB-i+1)
        print(f"\tλ = {lamb}")

        xi=calc_xi(lamb,B_[i_])
        print(f"\tx{index(i)} = {xi}")

        cur_C-=xi
        X.append(xi)
    X_str=", ".join(map(str,X))
    print(f"X = ({X_str}) - податки")
    X_=order_X(X,B_order)
    X__str=", ".join(map(str,X_))
    print(f"X* = ({X__str}) - впорядковані податки")
    R=[B[i]-X_[i] for i in range(len(B))]
    R_str=", ".join(map(str,R))
    print(f"({R_str}) - залишок")

def rivnevyi_podatok(B,C):
    print_problem(B,C)
    B_,B_order=sort_B(B)
    lenB=len(B_)
    cur_C=sum(B_)-C
    X=[]
    def calc_xi(lamb,bi):
        return bi-min(lamb,bi)
    for i_ in range(len(B_)):
        i=i_+1
        print(f"{i})")
        if i==1:
            print("\tλ ≤ b₁")
        elif i==lenB:
            print(f"\tb{index(i)} < λ")
        else:
            print(f"\tb{index(i-1)} < λ ≤ b{index(i)}")

        print(f"\t{lenB-i+1}*λ = {cur_C}")
        lamb=cur_C/(lenB-i+1)
        print(f"\tλ = {lamb}")

        xi=calc_xi(lamb,B_[i_])
        print(f"\tx{index(i)} = {xi}")

        cur_C-=B_[i_]-xi
        X.append(xi)
    X_str=", ".join(map(str,X))
    print(f"X = ({X_str}) - податки")
    X_=order_X(X,B_order)
    X__str=", ".join(map(str,X_))
    print(f"X* = ({X__str}) - впорядковані податки")
    R=[B[i]-X_[i] for i in range(len(B))]
    R_str=", ".join(map(str,R))
    print(f"({R_str}) - залишок")

def N_rivnevyi_podatok(B,C):
    B_,B_order=sort_B(B)
    lenB=len(B_)
    cur_C=sum(B_)-C
    X=[]
    def calc_xi(lamb,bi):
        return bi-min(lamb,bi/2)
    for i_ in range(len(B_)):
        i=i_+1
        print(f"{i})")
        if i==1:
            print("\tλ ≤ b₁")
        elif i==lenB:
            print(f"\tb{index(i)} < λ")
        else:
            print(f"\tb{index(i-1)} < λ ≤ b{index(i)}")

        print(f"\t{lenB-i+1}*λ = {cur_C}")
        lamb=cur_C/(lenB-i+1)
        print(f"\tλ = {lamb}")

        xi=calc_xi(lamb,B_[i_])
        print(f"\tx{index(i)} = {xi}")

        cur_C-=B_[i_]-xi
        X.append(xi)
    X_str=", ".join(map(str,X))
    print(f"X = ({X_str}) - податки")
    X_=order_X(X,B_order)
    X__str=", ".join(map(str,X_))
    print(f"X* = ({X__str}) - впорядковані податки")
    R=[B[i]-X_[i] for i in range(len(B))]
    R_str=", ".join(map(str,R))
    print(f"({R_str}) - залишок")

def N_podushnyi_podatok(B,C):
    B_,B_order=sort_B(B)
    lenB=len(B_)
    cur_C=C
    X=[]
    def calc_xi(lamb,bi):
        return min(lamb,bi/2)
    for i_ in range(len(B_)):
        i=i_+1
        print(f"{i})")
        if i==1:
            print("\tλ ≤ b₁")
        elif i==lenB:
            print(f"\tb{index(i)} < λ")
        else:
            print(f"\tb{index(i-1)} < λ ≤ b{index(i)}")

        print(f"\t{lenB-i+1}*λ = {cur_C}")
        lamb=cur_C/(lenB-i+1)
        print(f"\tλ = {lamb}")

        xi=calc_xi(lamb,B_[i_])
        print(f"\tx{index(i)} = {xi}")

        cur_C-=xi
        X.append(xi)
    X_str=", ".join(map(str,X))
    print(f"X = ({X_str}) - податки")
    X_=order_X(X,B_order)
    X__str=", ".join(map(str,X_))
    print(f"X* = ({X__str}) - впорядковані податки")
    R=[B[i]-X_[i] for i in range(len(B))]
    R_str=", ".join(map(str,R))
    print(f"({R_str}) - залишок")

def N_yadro(B,C):
    print_problem(B,C)
    if C<=sum(B)/2:
        print(f"C ≤ ½ Σbi")
        print("подушний метод")
        N_podushnyi_podatok(B,C)
    else:
        print(f"C ≥ ½ Σbi")
        print("рівневий метод")
        N_rivnevyi_podatok(B,C)
        

def index(n):
    res=""
    for num in str(n):
        res+=index_simp(int(num))
    return res
def index_simp(n):
    if n==0:
        return "₀"
    elif n==1:
        return "₁"
    elif n==2:
        return "₂"
    elif n==3:
        return "₃"
    elif n==4:
        return "₄"
    elif n==5:
        return "₅"
    elif n==6:
        return "₆"
    elif n==7:
        return "₇"
    elif n==8:
        return "₈"
    elif n==9:
        return "₉"
    

