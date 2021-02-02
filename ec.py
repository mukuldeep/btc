##########################
# This will work fine with python 2.7.x and may produce inconsistency in other version of python
#
#
##########################
P = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1 #prime number for modulus operations
order= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 #order for the elliptic curve y^2=x^3+7 ,used in bitcoin
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240 #x co-ordinate of generating point of secp256k1 i.e. curve used in bitcoin
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424 #y co-ordinate of generating point of secp256k1 i.e. curve used in bitcoin

def modinv(a,n): # Extended Euclidean Algorithm
    lm, hm = 1,0
    low, high = a%n,n
    while low > 1:
        ratio = high/low
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
  
# Elliptic curve point multiplication (Coming soon)

# Elliptic curve point substraction (Coming soon)

# Elliptic curve point division (LOL)

#test
_xx=Gx
_yy=Gy
for i in range(10):
  _xx,_yy=ECdouble(_xx,_yy)
  print(2<<i,"* G=")
  print(_xx,_yy)

