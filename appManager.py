import os
import requests

from modules.module_cmsWordPress import cmsWordPress
from modules.module_cmsDrupal import cmsDrupal
from modules.module_cmsJoomla import cmsJoomla
from modules.module_savingData import savingData

#########################################################################

class mainManager:

    # ***************************************************************
    def __init__(self, params):
        self.params = params
        self.status = self.main(self.params)

    # ***************************************************************
    def main(self, userSelect):

        pathToFile = userSelect["pathToFile"]
        pathToSave = userSelect["pathToSave"]
        extension = userSelect["extension"]
        genLogs = userSelect["genLogs"]

        fullPath = ""
        if genLogs:
            fileName = "Logs.txt"
            fullPath = os.path.join(pathToSave, fileName)
            file_listLogs = open(fullPath, "w")
            file_listLogs.close()

        finalData = {}
        file_listSites = open(pathToFile, "r")

        for url in file_listSites:
            url = url.strip()
            if url[-1] == "/":
                url = url[:-1]
            print(url)

            secretInfo = self.gettingInfo(url)
            if fullPath != "":
                message = "* " + url + " :\n"

                if "Error connection" not in secretInfo:
                    message += ">>> Identification of Server : "
                    message += "success\n" if "not available"\
                                not in secretInfo["Server"] else "error\n"
                    message += ">>> Identification of CMS : "
                    message += "success\n" if "not defined"\
                                not in secretInfo["CMS"] else "error\n"

                else:
                    message += "error connection\n"

                file_listLogs = open(fullPath, "a")
                file_listLogs.write(message + "#"*50 + "\n")
                file_listLogs.close()

            print(secretInfo)
            print("#" * 50)
            finalData.update({url: secretInfo})
        file_listSites.close()

        ############################################################
        magic = savingData(finalData, pathToSave, extension).status
        ############################################################

        return magic

    # ***************************************************************
    def gettingInfo(self, urlAddress):

        if "http" not in urlAddress:
            urlAddress = "http://" + urlAddress

        result = {}
        try:
            data = requests.get(urlAddress)
        except:
            return "Error connection to '{}'".format(urlAddress)

        primaryInfo = data.headers
        if "server" in primaryInfo.keys() and primaryInfo["server"]!="":
            serverInfo = primaryInfo["server"]
        else:
            serverInfo = "Server info is not available"
        result.update({ "Server": serverInfo })

        cmsInfo = ""
        if cmsWordPress(urlAddress).status == True:
            cmsInfo += "WordPress"
        elif cmsDrupal(urlAddress).status == True:
            cmsInfo += "Drupal"
        elif cmsJoomla(urlAddress).status == True:
            cmsInfo += "Joomla"
        else:
            cmsInfo += "CMS is not defined"
        result.update({ "CMS": cmsInfo })

        return result

#########################################################################

if __name__ == "__main__":
    testParams = {
        'pathToFile': 'D:\\test_siteList.txt',
        'pathToSave': 'D:\\test_saveDir',
        'extension': 'txt',
        'genLogs': True
    }
    status = mainManager(testParams).status
    print("#"*50)
    if status == True:
        print("Information about sites is stored")
    else:
        print("Error when saving data")

#========================================================================
