import requests
from lxml import html
from lxml import etree
import unittest

#########################################################################

class cmsDrupal:

    #***************************************************************
    def __init__(self, urlAdress):
        self.urlAdress = urlAdress
        self.status = self.onDrupal(self.urlAdress)

    #***************************************************************
    def onDrupal(self, urlAddress):

        data = requests.get(urlAddress)
        tree = html.fromstring(data.text)

        # Анализ тегов <meta>
        metaTags = tree.xpath("//meta")
        for element in metaTags:
            source = etree.tostring(element, encoding="utf-8")
            source = source.decode("utf-8").strip()
            if "Drupal" in source or "drupal.org" in source:
                return True

        # Анализ Файла "robots.txt"
        try:
            newUrl = urlAddress + "/robots.txt"
            data = requests.get(newUrl)
            for path in [": /?q=", ": /admin/", ": /user/"]:
                if path in data.text:
                    return True
        except:
            pass

        # Признаки Drupal не найдены
        return False

#########################################################################

class cmsDrupal_Tests(unittest.TestCase):

    def test_writtenOnDrupal(self):
        test_url = "https://www.whitehouse.gov/"
        status = cmsDrupal(test_url).status
        self.assertEqual(status, True)
        print("{} -> {}".format(test_url, status))

    def test_noDrupalOrError(self):
        test_url = "https://www.yandex.ru/"
        status = cmsDrupal(test_url).status
        self.assertEqual(status, False)
        print("{} -> {}".format(test_url, status))

#########################################################################

if __name__ == "__main__":
    unittest.main()

#========================================================================