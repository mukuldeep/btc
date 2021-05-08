##########################
# This will work fine with python 2.7.x and may produce inconsistency in other version of python
#
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
_xx=Gx
_yy=Gy
for i in range(10):
  _xx,_yy=ECdouble(_xx,_yy)
  print(2<<i,"* G=")
  print(_xx,_yy)

