import os
import random
import requests
from bs4 import BeautifulSoup
import json
import csv
from time import sleep
from requests_html import HTML



def hh_resume_online_parser():
    directory = "parsed_data"
    #таблица по профессиям
    user_id = 0
    job_info = []
    job_perechod_id = 0
    job_perechod = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        user_id += 1
        with open(f, encoding="utf-8") as file:
            src = file.read()
            soup = BeautifulSoup(src, "lxml")
            #top_job = soup.find("span", {'data-qa':"resume-block-title-position"})
            jobs = soup.find_all("div", {'data-qa':"resume-block-experience-position"})
            clean_jobs = [] #работы
            #clean_jobs.append(top_job.text)
            times = soup.find_all("div",
                                  class_="bloko-text bloko-text_tertiary")

            clean_times = [] #время работы
            for item in jobs:
                clean_jobs.append(item.text)
            for item in times:
                item = item.text.replace('\xa0',' ')
                clean_times.append(item)
            clean_times.pop(-1)
            print(clean_jobs)
            print(clean_times)

            # добавляю работам описание
            descriptions = soup.find_all("div", {'data-qa': "resume-block-experience-description"})

            # достаю стаж в месяцах
            exp_list = []
            for item in clean_times:
                integers = []
                i = 0
                while i < len(item):
                    s_int = ''
                    while i < len(item) and '0' <= item[i] <= '9':
                        s_int += item[i]
                        i += 1
                    i += 1
                    if s_int != '':
                        integers.append(int(s_int))
                    if len(integers) == 1:
                        months = 12 * integers[0]
                    elif len(integers) == 2:
                        months = 12 * integers[0] + integers[1]
                exp_list.append(months)
            print(exp_list)

            clean_descriptions = []
            for item in descriptions:
                item = item.text.replace('\xa0',' ')
                clean_descriptions.append(item)


            

            for i in range(len(clean_jobs)):
                job_info.append({'Job':clean_jobs[i], 'User_ID':user_id, 'Working_time':exp_list[i], 'Description':clean_descriptions[i]})
                if i >= len(clean_jobs)-1:
                    continue
                # заполняем таблицу переходов
                job_perechod_id += 1
                job_perechod.append({'ID_transition': job_perechod_id, 'User_ID':user_id, 'Prof_1':clean_jobs[i+1], 'Prof_2':clean_jobs[i], 'Time_transition':exp_list[i]})


    with open(f"data_frame.json", "a", encoding="utf-8") as file:
        json.dump(job_info, file, indent=4, ensure_ascii=False)

    with open(f"data_frame2.json", "a", encoding="utf-8") as file:
        json.dump(job_perechod, file, indent=4, ensure_ascii=False)
# def create_error_list(job):
#     error_list = []
#     for i in range(len(job)):
#         error_list.append(job.replace(i, ))
#     return error_list
# print(create_error_list('математик'))
    








hh_resume_online_parser()
