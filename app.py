import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://finance.naver.com/sise/sise_market_sum.nhn', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

finance_data = soup.select('table.type_2 > tbody > tr')
# contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td:nth-child(3)
# contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td.no
# contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td:nth-child(4) > img

for finance_info in finance_data:

    a_tag = finance_info.select_one('td > a')
    # contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td:nth-child(2) > a
    if a_tag is not None:

        pv = finance_info.select_one('td:nth-child(3)').text
        mk_rank = finance_info.select_one('td.no').text
        rate = finance_info.select_one('td:nth-child(4) > img')['alt']

        print(pv, mk_rank, rate)
