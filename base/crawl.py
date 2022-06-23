from bs4 import BeautifulSoup
import requests
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
pd.set_option('mode.chained_assignment', None)
class Close():
    def __init__(self,symbol="AAA"):
        super().__init__()
        self.URL_CLOSE = "https://finance.tvsi.com.vn/Enterprises/LichsugiaSymbolPart2?symbol=SYMBOL&currentPage=PAGE&duration=d&startDate=01%2F01%2F2000&endDate=19%2F06%2F2022&_=1655626220398".replace("AAA",symbol)
        self.HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}
        self.symbol=symbol
    def DownloadClose(self):
        return self.download_one_close()

    def fix_link(self,page):
        return self.URL_CLOSE.replace("SYMBOL",self.symbol).replace("PAGE",str(page))

    def download_batch(self,id_batch):
        url = self.fix_link(id_batch)
        rs = requests.get(url, headers = self.HEADERS, verify=False)
        soup = BeautifulSoup(rs.content, 'html.parser')
        table = soup.find('table')
        stock_slice_batch = pd.read_html(str(table))[0]
        return stock_slice_batch

    def download_one_close(self):
        stock_data = pd.DataFrame({})
        for i in range(1000):
            stock_slice_batch = self.download_batch(i + 1)
            stock_data = pd.concat([stock_data, stock_slice_batch], axis=0)
            try:
                date_end_batch = stock_slice_batch["Ngày"].values[-1]
            except:
                break
        return stock_data
