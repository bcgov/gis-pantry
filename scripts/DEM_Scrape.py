'''
Created by:     C.folkers
Date:           January 2023
description:    This script was created with the purpose to download open source zipped DEMs from the Government of British Columbia,
                un-zip them and save them all to a local area.


Copyright 2019 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at 

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''


import requests
import glob
from urllib.request import urlopen
from bs4 import BeautifulSoup
from zipfile import ZipFile

### would be useful to add lines to create files so there is no need to manually

# !!!!!-----!!!!!! Variables !!!!!-----!!!!!!

# input website to navigate and download from
url_var = r'https://pub.data.gov.bc.ca/datasets/175624/'
# Download location for zipped files
output_var =r'your/file/path/here'
#NTS grid list
arealist_var= ['82g/', '82j/', '82f/', '82k/', '82n/','82e/','82l/','82m/','82o/','83d/', '83c/','92h/','92i/','92p/']
# where to un-zip files
zipout_var= r'your/file/path/for/unzipped/files'

# !!!!!-----!!!!!! Define functions !!!!!-----!!!!!!
#Scrape URL for specific lists and download associated data to output folder
def dwnld (url, arealist, output):
   
    #create empty list for download links
    list_of_links=[]
    
    #loop through area list and combine with input website to get to proper directory
    for al in arealist: 
        link=url+al
        #access "new" link created above, to get to specific NTS grid directory
        r=requests.get(link)
        #parse HTML into text 
        soup= BeautifulSoup(r.text, 'html.parser')
        #if soup is printed it will print the entire webpage into text with tags
        # print (soup)

        #loop over all links in NTS grid directory
        for links in soup.find_all('a'):
            # Find all href tags, href attribute/tag specifies the URL of a linked page 
            dl_link=(links.get('href'))

            if dl_link.endswith('.md5'):
                continue
            elif dl_link.startswith('?'):
                continue
            # find the ziped href link that contains the DEM 
            elif dl_link.endswith('.zip'):
                #create download link
                add_link= str(link)+str(dl_link)
                #create path and filename for download 
                filename= (output+dl_link)
                print (filename)

                #open page that contains the download
                with urlopen(add_link) as file:
                    content=file.read()
                #download zipped DEM
                with open (filename, 'wb') as download:
                    download.write(content)


#function to unzip all files in folder to another folder
def unziped(output,zipout):
    outglob= (output+'/*.zip')
    #glob.glob finds all objects in folder with the wildcard specified as .zip
    files= glob.glob(outglob)
    print (len(files))
    #un-zip
    for zipy in files:
        with ZipFile(zipy, 'r') as zip_obj:
            zip_obj.extractall(path=zipout)
        print (zipy+ ' Unzipped \n')

# !!!!!-----!!!!!! call functions !!!!!-----!!!!!!

dwnld(url_var, arealist_var,output_var)
unziped(output_var, zipout_var)


