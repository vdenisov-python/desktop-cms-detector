import requests
from lxml import html
from lxml import etree
import unittest

#########################################################################

class cmsWordPress:

    #***************************************************************
    def __init__(self, urlAdress):
        self.urlAdress = urlAdress
        self.status = self.onWordPress(self.urlAdress)

    #***************************************************************
    def onWordPress(self, urlAddress):

        data = requests.get(urlAddress)
        tree = html.fromstring(data.text)

        # Анализ тегов <meta>
        metaTags = tree.xpath("//meta")
        for element in metaTags:
            source = etree.tostring(element, encoding="utf-8")
            source = source.decode("utf-8").strip()
            if "wp.com" in source or "wp-content" in source:
                return True

        # Анализ тегов <link>
        for tag in ["link", "a"]:
            linkTags = tree.xpath("//" + tag)
            for element in linkTags:
                source = etree.tostring(element, encoding='utf-8')
                source = source.decode("utf-8").strip()
                if "wp.com" in source or "wp-content" in source:
                    return True

        # Анализ Файла "robots.txt"
        try:
            newUrl = urlAddress + "/robots.txt"
            data = requests.get(newUrl)
            for path in ["wp-admin", "wp-includes", "wp-login"]:
                if path in data.text:
                    return True
        except:
            pass

        # Признаки WordPress не найдены
        return False

#########################################################################

class cmsWordPress_Tests(unittest.TestCase):

    def test_writtenOnWordPress(self):
        test_url = "http://www.bbcamerica.com/"
        status = cmsWordPress(test_url).status
        self.assertEqual(status, True)
        print("{} -> {}".format(test_url, status))

    def test_noWordPressOrError(self):
        test_url = "https://www.yandex.ru/"
        status = cmsWordPress(test_url).status
        self.assertEqual(status, False)
        print("{} -> {}".format(test_url, status))

#########################################################################

if __name__ == "__main__":
    unittest.main()

#========================================================================
