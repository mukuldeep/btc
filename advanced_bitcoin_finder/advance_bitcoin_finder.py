##########################
# This is designed work fine with python 2.7.x & 3.x.x and may produce inconsistency in other version of python
# This module is developed by Mukuldeep Maiti, It is only for educational purposes. 
# 
# If you got the STAR of David without modifying any code, Contact me mukul0018@gmail.com, you might get a BRAND NEW TESLA.
#
##########################
P = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1 #prime number for modulus operations
order= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 #order for the elliptic curve y^2=x^3+7 ,used in bitcoin
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240 #x co-ordinate of generating point of secp256k1 i.e. curve used in bitcoin
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424 #y co-ordinate of generating point of secp256k1 i.e. curve used in bitcoin

# mod inverse
# Extended Euclidean Algorithm
def modinv(a,n): 
    lm, hm = 1,0
    low, high = a%n,n
    while low > 1:
        ratio = high//low
        nm = hm - lm * ratio
        new = high - low * ratio
        hm = lm
        high = low
        lm = nm
        low = new
    return lm % n

# Elliptic curve point doubling
def ECdouble(xp,yp):
  l = ( ( 3 * xp * xp )* modinv( 2 * yp, P ) ) % P
  X = ( l * l - 2 * xp ) % P
  Y = ( l * ( xp - X ) - yp ) % P
  return X,Y


# Elliptic curve point addition
def ECadd(xp,yp,xq,yq):
    #point addition will not work if both the point are same. So, point doubling is required
    if xp==xq and yp==yq:
      return  ECdouble(xp,yp)
    
    m = ((yq-yp) * modinv(xq-xp,P))%P
    xr = (m*m-xp-xq)%P
    yr = (m*(xp-xr)-yp)%P
    return (xr,yr)
  
# Elliptic curve point multiplication
##1. scaler multiplication with generator point
### slowest ECmult method 
def ECmult(scaler):
  if scaler==0:
    return 0,0
  _2pX=[0]*258
  _2pY=[0]*258
  _2pX[0],_2pY[0]=Gx,Gy
  _X=Gx
  _Y=Gy
  for i in range(1,257):
    _2pX[i],_2pY[i]=ECdouble(_2pX[i-1],_2pY[i-1])
  
  index=0
  while not(scaler & 1):
    index+=1
    scaler>>=1
  _X=_2pX[index]
  _Y=_2pY[index]
  scaler>>=1
  index+=1
  while scaler>0:
    if scaler & 1:
      _X,_Y=ECadd(_X,_Y,_2pX[index],_2pY[index])
    scaler>>=1
    index+=1
  return _X,_Y

##1. scaler multiplication with generator point
## Returns only x co-ordinate

def ECmultx(scaler):
  if scaler==0:
    return 0
  _2pX=[0]*258
  _2pY=[0]*258
  _2pX[0],_2pY[0]=Gx,Gy
  _X=Gx
  _Y=Gy
  for i in range(1,257):
    _2pX[i],_2pY[i]=ECdouble(_2pX[i-1],_2pY[i-1])
  
  index=0
  while not(scaler & 1):
    index+=1
    scaler>>=1
  _X=_2pX[index]
  _Y=_2pY[index]
  scaler>>=1
  index+=1
  while scaler>0:
    if scaler & 1:
      _X,_Y=ECadd(_X,_Y,_2pX[index],_2pY[index])
    scaler>>=1
    index+=1
  return _X

#ECmult fast scaler
def ECmultx_fast(scaler):
  if scaler==0:
    return 0,0
  if(scaler==1):
    return Gx
  scaler-=1
  _2px=Gx
  _2py=Gy
  _x=Gx
  _y=Gy
  while(scaler):
    if scaler&1:
      _x,_y=ECadd(_x,_y,_2px,_2py)
    scaler>>=1
    _2px,_2py=ECdouble(_2px,_2py)
  return _x

