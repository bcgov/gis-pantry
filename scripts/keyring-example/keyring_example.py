import keyring
  
keyring.set_password("AGOL","User123","Password@123")
  
credentials = keyring.get_credential("AGOL","")
  
print("Username : ",credentials.username)
print("Password : ",credentials.password)