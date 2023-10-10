from CommonLib_version_01 import Commonlib, Checking_Process, BeautifulSoup, create_csv, pd

class Universities_url:
    def __init__(self, header):
        self.header = header

    def get_universities_url(self, pagination_soup):
        try:
            for div_tag in pagination_soup.find_all('div', class_='col-md-7'):
                inside_div_tags = div_tag.find('div', class_='row').find_all('div', recursive=False)
                universities_url = inside_div_tags[0].find('a')['href']
                universities_type = inside_div_tags[1].get_text(' ').lstrip('Type').strip()
                if 'High school, Primary school' not in universities_type:
                    print(universities_url)
                    print(universities_type)
                    df = {'Universities or Institution urls': [universities_url], 'Universities or Institution Type': [universities_type]}
                    create_csv(df=pd.DataFrame(df), file_name='Universities_or_Institution_urls.csv')
        except Exception as e:
            print('CSV File is not created...')
            raise e

    def pagination(self):
        try:
            page_num = 1
            page_nav = ''
            commonlib_obj = Commonlib(continuous_count=1, operation='Get universities or institution url', time_delay=0)
            while page_nav is not None:
                pagination_url = f'https://www.studiesinaustralia.com/universities-colleges-tafes-schools/search/results?location=QLD&organisation_cricos_not_null=1&page={page_num}'
                values = {'url': pagination_url, 'header': self.header, 'file name': f'Universities or institution pagination {page_num}'}
                pagination_soup = commonlib_obj.save_data_use_request(values)
                pagination_soup = BeautifulSoup(pagination_soup, 'html.parser')
                self.get_universities_url(pagination_soup)
                page_nav = pagination_soup.find('ul', class_='pagination').find_all('li')[-1].find('a', rel='next')
                page_num += 1
        except Exception as e:
            print('Check pagination part...')
            raise e

if __name__ == '__main__':
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': '_gcl_au=1.1.998454187.1695099697; _gid=GA1.2.1846374984.1695099698; _fbp=fb.1.1695099698506.1053416063; hubspotutk=f31180299b7e9c28c0a0147b09fcf689; __hssrc=1; _ga_1BYWQKJ19B=deleted; _ga=GA1.1.253422625.1695099698; __gads=ID=8bf4979628b95e4a-22fec4a3dee30028:T=1695099697:RT=1695105618:S=ALNI_MZ11WG6uDlsnRkqYj1XH1z_MJjaWw; __gpi=UID=00000c4b80228fb9:T=1695099697:RT=1695105618:S=ALNI_MYwmcgiLw0gWrjC9EvzHqjaSjoBgg; AWSALB=id+XjBxu5xurpB9Jeodduu26Zz5JPyMPS3ZKeQLunnzS2YUCasiTlBKiBmlGrgxdV4SeNPga0Gm36WYUbGGb2+V0N90/TSAWhj/Ugofli17xak1XzD/PO1eDlfjx; AWSALBCORS=id+XjBxu5xurpB9Jeodduu26Zz5JPyMPS3ZKeQLunnzS2YUCasiTlBKiBmlGrgxdV4SeNPga0Gm36WYUbGGb2+V0N90/TSAWhj/Ugofli17xak1XzD/PO1eDlfjx; XSRF-TOKEN=eyJpdiI6ImVRbHBFUkZyRlVmOXVqY3BzTlFjckE9PSIsInZhbHVlIjoiWFhBN1FSUTN2MitOQmU2dnRBNGtDbWs4THhrWlhUcWtZQnZMMHU5YVJ4K0hyc1Q1dlR5MndzSy9UR05jY29nZXVab1ZiS0NIbUJTcW9ZUnhiUmJiSnZyQWs5WTJDdUpra1BNV3BKZ0FXT3hobWF3aWpsS21WN0J6Ym0wVCtiNUUiLCJtYWMiOiJhNTQzMTMyMWJkMjQ2NWI5Njc4YTAwZGQzZDgxZjJjYzMxYzU2ODdlZDAzZTRmMjAzOGMyMDc0OGM2NDY4OTY0IiwidGFnIjoiIn0%3D; geg_web_session=eyJpdiI6IkprNUs1YlJDSTl0MnhQeEwvTGVxVEE9PSIsInZhbHVlIjoidXNGTk9VTjRBZ3p2RHI2M2NLSVNuenZleldpeXUra1ZTSllMZ2d2ano1WEY2NGZwYkNocjc1VVgreWNhRkhWbXBJVUQyczFOYmJ1ZUhsQXhyRFhVcXpXRHhqL2Myd0NhdVdnUmZIVVBLcmFIQ1gxWjc1bWFXYWNHRExyNHFpa0IiLCJtYWMiOiIxMTgyNGFmZmE4ODdkNjBhNjlhOTA5NGVjMDQ3OGJiMjYyYzlkOWFhNzE3NmM2NWMxOWI0MzQ5MWY1NTVkYTJmIiwidGFnIjoiIn0%3D; _uetsid=9d37236056a911ee8fbc252da9b3773a; _uetvid=9d37588056a911ee8a72b188c784d2b3; __hstc=108851421.f31180299b7e9c28c0a0147b09fcf689.1695099698791.1695099698791.1695105620290.2; __hssc=108851421.1.1695105620290; _ga_1BYWQKJ19B=GS1.1.1695105617.2.1.1695105692.0.0.0',
        'Referer': 'https://www.studiesinaustralia.com/universities-colleges-tafes-schools/search/results?location=QLD',
        'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    universities_obj = Universities_url(header)
    universities_obj.pagination()