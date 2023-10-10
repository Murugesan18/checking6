import random
import re
import time
from CommonLib_version_01 import os, pd, create_csv, Command_line_arg, Checking_Process, open_html_file, create_log, send_msg
import inspect

import requests


class Get_campus_data:
    def __init__(self, html_files_path, visited_files):
        self.visited_files = visited_files
        self.html_files_path = html_files_path
        self.check_count = 1

    def get_college_name(self, data):
        try:
            campus_url = data.find('meta', property='og:url')['content']
            college_name = data.find('h1').text.strip()
            print(campus_url)
            return campus_url, college_name
        except Exception as e:
            raise e

    # def campus_data(self, data, college_name, college_url, campus_url):
    #     try:
    #
    #     except Exception as e:
    #         raise e

    def get_data(self):
        for files in os.listdir(self.html_files_path):
            if files in self.visited_files:
                print('Already collected data...', files)
            else:
                # Read Html files
                try:
                    data = open_html_file(file_name=files, path=self.html_files_path)
                except Exception as e:
                    line_num = inspect.currentframe().f_lineno
                    create_log(message=e, file_name='read_data', line_num=line_num)
                    data = False

                # Get college data
                if data:
                    # Get college name and url
                    try:
                        campus_url, college_name = self.get_college_name(data)
                        college_url = campus_url.replace('/campuses', '')
                    except Exception as e:
                        print('Check college name and url error: ', e)
                        campus_url, college_name, college_url = '', '', ''

                    # Get college campus data
                    try:
                        check_break_point = False
                        for tr_tag in data.find('table', class_='table').find_all('tr')[1:]:
                            td_tags = tr_tag.find_all('td')
                            campus = td_tags[0].text.strip()
                            address = td_tags[1].text.strip()
                            location_url = td_tags[1].find('a')['href'].replace(' ', '%20')

                            print(campus, ' - ', address)
                            print(location_url)
                            if address != '':
                                try:
                                    payload = {'api_key': '6bdf44168329d02b26fdd58dc2e3d46d', 'url': location_url}
                                    # payload = {'api_key': '6fbe706c8f7af2f58c1290', 'url': location_url}
                                    r = requests.get('http://api.scraperapi.com', params=payload)
                                    status_code = r.status_code
                                    if status_code == 200:
                                        self.check_count = 1
                                    else:
                                        self.check_count += 1
                                    print(self.check_count)
                                    print(status_code)
                                    if self.check_count >= 3:
                                        print(self.check_count)
                                        check_break_point = True
                                    location = re.search('@(-?\d+\.\d+),(-?\d+\.\d+)', r.text)
                                    latitude = location.group(1)
                                    longitude = location.group(2)
                                    time.sleep(random.randint(5, 10))
                                except:
                                    latitude, longitude, check_status = '', '', ''
                            else:
                                latitude, longitude, check_status = '', '', ''

                            df = {'College name': [college_name], 'College url': [college_url],
                                  'Campus url': [campus_url], 'Campus': [campus], 'Address': [address],
                                  'Latitude': [latitude], 'Longitude': [longitude]}
                            create_csv(df=pd.DataFrame(df), file_name='Final_campus_data.csv')

                        if check_break_point:
                            send_msg('Check get campus code')
                            break
                        create_csv(df=pd.DataFrame({'file name': [files]}), file_name=visited_file_csv_name)
                    except Exception as e:
                        print('Check college campus error: ', e)
                        check_status = ''

                    print('-' * 500)
                    # break
if __name__ == '__main__':
    description = 'Get Campus Tab data'
    epilog = '''Usage: py get_campus_data.py -path PATH -operation OPERATION'''
    path_help = r'Give saved universities url HTML file path Example: "F:\Studies in Australia\Studies in Australia\3 - Save Universities or Institutions Tab url\00 - Saved pages\00 - HTML files\Campus tab HTML files"'
    operation_help = 'Give Get campus tab data operation name Example: "Get Campus Tab data"'

    # args = Command_line_arg(description=description, epilog=epilog, file_name=False, path=True, operation=True,
    #                         path_help=path_help, operation_help=operation_help)

    # html_files_path = args.path
    # operation = args.operation


    # for index, row in pd.read_csv('Campus_data.csv')
    html_files_path = r'F:\Studies in Australia\Studies in Australia\3 - Save Universities or Institutions Tab url\00 - Saved pages\00 - HTML files\Campus tab HTML files'
    operation = 'Get Campus Tab data'

    visited_file_csv_name = 'visited_file.csv'
    checking_process_obj = Checking_Process()
    visited_files = checking_process_obj.check_visited_url(visited_file_csv_name)

    get_campus_data_obj = Get_campus_data(html_files_path=html_files_path, visited_files=visited_files)
    get_campus_data_obj.get_data()