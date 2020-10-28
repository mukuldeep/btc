import urllib.request
import json
from hashlib import sha256
from binascii import unhexlify

#function to convert into little endian format and vice versa
def littleEndian(string):
	splited = [str(string)[i:i + 2] for i in range(0, len(str(string)), 2)]
	splited.reverse()
	return "".join(splited)

#input block hash 
print("enter a valid block hash:")
hash=input()

#block in json format from blockchain.info
url="https://blockchain.info/rawblock/"+hash
response = json.loads(urllib.request.urlopen(url).read())
print("☑ Block read! size: "+str(len(response)))

lst=[]
for i in response["tx"]:
  lst.append(i["hash"]);
print("☑ no of transactions: "+str(len(lst)))

#markle rooh hash generation
##converting transactions into little endian format first
lst2=[]
for i in lst:
  lst2.append(littleEndian(i))

while(len(lst2)>1):
    if(len(lst2)&1):
        lst2.append(lst2[len(lst2)-1])
    new_list=[]
    for i in range(0,len(lst2)-1,2):
      enc_tx2=unhexlify(lst2[i]+lst2[i+1])
      new_list.append(sha256(sha256(enc_tx2).digest()).hexdigest())
    lst2=new_list
markle_root=littleEndian(lst2[0])
print("☑ calculated markle root: "+markle_root)
print("☑ markle root (in block): "+response["mrkl_root"])

if(markle_root==response["mrkl_root"]):
  print("✓ markle root matched!")
else:
  print("✘ markle root doesn't matched!")

#collecting other data from block
version=response["ver"]
previous_block_hash=response["prev_block"]
timestamp=response["time"]
bits=response["bits"]
nonce=response["nonce"]

#hexifying
version=hex(version)[2:]
timestamp=hex(timestamp)[2:]
bits=hex(bits)[2:]
nonce=hex(nonce)[2:]

#converting into little endian format
version=littleEndian(version)
previous_block_hash=littleEndian(previous_block_hash)
markle_root=littleEndian(markle_root)
timestamp=littleEndian(timestamp)
bits=littleEndian(bits)
nonce=littleEndian(nonce)

print("")
print("☐ #little endian hex data:")
print("\t☑ version: "+str(version))
print("\t☑ previous block: "+ str(previous_block_hash))
print("\t☑ markle root: "+markle_root)
print("\t☑ timestamp: "+ str(timestamp))
print("\t☑ bits: "+str(bits))
print("\t☑ nonce: "+str(nonce))
print("")

#combining togather
combined_data=version+previous_block_hash+markle_root+timestamp+bits+nonce
print("☑ combined data: "+combined_data)

#calculating block hash
header = unhexlify(combined_data)
CalculatedHash = sha256(sha256(header).digest()).hexdigest()
CalculatedHash=littleEndian(CalculatedHash)
print("☑ calculated hash: "+CalculatedHash)
print("☑ hash in block  : "+response["hash"])
if(CalculatedHash==response["hash"]):
  print("✓ block hash matched!")
  print("✓ Valid block!")
else:
  print("✘ block hash doesn't matched!")
  print("✘ Invalid block!")
