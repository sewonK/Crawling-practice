# from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from multiprocessing import Pool

# driver = webdriver.Chrome('chromedriver.exe')
# driver.implicitly_wait(3)
# driver.get('https://keyescape.co.kr/web/home.php?go=rev.make')
# driver.find_element_by_link_text('부산점').click()
# driver.find_element_by_link_text('30').click()
# 전체 지점 가져오기
# themes = driver.find_element_by_id('zizum_data')
# print(themes.get_attribute('innerHTML'))

url="https://keyescape.co.kr/web/home.php?go=rev.theme_time"

cafeName = {"16": "우주라이크"
            ,"15": "강남더어썸"
            ,"14": "강남더오름"
            ,"3": "강남점"
            ,"9": "부산점"
            ,"7": "전주점"
            ,"10": "홍대점"
        }

cafeThemes = {"16": ["55"]
            ,"15":["53", "54"]
            ,"14":["48", "51"]
            ,"3":["5", "6", "7"]
            ,"9":["37", "38", "35", "39", "36"]
            ,"7":["32", "31", "29", "33", "30"]
            ,"10":["41", "45", "43"]
        }

themeName = {"55" : "US"
            ,"53" : "원더리아"
            ,"54" : "BACK TO THE SCENE"
            ,"48" : "네드"
            ,"51" : "엔제리오"
            ,"5" : "월야애담"
            ,"6" : "살랑살랑연구소"
            ,"7" : "그카지말라캤자나"
            ,"37" : "정신병동"
            ,"38" : "파파라치"
            ,"35" : "난쟁이의 장난"
            ,"39" : "셜록 죽음의 전화"
            ,"36" : "신비의숲 고대마법의 비밀"
            ,"32" : "난쟁이의 장난"
            ,"31" : "혜화잡화점"
            ,"29" : "월야애담"
            ,"33" : "사라진 목격자"
            ,"30" : "살랑살랑연구소"
            ,"41" : "삐릿-뽀"
            ,"45" : "홀리데이"
            ,"43" : "고백"
            }

cafes = ["16", "15", "14", "3", "9", "7", "10"]
date = '2021-08-30'
def getThemeTime(theme, cafe):
    # for theme in cafeThemes[cafe]:
        response = requests.post(url, data={"zizum_num":cafe, "rev_days":date, "theme_num":theme})
        response.encoding = None

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        possibleThemes = soup.select('.possible')
        impossibleThemes = soup.select('.impossible')
        print(cafeName[cafe] + "점의 <" + themeName[theme] + ">테마 예약정보(" + date + ")")
        print("가능한 시간대")
        for theme in possibleThemes:
            print(theme.text.strip())

        print("불가능한 시간대")
        for theme in impossibleThemes:
            print(theme.text.strip())

def getCafeTheme(cafe):
    return cafeThemes[cafe]

def do_thread_crawl(cafe, themes: list):
    thread_list = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for theme in themes:
            thread_list.append(executor.submit(getThemeTime, theme, cafe))
        for execution in concurrent.futures.as_completed(thread_list):
            execution.result()

def do_process_with_thread_crawl(cafe: str):
    do_thread_crawl(cafe, getCafeTheme(cafe))

if __name__ == "__main__":
    start_time = time.time()

    with Pool(processes=4) as pool:
        pool.map(do_process_with_thread_crawl, cafes)
        print("--- elapsed time %s seconds ---" % (time.time() - start_time))

