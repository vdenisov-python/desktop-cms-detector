import os
import xlrd, xlwt
import unittest

#########################################################################

class savingData:

    #***************************************************************
    def __init__(self, finalData, pathToSave, extension):
        self.params = [finalData, pathToSave, extension]
        self.status = self.manager(self.params)

    #***************************************************************
    def manager(self, params):

        finalData = params[0]
        pathToSave = params[1]
        extension = params[2]

        status = os.path.exists(pathToSave)

        if status != True:
            try:
                os.mkdir(pathToSave)
            except:
                print("File system error")
                print("#" * 50)
                return False

        if extension == "txt":
            status = self.saveToTXT(finalData, pathToSave)
        elif extension == "xls":
            status = self.saveToXLS(finalData, pathToSave)
        else:
            status = False

        return status

    #***************************************************************
    def saveToTXT(self, finalData, pathToSave):

        atLeastOne = False

        for siteName in finalData.keys():

            secretInfo = finalData[siteName]
            if "Error connection" in secretInfo:
                print("Error connection to '{}'".format(siteName))
                continue

            fileName = "[{}].txt".format(siteName)
            fullPath = os.path.join(pathToSave, fileName)

            if os.path.exists(fullPath):
                continue

            try:
                reportFile = open(fullPath, "w")
                reportFile.write( "Server : {}\n".format(secretInfo["Server"]) )
                reportFile.write( "CMS : {}\n".format(secretInfo["CMS"]) )
                reportFile.close()
                atLeastOne = True
            except:
                print("Invalid file name : " + fileName)
                print("#" * 50)
                continue

        return atLeastOne

    #***************************************************************
    def saveToXLS(self, finalData, pathToSave):

        atLeastOne = False

        title = [
            ["Name of site", "Info about server", "Info about CMS"],
            ["", "", ""]
        ]

        dataBase = []

        for siteName in finalData.keys():

            secretInfo = finalData[siteName]
            if "Error connection" in secretInfo:
                print("Error connection to '{}'".format(siteName))
                continue

            siteInfo = [ siteName, secretInfo["Server"], secretInfo["CMS"] ]
            dataBase.append(siteInfo)

        if len(dataBase) > -1:

            atLeastOne = True

            dataForTable = title + dataBase

            pathToSave = pathToSave.replace("/", "\\")
            fileName = "Results_of_analysis.xls"
            fullPath = os.path.join(pathToSave, fileName)

            workBook = xlwt.Workbook()
            workSheet = workBook.add_sheet("analysisResults")
            for n in range(0, 3):
                workSheet.col(n).width = 7500

            for i in range(len(dataForTable)):
                id_row = i
                for j in range(len( dataForTable[i] )):
                    id_column = j
                    workSheet.write(id_row, id_column, dataForTable[i][j])

            workBook.save(fullPath)

        return atLeastOne

#########################################################################

if __name__ == "__main__":
    pathToSave = "D:/test_saveDir"
    extension = "xls"
    finalData = {
        "site#1": {
            "Server": "server#1",
            "CMS": "CMS#1"
        },
        "site#2": {
            "Server": "server#2",
            "CMS": "CMS#2"
        },
        "site#3": {
            "Server": "server#3",
            "CMS": "CMS#3"
        }
    }

    status = savingData(finalData, pathToSave, extension).status

    print(status)

#========================================================================
