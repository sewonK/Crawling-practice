from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
start = time.time()  # 시작 시간 저장
# driver = webdriver.Chrome('chromedriver.exe')
# driver.implicitly_wait(3)
# driver.get('https://keyescape.co.kr/web/home.php?go=rev.make')
# driver.find_element_by_link_text('부산점').click()
# driver.find_element_by_link_text('30').click()
# 전체 지점 가져오기
# themes = driver.find_element_by_id('zizum_data')
# print(themes.get_attribute('innerHTML'))

url="https://keyescape.co.kr/web/home.php?go=rev.theme_time"

cafes = {"우주라이크": "16"
            ,"강남더어썸": "15"
            ,"강남더오름": "14"
            ,"강남점": "3"
            ,"부산점": "9"
            ,"전주점": "7"
            ,"홍대점": "10"
            # ,"혜화점": "4" 영업종료
            # ,"명동점": "5" 영업종료
        }

cafesInGangnam = {"우주라이크": "16"
                    ,"강남더어썸": "15"
                    ,"강남더오름": "14"
                    ,"강남점": "3"
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
def getThemeTime(cafes, time):
    for name in cafes.keys():
        for theme in cafeThemes[cafes[name]]:
            response = requests.post(url, data={"zizum_num":cafes[name], "rev_days":time, "theme_num":theme})
            response.encoding = None

            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            possibleThemes = soup.select('.possible')
            impossibleThemes = soup.select('.impossible')
            print(name + "점의 <" + themeName[theme] + ">테마 예약정보(" + time + ")")
            print("가능한 시간대")
            for theme in possibleThemes:
                print(theme.text.strip())

            print("불가능한 시간대")
            for theme in impossibleThemes:
                print(theme.text.strip())

getThemeTime(cafes, '2021-08-30')
print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간