#############################################################################
#
#   THIS IS FOR DEMONSTRATION! DON'T USE IT IN PRODUCTION
#     it show how EC signature and verification works
#           [for secp256k1 only]
#############################################################################

P = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1  # prime number for modulus operations
order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # order for the elliptic curve y^2=x^3+7 ,used in bitcoin
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240  # x co-ordinate of generating point of secp256k1 i.e. curve used in bitcoin
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424  # y co-ordinate of generating point of secp256k1 i.e. curve used in bitcoin

#
#     #
#   # # #   copy all the methods from ec.py  that includes mod_inv, ECadd, ECmult, ECmultp etc
#    # #
#

#SIGNING the message 
#NOTE: the message should be in the form of integer here so before sending to this method please do convert
def sign_message(self,msg,prv_k):
    print("signing....")
    #1. generating a random number, say rn
    st=1<<254
    en=self.order-1
    rn=random.randrange(st, en)
    #2. multiplying with the generator point 
    #   and considering x co-ordinate as random part, say, rx
    (rx,ry)=self.ECmult(rn)
    
    #3. generating signature ((random_part*private_key)+message)/random_number_generated_earlier
    #                     sign=((rx*priv_k)+msg)/rn  mod order
    sign=(((rx*prv_k)%self.order+msg)*self.modinv(rn,self.order))%self.order
    
    #4. returning random part and signature
    return (rx,sign)

#VERIFICATION  
#verifying whether the message is signed by the guy with private key for the provided public key or not
def verify_message(self,s,r,msg,pub_x,pub_y):
    print("verifying...")
    #1. dividing message by sign i.e. msg/s mod order and generating our first point on the curve by scaler multiplication with generator point
    m_s=(msg*self.modinv(s,self.order))%self.order
    (x,y)=self.ECmult(m_s)
    
    #2. dividing random_part by sign i.e. r/s mod order and generating our second point
    r_s=(r*self.modinv(s,self.order))%self.order
    (x2,y2)=self.ECmultp(pub_x,pub_y,r_s)
    
    #3. adding these two point to get third point
    (x3,y3)=self.ECadd(x,y,x2,y2)
    
    #4. if the x co-ordiinate of the resulting point equals random_part then the signature is valid else invalid
    if(x3==r):
        print("valid")
        return true
    else:
        print("invalid")
        return false
