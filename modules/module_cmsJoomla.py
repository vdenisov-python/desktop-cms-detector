import requests
from lxml import html
from lxml import etree
import unittest

#########################################################################

class cmsJoomla:

    #***************************************************************
    def __init__(self, urlAdress):
        self.urlAdress = urlAdress
        self.status = self.onJoomla(self.urlAdress)

    #***************************************************************
    def onJoomla(self, urlAddress):

        data = requests.get(urlAddress)
        tree = html.fromstring(data.text)

        # Анализ тегов <meta>
        metaTags = tree.xpath("//meta")
        for element in metaTags:
            source = etree.tostring(element, encoding="utf-8")
            source = source.decode("utf-8").strip()
            if "Joomla" in source:
                return True

        # Анализ тегов <link>
        for tag in ["link", "a"]:
            linkTags = tree.xpath("//" + tag)
            for element in linkTags:
                source = etree.tostring(element, encoding='utf-8')
                source = source.decode("utf-8").strip()
                if "joomla" in source:
                    return True

        # Анализ Файла "robots.txt"
        try:
            newUrl = urlAddress + "/robots.txt"
            data = requests.get(newUrl)
            for path in [": /administrator/", ": /installation/"]:
                if path in data.text:
                    return True
        except:
            pass

        # Признаки Joomla не найдены
        return False

#########################################################################

class cmsJoomla_Tests(unittest.TestCase):

    def test_writtenOnJoomla(self):
        test_url = "http://www.fudzilla.com/"
        status = cmsJoomla(test_url).status
        self.assertEqual(status, True)
        print("{} -> {}".format(test_url, status))

    def test_noJoomlaOrError(self):
        test_url = "https://www.yandex.ru/"
        status = cmsJoomla(test_url).status
        self.assertEqual(status, False)
        print("{} -> {}".format(test_url, status))

#############################################################

if __name__ == "__main__":
    unittest.main()

#========================================================================
