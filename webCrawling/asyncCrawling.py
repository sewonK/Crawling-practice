from asyncio import futures
from bs4 import BeautifulSoup
import time
import asyncio

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

async def getThemeTime(cafe, date):
    # for cafe in cafes:
    for theme in cafeThemes[cafe]:

        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, data={"zizum_num":cafe, "rev_days":date, "theme_num":theme}) as res:
                res.encoding = None
                html = await res.text()

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

async def main():
    cafes = ["16", "15", "14", "3", "9", "7", "10"]
    date = '2021-08-30'
    futures = [asyncio.ensure_future(getThemeTime(cafe, date)) for cafe in cafes]
    await asyncio.gather(*futures)

if __name__ == "__main__":
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("--- elapsed time %s seconds ---" % (time.time() - start_time))
