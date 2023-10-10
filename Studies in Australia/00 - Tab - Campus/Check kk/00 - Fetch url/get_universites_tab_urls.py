from CommonLib_version_01 import os, pd, Checking_Process, create_log, open_html_file, create_csv, Command_line_arg
import inspect

class GetUrl:
    def __init__(self, html_files_path, visited_files):
        self.visited_files = visited_files
        self.html_files_path = html_files_path

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
                    # Get Tab url
                    for li_tag in data.find('ul', id='sections').find_all('li'):
                        if 'Campuses' in str(li_tag):
                            campus_url = li_tag.find('a')['href']
                            # print(campus_url)
                            # create_csv(df=pd.DataFrame({'Campus url': [campus_url]}), file_name='Universities_campus_urls.csv')
                        if 'Ratings' in str(li_tag):
                            rating_url = li_tag.find('a')['href'] + r'/undergraduate'
                            create_csv(df=pd.DataFrame({'Rating url': [rating_url]}), file_name='Universities_rating_urls.csv')
                            rating_url = li_tag.find('a')['href'] + r'/postgraduate'
                            create_csv(df=pd.DataFrame({'Rating url': [rating_url]}), file_name='Universities_rating_urls.csv')
                # create_csv(df=pd.DataFrame({'file name': [files]}), file_name=visited_file_csv_name)


if __name__ == '__main__':
    description = 'Get Universities or Institutions Tab url'
    epilog = '''Usage: py save_universities_or_institution_urls.py -path PATH -operation OPERATION'''
    path_help = r'Give saved universities url HTML file path Example: "F:\Studies in Australia\Studies in Australia\1 - Save Universities or Institutions Url\00 - Saved pages"'
    operation_help = 'Give Save universities page operation name Example: "Get Universities or Institution Tab urls"'

    # args = Command_line_arg(description=description, epilog=epilog, file_name=False, path=True, operation=True,
    #                         path_help=path_help, operation_help=operation_help)

    # html_files_path = args.path
    # operation = args.operation

    html_files_path = r'F:\Studies in Australia\Studies in Australia\1 - Save Universities or Institutions Url\00 - Saved pages'
    operation = 'Get Universities or Institution Tab urls'

    visited_file_csv_name = 'visited_file.csv'
    checking_process_obj = Checking_Process()
    visited_files = checking_process_obj.check_visited_url(visited_file_csv_name)

    get_url_obj = GetUrl(html_files_path=html_files_path, visited_files=visited_files)
    get_url_obj.get_data()