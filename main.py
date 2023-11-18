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
            #print(clean_jobs)
            #print(clean_times)

            # добавляю работам описание
            descriptions = soup.find_all("div", {'data-qa': "resume-block-experience-description"})

            clean_descriptions = []
            for item in descriptions:
                item = item.text.replace('\xa0',' ')
                clean_descriptions.append(item)


            

            for i in range(len(clean_jobs)):
                job_info.append({'Job':clean_jobs[i], 'User_ID':user_id, 'Working_time':clean_times[i], 'Description':clean_descriptions[i]})
                if i >= len(clean_jobs)-1:
                    continue
                # заполняем таблицу переходов
                job_perechod_id += 1
                job_perechod.append({'ID_transition': job_perechod_id, 'Prof_1':clean_jobs[i], 'Prof_2':clean_jobs[i+1], 'Time_transition':clean_times[i]})


                with open("data_frame.csv", "a", encoding="utf-8", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (clean_jobs[i],
                         user_id,
                         clean_times[i],
                         clean_descriptions[i]
                        )
                    )
    with open(f"data_frame.json", "a", encoding="utf-8") as file:
        json.dump(job_info, file, indent=4, ensure_ascii=False)

    with open(f"data_frame2.json", "a", encoding="utf-8") as file:
        for prof in range(len(clean_jobs)):
            json.dump(job_perechod, file, indent=4, ensure_ascii=False)
    








hh_resume_online_parser()
