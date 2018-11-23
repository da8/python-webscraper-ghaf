development = False

import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import csv
import os.path
import pickle
import json

sourceUrls = [
    'https://github.com/Autodesk-Forge',
    'https://github.com/Autodesk-Forge?page=2',
    'https://github.com/Autodesk-Forge?page=3'   
]

fileNameRepositoriesNames = 'repositoriesNames.txt'
fileNameRepositoriesDescriptions = 'repositoriesDescriptions.txt'
fileNameRepositoriesJSON = 'repositories.json'

urlRoot = 'https://github.com'

def getWebpageData(method, url):
    if development:
        print (sys._getframe().f_code.co_name)

    http = urllib3.PoolManager()
    r = http.request(method, url)
    return r.data

def deleteFiles():
    if development:
        print (sys._getframe().f_code.co_name)

    try:
        os.remove(fileNameRepositoriesNames)
        os.remove(fileNameRepositoriesDescriptions)
        os.remove(fileNameRepositoriesJSON)
    except OSError:
        pass

def writeToFile(fileName, listData):
    if development:
        print (sys._getframe().f_code.co_name)
        
    dateiWarVorhanden = os.path.isfile(fileName)

    with open(fileName, 'a', newline='') as targetFile:
        fieldNames = [
            'column 1'
        ]

        dictWriter = csv.DictWriter(targetFile, fieldnames = fieldNames) 

        if not dateiWarVorhanden:
            dictWriter.writeheader()

        for dataItem in listData:
            dictWriter.writerow( {'column 1' : dataItem} )

def writeStringToFile(fileName, string):
    with open(fileName, 'w') as fileString:
        fileString.write(string)

'''
</a>
<a data-hovercard-type="repository" data-hovercard-url="/Autodesk-Forge/autodesk-forge.github.io/hovercard" href="/Autodesk-Forge/autodesk-forge.github.io" itemprop="name codeRepository">
          autodesk-forge.github.io
</a>
'''
def getRepositoriesNames(bsWebpage):
    if development:
        print (sys._getframe().f_code.co_name)
        
    anchors = bsWebpage.find_all('a', attrs={"itemprop": "name codeRepository"})

    repositoriesNames = []

    for anchor in anchors:
        repositoryName = anchor.contents[0].strip()

        repositoriesNames.append(repositoryName)

    return repositoriesNames

def getRepositoryName(bsListItem):
    if development:
        print (sys._getframe().f_code.co_name)
        
    anchors = bsListItem.find_all('a', attrs={"itemprop": "name codeRepository"})

    repositoryName = anchors[0].contents[0].strip()

    return repositoryName

'''
<p class="col-9 d-inline-block text-gray mb-2 pr-4" itemprop="description">
          3D model navigation pane: Navigates a 3D model using a synchronized 2D map pane
        </p>
'''
def getRepositoriesDescriptions(bsWebpage):
    if development:
        print (sys._getframe().f_code.co_name)
        
    paragraphs = bsWebpage.find_all('p', attrs={"itemprop": "description"})

    repositoriesDescriptions = []

    for paragraph in paragraphs:
        repositoryDescription = paragraph.contents[0].strip() if paragraph.findChildren() == [] else paragraph.findChildren()[0].contents[0].strip()

        repositoriesDescriptions.append(repositoryDescription)

    return repositoriesDescriptions

def getRepositoryDescription(bsListItem):
    if development:
        print (sys._getframe().f_code.co_name)
        
    paragraphs = bsListItem.find_all('p', attrs={"itemprop": "description"})

    if not paragraphs:
        description = ""
    else:
        description = paragraphs[0].contents[0].strip() if paragraphs[0].findChildren() == [] else paragraphs[0].findChildren()[0].contents[0].strip()

    return description

def getURLWithRoot(url):
    return urlRoot + url

'''
<a itemprop="name codeRepository" data-hovercard-type="repository" data-hovercard-url="/Autodesk-Forge/viewer-walkthrough-online.viewer/hovercard" href="/Autodesk-Forge/viewer-walkthrough-online.viewer" aria-describedby="hovercard-aria-description">
          viewer-walkthrough-online.viewer
</a>
'''
def getRepositoryURL(bsListItem):
    if development:
        print (sys._getframe().f_code.co_name)
        
    anchors = bsListItem.find_all('a', attrs={"itemprop": "name codeRepository"})

    repositoryURL = getURLWithRoot(anchors[0]['href'])

    return repositoryURL

'''
<span class="text-gray-dark mr-2" itemprop="about">
          Online Viewer Walkthrough: Build a viewer that converts and displays models on a browser
        </span>
'''
def getRepositoryWebpageContent(repositoryURL):
    if development:
        print (sys._getframe().f_code.co_name)

    webpage = getWebpageData('GET', repositoryURL)

    bsWebpage = BeautifulSoup(webpage, 'html.parser')

    spans = bsWebpage.find_all('span', attrs={"itemprop": "about"})

    repositoryWebpageContent = "" if (not spans) else spans[0].contents[0].strip()

    return repositoryWebpageContent

def getRepositories(bsWebpage):
    if development:
        print (sys._getframe().f_code.co_name)
        
    repositories = []

    bsListItems = bsWebpage.find_all('li', attrs={"itemprop": "owns"})

    for bsListItem in bsListItems:
        repositoryName = getRepositoryName(bsListItem)

        repositoryDescription = getRepositoryDescription(bsListItem)

        repositoryURL = getRepositoryURL(bsListItem)

        repositoryWebpageContent = getRepositoryWebpageContent(repositoryURL)

        repositoryData = {
            'repositoryName': repositoryName,
            'repositoryDescription': repositoryDescription,
            'repositoryURL': repositoryURL,
            'repositoryWebpageContent': repositoryWebpageContent
        }

        repositories.append(repositoryData)         

    return repositories

def main():
    if development:
        print (sys._getframe().f_code.co_name)
        
    deleteFiles()

    repositories = []
    
    for sourceUrl in sourceUrls:
        webpage = getWebpageData('GET', sourceUrl)

        bsWebpage = BeautifulSoup(webpage, 'html.parser')

        #writeToFile(fileNameRepositoriesNames, getRepositoriesNames(bsWebpage))

        #writeToFile(fileNameRepositoriesDescriptions, getRepositoriesDescriptions(bsWebpage))

        repositories.extend(getRepositories(bsWebpage))

    writeStringToFile(fileNameRepositoriesJSON, json.dumps(repositories, indent=4))

if __name__ == '__main__':
    main()