print("Engine(1/3): igniting EC Super Fast Engine")
pre_res=[]
def pre_calc_2p():#precalculation for all the bits 
  _2px=Gx
  _2py=Gy
  for i in range(0,256):
    pre_res.append([_2px,_2py])
    _2px,_2py=ECdouble(_2px,_2py)

pre_calc_2p()
def ECmultx_super_fast(scaler):
  if scaler==0:
    return 0,0
  if(scaler==1):
    return Gx
  scaler-=1
  ind=0
  _x=Gx
  _y=Gy
  while(scaler):
    if scaler&1:
      _x,_y=ECadd(_x,_y,pre_res[ind][0],pre_res[ind][1])
    scaler>>=1
    ind+=1
  return _x

def ECmult_super_fast(scaler):
  if scaler==0:
    return 0,0
  if(scaler==1):
    return Gx,Gy
  scaler-=1
  ind=0
  _x=Gx
  _y=Gy
  while(scaler):
    if scaler&1:
      _x,_y=ECadd(_x,_y,pre_res[ind][0],pre_res[ind][1])
    scaler>>=1
    ind+=1
  return _x,_y

##2. scaler multiplication with other point on secp256k1 curve
###Example 2*(4G)=8G 4*(5G)=20G etc.
def ECmultp(Sx,Sy,scaler):
  _2pX=[0]*258
  _2pY=[0]*258
  _2pX[0],_2pY[0]=Sx,Sy
  _X=Sx
  _Y=Sy
  for i in range(1,257):
    _2pX[i],_2pY[i]=ECdouble(_2pX[i-1],_2pY[i-1])
  
  index=0
  while not(scaler & 1):
    index+=1
    scaler>>=1
  _X=_2pX[index]
  _Y=_2pY[index]
  scaler>>=1
  index+=1

  while scaler>0:
    if scaler & 1:
      _X,_Y=ECadd(_X,_Y,_2pX[index],_2pY[index])
    scaler>>=1
    index+=1
  return _X,_Y


# Elliptic curve point substraction (Coming soon)

# Elliptic curve point halving
## the idea is simple half(xG)=xG*2^(ORD-2)
## where ORD is the order of the curve
def EChalf(Px,Py):
  return ECmultp(Px,Py,pow(2,order-2,order))

# Elliptic curve point division (LOL)

#test

# _xx=Gx
# _yy=Gy
# for i in range(10):
#   _xx,_yy=ECdouble(_xx,_yy)
#   print(2<<i,"* G=")
#   print(_xx,_yy)
import random
import time

print("Engine(2/3): Booting up EC Ultra Fast Engine")
#ec 2 
byte_pre=[[] for i in range(32)]
byte_pre[0].append((0,0))
for i in range(1,256):
  byte_pre[0].append(ECmult_super_fast(i))

for j in range(1,32):
  byte_pre[j].append((0,0))
  for i in range(1,256):
    byte_pre[j].append(ECdouble(byte_pre[j-1][i][0],byte_pre[j-1][i][1]))
    for k in range(3):
      byte_pre[j][i]=ECdouble(byte_pre[j][i][0],byte_pre[j][i][1])   

def ECmultx_ultra_fast(scaler):
  if scaler==0:
    return 0,0
  if(scaler==1):
    return Gx,Gy
  scaler-=1
  ind=0
  _x=Gx
  _y=Gy
  while(scaler):
    if scaler&15:
      _x,_y=ECadd(_x,_y,byte_pre[ind][scaler&15][0],byte_pre[ind][scaler&15][1])
    scaler>>=4
    ind+=1
  return _x
print("Checking EC Ultra Fast Engine")
for i in range(100):
  n = random.randint(237824637423,234234234234234234322238947293847923455)
  if ECmultx_super_fast(n)!=ECmultx_ultra_fast(n):
    print(n)
    
print("Engine(3/3): starting EC BLAZE Fast Engine")    
#ec 3 
byte_pre3=[[] for i in range(26)]
byte_pre3[0].append((0,0))
for i in range(1,1024):
  byte_pre3[0].append(ECmult_super_fast(i))

