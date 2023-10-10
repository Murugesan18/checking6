import multiprocessing
from CommonLib_version_01 import os, pd, Checking_Process, Commonlib, Command_line_arg
from concurrent.futures import ThreadPoolExecutor


if __name__ == '__main__':
    description = 'Save Universities or Institutions url'
    epilog = '''Usage: py save_universities_or_institution_urls.py -file_name FILENAME -path PATH -operation OPERATION'''
    file_name_help = 'Give already collected universities url csv file name Example: "Universities_or_Institution_urls.csv"'
    path_help = r'Give saved university url csv file path Example: "F:\Studies in Australia\Studies in Australia\0 - Get Universities or Institutions Url\02 - CSV Files\01 - Saved urls"'
    operation_help = 'Give Save universities page operation name Example: "Save universities or institutions url"'

    args = Command_line_arg(description=description, epilog=epilog, file_name=True, path=True, operation=True, file_name_help=file_name_help, path_help=path_help, operation_help=operation_help)
    csv_file_path = args.path
    csv_file_name = csv_file_path + fr'\{args.file_name}'
    operation = args.operation

    # csv_file_path = r'F:\Studies in Australia\Studies in Australia\0 - Get Universities or Institutions Url\02 - CSV Files\01 - Saved urls'
    # csv_file_name = csv_file_path + r'\Universities_or_Institution_urls.csv'
    # operation = 'Save universities or institutions url'

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

    checking_process_obj = Checking_Process()
    visited_file_list = checking_process_obj.check_visited_html_file(operation)

    common_lib = Commonlib(continuous_count=1, operation=operation, time_delay=0)
    valid_url_list = []
    for index, valid_url in pd.read_csv(csv_file_name).iterrows():
        valid_url = valid_url['Universities or Institution urls']
        file_name = valid_url.split('/', 4)[-1].replace('/', '_')
        if file_name in visited_file_list:
            print('Already saved...', valid_url)
            print('Index: ', index)
        else:
            values = {'url': valid_url, 'file name': file_name, 'header': header}
            valid_url_list.append(values)

    try:
        max_worker = multiprocessing.cpu_count()
    except:
        max_worker = 3

    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        executor.map(common_lib.save_data_use_request, valid_url_list)