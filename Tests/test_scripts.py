import unittest
import laley
import os.path
import config
import shutil
import codecs
from bs4 import BeautifulSoup

class LaleyTest(unittest.TestCase):

    def test_extract_expediente_link(self):
        current_folder = os.path.dirname(os.path.realpath(__file__))
        page = os.path.join(current_folder, "Laley/3F06B090353436A90525797C005B72B4.html")
        print page
        expediente_link = "http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/00686?opendocument"
        codigo = "00686"

        result = laley.extract_expediente_link(page)
        self.assertEqual(result[0], expediente_link)
        self.assertEqual(result[1], codigo)


    def test_download_exp_pagina(self):
        codigo = "00686"
        # Create needed folders
        current_folder = os.path.dirname(os.path.realpath(__file__))
        page_folder = os.path.join(current_folder, "pages")
        if not os.path.isdir(page_folder):
            os.mkdir(page_folder)
        
        filename = os.path.join(page_folder, codigo)
        filename += ".html"
        # link = [url, codigo]
        link = ["http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/00686?opendocument"]
        link.append(codigo)

        laley.download_exp_pagina(link)
        result = os.path.isfile(filename)
        self.assertEqual(result, 1)

        result = laley.download_exp_pagina(link)
        self.assertEqual(result, "downloaded already")

        shutil.rmtree(page_folder)


    def test_extract_doc_links(self):
        f = codecs.open("Laley/OpenView.html", "r", "utf-8")
        html = f.read()
        f.close()
        soup = BeautifulSoup(html)
        result = laley.extract_doc_links(soup)

        self.assertEqual(len(result), 100)
        

    def test_create_database(self):
        laley.create_database()
        result = os.path.isfile(os.path.join(config.current_folder, "leyes.db"))
        os.remove(os.path.join(config.current_folder, "leyes.db"))
        self.assertEqual(result, 1)


    def test_insert_data(self):
        current_folder = os.path.dirname(os.path.realpath(__file__))
        page_folder = os.path.join(current_folder, "pages")
        if not os.path.isdir(page_folder):
            os.mkdir(page_folder)

        laley.insert_data()

    def test_extract_metadata(self):
        filename = "Laley/3F06B090353436A90525797C005B72B4.html"
        link_to_pdf = "http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/00686?opendocument"
        result = laley.extract_metadata(filename)

        self.assertEqual(result['codigo'], "00686")
        self.assertEqual(result['link_to_pdf'], link_to_pdf)

    def test_extract_pdf_url(self):
        link = "http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/00686?opendocument"
        pdf_url = "http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc01_2011.nsf/d99575da99ebfbe305256f2e006d1cf0/9d97058b24ac5c0e0525797c00097d25/$FILE/PL00686412012.pdf"
        result = laley.extract_pdf_url(link)
        self.assertEqual(result, pdf_url)

        os.remove("pages/00686.html")
        self.assertEqual(result, pdf_url)

    def test_extract_pdf_url_from_local_file(self):
        link = "http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/visbusqptramdoc/00686?opendocument"
        pdf_url = "http://www2.congreso.gob.pe/Sicr/TraDocEstProc/Contdoc01_2011.nsf/d99575da99ebfbe305256f2e006d1cf0/9d97058b24ac5c0e0525797c00097d25/$FILE/PL00686412012.pdf"
        # also downloads to local folder
        laley.extract_pdf_url(link)
        filename = "pages/00686.html"
        result = laley.extract_pdf_url_from_local_file(filename)
        self.assertEqual(result, pdf_url)




if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner=runner)