for j in range(1,26):
  # print(j)
  byte_pre3[j].append((0,0))
  for i in range(1,1024):
    byte_pre3[j].append(ECdouble(byte_pre3[j-1][i][0],byte_pre3[j-1][i][1]))
    for k in range(9):
      byte_pre3[j][i]=ECdouble(byte_pre3[j][i][0],byte_pre3[j][i][1])   

def ECmultx_blaze_fast(scaler):
  if scaler==0:
    return 0,0
  if(scaler==1):
    return Gx,Gy
  scaler-=1
  ind=0
  _x=Gx
  _y=Gy
  while(scaler):
    if scaler&1023:
      _x,_y=ECadd(_x,_y,byte_pre3[ind][scaler&1023][0],byte_pre3[ind][scaler&1023][1])
    scaler>>=10
    ind+=1
  return _x

def ECmult_blaze_fast(scaler):
  if scaler==0:
    return 0,0
  if(scaler==1):
    return Gx,Gy
  scaler-=1
  ind=0
  _x=Gx
  _y=Gy
  while(scaler):
    if scaler&1023:
      _x,_y=ECadd(_x,_y,byte_pre3[ind][scaler&1023][0],byte_pre3[ind][scaler&1023][1])
    scaler>>=10
    ind+=1
  return _x,_y
  
print("Checking EC BLAZE Fast Engine")    
for i in range(100):
  n = random.randint(237824637423,234234234234234234322238947293847923455)
  if ECmultx_blaze_fast(n)!=ECmultx_ultra_fast(n):
    print(n)
 
print("All Engines are Ready\n\n\n") 
print("Time to Speed Test")    
#test of speed
#start_time = time.time()
#for i in range(100):
#  n = random.randint(237824637423,234234234234234234322238947293847923455)
#  ECmultx_gen_fast(n)
#print("--- %s seconds ---" % (time.time() - start_time))


start_time = time.time()
for i in range(100):
  n = random.randint(237824637423,234234234234234234322238947293847923455)
  ECmultx_blaze_fast(n)
