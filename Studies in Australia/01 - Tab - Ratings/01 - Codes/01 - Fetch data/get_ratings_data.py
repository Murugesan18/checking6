import re
from CommonLib_version_01 import os, pd, create_csv, Checking_Process, create_log, open_html_file
import inspect

class Get_rating_data:
    def __init__(self, html_files_path, visited_files):
        self.html_files_path = html_files_path
        self.visited_files = visited_files

    def get_college_name(self, data):
        try:
            rating_url = data.find('meta', property='og:url')['content']
            college_name = data.find('h1').text.strip()
            if '/postgraduate' in rating_url:
                postgraduate_rating_url = rating_url
            else:
                postgraduate_rating_url = ''

            if '/undergraduate' in rating_url:
                undergraduate_rating_url = rating_url
            else:
                undergraduate_rating_url = ''

            college_url = rating_url.replace('/postgraduate', '').replace('/undergraduate', '')
            return college_url, college_name, postgraduate_rating_url, undergraduate_rating_url
        except Exception as e:
            raise e

    def get_ratings_data(self, data):
        try:
            graduate_salary, staff_qualification, student_teacher_ratio, full_time_employment = [], [], [], []
            for div_tags in data.find('div', class_='row no-gutters').find_all('div', recursive=False):
                h5_tag = div_tags.find('h5')
                if 'Graduate Salary' in h5_tag.text.strip():
                    graduate_salary_value = h5_tag.find_next('p').text.strip()
                    graduate_salary_value = re.search('\d+,\d+', graduate_salary_value).group()
                    graduate_salary.append(graduate_salary_value)
                if 'Staff Qualification' in h5_tag.text.strip():
                    staff_qualification_value = h5_tag.find_next('p').text.strip()
                    staff_qualification_value = re.search('(\d+)%', staff_qualification_value).group(1)
                    staff_qualification.append(staff_qualification_value)
                if 'Teacher Ratio' in h5_tag.text.strip():
                    student_teacher_ratio_value = h5_tag.find_next('p').text.strip()
                    student_teacher_ratio_value = re.search('there are (\d+) students per (\d+) teaching', student_teacher_ratio_value)
                    student_teacher_ratio_value = f'{student_teacher_ratio_value.group(1)}:{student_teacher_ratio_value.group(2)}'
                    student_teacher_ratio.append(student_teacher_ratio_value)
                if 'Full-Time Employment' in h5_tag.text.strip():
                    full_time_employment_value = h5_tag.find_next('p').text.strip()
                    full_time_employment_value = re.search('(\d+\.?\d+?)%', full_time_employment_value).group(1)
                    full_time_employment.append(full_time_employment_value)

            if len(graduate_salary) == 0:
                graduate_salary = ['']
            if len(staff_qualification) == 0:
                staff_qualification = ['']
            if len(student_teacher_ratio) == 0:
                student_teacher_ratio = ['']
            if len(full_time_employment) == 0:
                full_time_employment = ['']

            return graduate_salary, staff_qualification, student_teacher_ratio, full_time_employment
        except Exception as e:
            raise e
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
                        college_url, college_name, postgraduate_rating_url, undergraduate_rating_url = self.get_college_name(data)
                    except Exception as e:
                        print('Check college name and url error: ', e)
                        college_url, college_name, postgraduate_rating_url, undergraduate_rating_url = '', '', '', ''
                    if 'postgraduate' in files:
                        try:
                            graduate_salary, staff_qualification, student_teacher_ratio, full_time_employment = self.get_ratings_data(data)
                        except Exception as e:
                            print('Check undergraduate rating error...', e)
                            graduate_salary, staff_qualification, student_teacher_ratio, full_time_employment = '', '', '', ''
                        df = {'College name': [college_name], 'College url': [college_url],
                              'Postgraduate rating url': [postgraduate_rating_url],
                              'Postgraduate Graduate salary in dollar': graduate_salary,
                              'Postgraduate Staff qualification in percentage': staff_qualification,
                              'Postgraduate Student Teacher ratio': student_teacher_ratio,
                              'Postgraduate Full time employment in percentage': full_time_employment}

                        create_csv(df=pd.DataFrame(df), file_name='Postgraduate_rating_data.csv')
                    else:
                        try:
                            graduate_salary, staff_qualification, student_teacher_ratio, full_time_employment = self.get_ratings_data(data)
                        except Exception as e:
                            print('Check undergraduate rating error...', e)
                            graduate_salary, staff_qualification, student_teacher_ratio, full_time_employment = '', '', '', ''
                        df = {'College name': [college_name], 'College url': [college_url],
                              'Undergraduate rating url': [undergraduate_rating_url],
                              'Undergraduate Graduate salary in dollar': graduate_salary,
                              'Undergraduate Staff qualification in percentage': staff_qualification,
                              'Undergraduate Student Teacher ratio': student_teacher_ratio,
                              'Undergraduate Full time employment in percentage': full_time_employment}
                        create_csv(df=pd.DataFrame(df), file_name='Undergraduate_rating_data.csv')
                    # break
if __name__ == '__main__':
    description = 'Get Ratings Tab data'
    epilog = '''Usage: py get_ratings_data.py -path PATH -operation OPERATION'''
    path_help = r'Give saved universities url HTML file path Example: "F:\Studies in Australia\Studies in Australia\3 - Save Universities or Institutions Tab url\00 - Saved pages\00 - HTML files\Rating tab HTML files"'
    operation_help = 'Give Get rating tab data operation name Example: "Get Rating Tab data"'

    # args = Command_line_arg(description=description, epilog=epilog, file_name=False, path=True, operation=True,
    #                         path_help=path_help, operation_help=operation_help)

    # html_files_path = args.path
    # operation = args.operation

    html_files_path = r'F:\Studies in Australia\Studies in Australia\3 - Save Universities or Institutions Tab url\00 - Saved pages\00 - HTML files\Rating tab HTML files'
    operation = 'Get Rating Tab data'

    visited_file_csv_name = 'visited_file.csv'
    checking_process_obj = Checking_Process()
    visited_files = checking_process_obj.check_visited_url(visited_file_csv_name)

    get_rating_data_obj = Get_rating_data(html_files_path=html_files_path, visited_files=visited_files)
    get_rating_data_obj.get_data()

    df1 = pd.read_csv('Postgraduate_rating_data.csv')
    df2 = pd.read_csv('Undergraduate_rating_data.csv')
    merge_data = pd.merge(df1, df2, left_on=['College url', 'College name'], right_on=['College url', 'College name'], suffixes=('_left', '_right'), how='inner')
    desired_order = ['College name', 'College url', 'Undergraduate rating url',
                     'Postgraduate rating url', 'Undergraduate Graduate salary in dollar',
                     'Undergraduate Staff qualification in percentage',
                     'Undergraduate Student Teacher ratio',
                     'Undergraduate Full time employment in percentage',
                     'Postgraduate Graduate salary in dollar',
                     'Postgraduate Staff qualification in percentage',
                     'Postgraduate Student Teacher ratio',
                     'Postgraduate Full time employment in percentage']
    merge_data = merge_data[desired_order]
    merge_data.to_csv('Final_ratings_data.csv', index=False)
    os.remove('Postgraduate_rating_data.csv')
    os.remove('Undergraduate_rating_data.csv')