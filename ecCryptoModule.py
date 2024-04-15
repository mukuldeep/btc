import random

class crypto:
    P = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1  # prime number for modulus operations
    order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # order for the elliptic curve y^2=x^3+7 ,used in bitcoin
    Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240  # x co-ordinate of generating point of secp256k1 i.e. curve used in bitcoin
    Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424  # y co-ordinate of generating point of secp256k1 i.e. curve used in bitcoin

    # mod inverse
    # Extended Euclidean Algorithm for finding mod inverse
    def modinv(self,a, n):
        lm, hm = 1, 0
        low, high = a % n, n
        while low > 1:
            ratio = high // low
            nm = hm - lm * ratio
            new = high - low * ratio
            hm = lm
            high = low
            lm = nm
            low = new
        return lm % n

    # Elliptic curve point addition
    def ECadd(self,xp, yp, xq, yq):
        # point addition will not work if both the point are same. So, point doubling is required
        if xp == xq and yp == yq:
            return self.ECdouble(xp, yp)

        m = ((yq - yp) * self.modinv(xq - xp, self.P)) % self.P
        xr = (m * m - xp - xq) % self.P
        yr = (m * (xp - xr) - yp) % self.P
        return (xr, yr)

    # Elliptic curve point subtraction i.e. (p1x,p1y)+(p2x,-p2y)
    def ECsubtract(self,p1x,p1y,p2x,p2y):
        if(p1x==p2x):
            print("invalid point subtraction")
            return (0,0)
        return self.ECadd(p1x,p1y,p2x,(self.P-p2y)%self.P)

    # Elliptic curve point doubling
    def ECdouble(self,xp, yp):
        l = ((3 * xp * xp) * self.modinv(2 * yp, self.P)) % self.P
        X = (l * l - 2 * xp) % self.P
        Y = (l * (xp - X) - yp) % self.P
        return X, Y

    # Elliptic curve point multiplication
    ##1. scaler multiplication with generator point
    def ECmult(self,scaler):
        if scaler == 0:
            return 0, 0
        _2pX = [0] * 258
        _2pY = [0] * 258
        _2pX[0], _2pY[0] = self.Gx, self.Gy
        _X = self.Gx
        _Y = self.Gy
        for i in range(1, 257):
            _2pX[i], _2pY[i] = self.ECdouble(_2pX[i - 1], _2pY[i - 1])

        index = 0
        while not (scaler & 1):
            index += 1
            scaler >>= 1
        _X = _2pX[index]
        _Y = _2pY[index]
        scaler >>= 1
        index += 1
        while scaler > 0:
            if scaler & 1:
                _X, _Y = self.ECadd(_X, _Y, _2pX[index], _2pY[index])
            scaler >>= 1
            index += 1
        return _X, _Y

    # fast EC scaler multiplication 4x faster than previous method
    # this can be improved more by catching precalculating group by few bits.
    def ECmult_fast(scaler):
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
        return _x,_y

    ##2. scaler multiplication with other point on secp256k1 curve
    ###Example 2*(4G)=8G 4*(5G)=20G etc.
    def ECmultp(self,Sx, Sy, scaler):
        _2pX = [0] * 258
        _2pY = [0] * 258
        _2pX[0], _2pY[0] = Sx, Sy
        _X = Sx
        _Y = Sy
        for i in range(1, 257):
            _2pX[i], _2pY[i] = self.ECdouble(_2pX[i - 1], _2pY[i - 1])

        index = 0
        while not (scaler & 1):
            index += 1
            scaler >>= 1
        _X = _2pX[index]
        _Y = _2pY[index]
        scaler >>= 1
        index += 1

        while scaler > 0:
            if scaler & 1:
                _X, _Y = self.ECadd(_X, _Y, _2pX[index], _2pY[index])
            scaler >>= 1
            index += 1
        return _X, _Y

    # ECscalerDivide divide a ECpoint by a scaler number
    # e.g. 8G/2=4G
    def ECscalerDivide(self,x,y,scaler):
      return self.ECmultp(x,y,self.modinv(scaler,self.order))

    # find possible y coordinates w.r.t x coordinate
    # y^2 = x^3+7
    # y = pow_mod(x^3+7,P+1//4)
    def ECxToy(self,x):
      a = (pow(x, 3, self.P) + 7) % self.P
      y = pow(a, (self.P+1)//4, self.P)
      return y,(self.P-y)%self.P

    #Generate a private key
    def generate_private_key(self):
        st = 1 << 254
        en = self.order - 1
        rn = random.randrange(st, en)
        (rx, ry) = self.ECmult(rn)
        rn=(rx+ry)%self.order
        (rx, ry) = self.ECmult(rn)
        return ry;

    #private key to public key conversion i.e. x coordinate of G*priv
    def private_to_public(self,priv_k):
        return self.ECmult(priv_k)

    ## Signing message and returning random part and signature
    def sign_message(self,msg,rn,prv_k):
        print("signing....")
        #order=115792089237316195423570985008687907852837564279074904382605163141518161494337
        st=1<<254
        en=self.order-1
        #rn=random.randrange(st, en)
        #print(rn)
        (rx,ry)=self.ECmult(rn)
        #print(rx,ry)
        sign=(((rx*prv_k)%self.order+msg)*self.modinv(rn,self.order))%self.order
        print("rx:",rx)
        print("sign:",sign)
        return (rx,sign)

    #verifying message
    def verify_message(self,s,r,msg,pub_x,pub_y):
        print("verifying...")
        m_s=(msg*self.modinv(s,self.order))%self.order
        print("m_s:",m_s)
        r_s=(r*self.modinv(s,self.order))%self.order
        print("r_s:",r_s)
        (x,y)=self.ECmult(m_s)
        (x2,y2)=self.ECmultp(pub_x,pub_y,r_s)
        (x3,y3)=self.ECadd(x,y,x2,y2)
        print("(x,y):",(x,y))
        print("(x2,y2):",(x2,y2))
        print("(x3,y3):",(x3,y3))
        if(x3==r):
            #print("valid")
            return True
        else:
            #print("invalid")
            return False

    #encryption of message to be send
    #Currently this is only xor(NOT SECURE), it is to be changed to ECadd & ECsub
    def encrypt_message(self,msg,r,prv_k,pub_k):
        (px,py)=self.ECmultp(pub_k[0],pub_k[1],prv_k)
        (rx,ry)=self.ECmultp(px,py,r)
        enc_msg=0
        l=0
        cnt=0
        for ch in msg:
            cnt+=1
            # print(ord(ch))
            l<<=8
            l+=ord(ch)
            if(cnt==30):
                cnt=0
                l=l^rx
                enc_msg <<= 256
                enc_msg|=l
                l=0
        if(l):
            l = l ^ rx
            enc_msg <<= 256
            enc_msg |= l

        # print(l)
        # enc_msg=l+rx
        # print(enc_msg)
        return enc_msg
        # encoded_string = msg.encode()
        # byte_array = bytearray(encoded_string)
        # print(byte_array)


    # encryption of message to be send
    # Currently this is only xor(NOT SECURE), it is to be changed to ECadd & ECsub Concept
    def decrypt_message(self,enc_msg,r,prv_k,pub_k):
        (px, py) = self.ECmultp(pub_k[0], pub_k[1], prv_k)
        (rx, ry) = self.ECmultp(px, py, r)
        msg=""
        while(enc_msg):
            l=enc_msg&((1<<256)-1)^rx
            while(l):
                ch_i=l&255
                msg=chr(ch_i)+msg
                l>>=8
            enc_msg>>=256
        #print(msg)
        return msg