print("Blaze Fast Engine: --- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
for i in range(100):
  n = random.randint(237824637423,234234234234234234322238947293847923455)
  ECmultx_ultra_fast(n)
print("Ultra Fast Engine: --- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
for i in range(100):
  n = random.randint(237824637423,234234234234234234322238947293847923455)
  ECmultx_super_fast(n)
print("Super fast Engine: --- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
for i in range(100):
  n = random.randint(237824637423,234234234234234234322238947293847923455)
  ECmultx_fast(n)
print("Fast Engine: --- %s seconds ---" % (time.time() - start_time))
print("Engine speed test Done")

##next greater number with same no of setbits GOSPER'S HACK    
def next_num_same_set_bit(Set):
  #Set = (1 << 128) - 1
  #limit = (1 << 256) 
  #while (Set < limit):
  c = Set & -Set
  r = Set + c 
  Set = (((r ^ Set) >> 2) // c) | r
  #print(bin(Set))
  return Set

import random
#generate a random number of x setbits
def get_rand_x_bit(x):
  st=set(())
  while len(st)<x:
    n = random.randint(0,255)
    st.add(n)
  #print(st)
  ans=0
  for xd in st:
    #print(xd)
    ans=ans|(1<<xd)
  #print(bin(ans))
  return ans


#reading pubx
try:
  print("opening all.csv file")  
  filepath = "all.csv"
  fin = open(filepath, "r")
  data = fin.read()
  fin.close()
  data=data.split("\n")
except:
  print("failed to open all.csv file. Please put it in the same directory")
  raise Exception('failed to open all.csv file. Please put it in the same directory')
_arx=[]
_ary=[]



for i in data[:]:
  if i!='':
    pub=i.split(",")[0]
    pubx=pub[2:66]
    puby=pub[66:]
    
    # print(pub)
    # print pubx
    # print puby
    ipubx=int("0x"+pubx,16)
    ipuby=int("0x"+puby,16)
    _arx.append(ipubx)
    _ary.append(ipuby)

#for i in range(10):
#  print(_arx[i])



##searching techniques
#binary search
def bin_src(x):
    low = 0
    high = len(_arx) - 1
    mid = 0
    while low <= high:
        mid = (high + low) // 2
        if _arx[mid] < x:
            low = mid + 1
        elif _arx[mid] > x:
            high = mid - 1
        else:
            return True
    return False

dct={}

vvll=[[] for i in range(100000)]
# vvll[123123%100].append(123123)
# print(vvll)

for xd in _arx:
  dct[xd]=1
  vvll[xd%100000].append(xd)

# for x in vvll:
#   print(x)
#hashes binary search
def hash_bin_src(val):
  bucket=val%10000
  b_arr=vvll[bucket]
  # print(b_arr)
  low = 0
  high = len(b_arr) - 1
  mid = 0
  while low <= high:
      mid = (high + low) // 2
      if b_arr[mid] < val:
          low = mid + 1
      elif b_arr[mid] > val:
          high = mid - 1
      else:
          return True
  return False

#hashed list search
def hash_src(val):
  if val in vvll[val%100000]:
    return True
  return False

#search in dictionary
def dict_src(val):
  if val in dct.keys():
    return True
  return False

#search in list
def list_src(val):
  if val in _arx:
    return True
  return False



print(list_src(27130910361954952328861749905913182248683146585022625587482721713724797111))

is_found=bin_src(27130910361954952328861749905913182248683146585022625587482721713724797111)
print(is_found)


#write data to file
def write_to_file(data):
  file1 = open("found.btc", "a")
  file1.write(data+"\n")
  file1.close()
#write_to_file(str(23761827368)+" "+str(8374682734)+" \n")

#print star of david
def print_star():
  print("                *                ")
  print("             *     *             ") 
  print("           *         *           ") 
  print("  *  *   *   *   *  *  *   *  *  ") 
  print("    *  *                 *  *    ") 
  print("     *                     *     ") 
  print("   *   *                 *   *   ") 
  print(" *   *   *   *   *   *  *   *  * ") 
  print("           *         *           ")
  print("             *     *             ") 
  print("                *                ")
#print_star()

#one lap for fixed size setbit numbers
def one_lap(x_bit,n_num):
  num=get_rand_x_bit(x_bit)
  #print(bin(num),"\n")
  print("from ",num,": checking next ",n_num," ",x_bit,"setbit numbers")
  for i in range(n_num):
    pubk=ECmultx_blaze_fast(num)
    if hash_src(pubk):
      print("found:",num)
      write_to_file("found:"+str(num)+""+str(pubk)+" \n")
      print_star()
    num=next_num_same_set_bit(num)
    #print((num),pubk)

#adjacent lap for numbers in series
def one_lap_adjacent(x_bit,n_num):
  num=get_rand_x_bit(x_bit)
  #print(bin(num),"\n")
  print("from ",num," checking ",n_num," numbers")
  pub_x,pub_y=ECmult_blaze_fast(num)
  for i in range(n_num):
    if hash_src(pub_x):
      print("found:",num+i)
      write_to_file("found:"+str(num+i)+""+str(pub_x)+" \n")
      print_star()
    pub_x,pub_y=ECadd(pub_x,pub_y,Gx,Gy)

import time
start_time = time.time()

while(1):
    '''
    for i in range(10):
      bits_no=random.randint(90,160)#sweet spot
      one_lap(bits_no,1000)
      print("--- %s seconds ---" % (time.time() - start_time))
    ''' 
    for i in range(10):
      bits_no=random.randint(90,160)#sweet spot
      one_lap_adjacent(bits_no,23000)
      print("--- %s seconds ---" % (time.time() - start_time))
