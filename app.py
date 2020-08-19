from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


def getPage(page):
    # 타겟 URL을 읽어서 HTML를 받아오고,
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://finance.naver.com/sise/sise_market_sum.nhn?page=' + page, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    finance_data = soup.select('table.type_2 > tbody > tr')
    # contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td:nth-child(3)
    # contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td.no
    # contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td:nth-child(4) > img
    # contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td:nth-child(5) > span

    for finance_info in finance_data:

        a_tag = finance_info.select_one('td > a')
        # contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td:nth-child(2) > a
        if a_tag is not None:

            stock = finance_info.select_one('td:nth-child(2) > a').text
            pv = finance_info.select_one('td:nth-child(3)').text
            mk_rank = finance_info.select_one('td.no').text
            rate = finance_info.select_one('td:nth-child(5) > span').text.strip()

            print(stock, pv, mk_rank, rate)

            doc={
                'stock':stock,
                'pv':pv,
                'mk_rank': mk_rank,
                'rate': rate,
            }
            db.finance.insert_one(doc)

getPage('1')
getPage('2')
getPage('3')
getPage('4')

@app.route('/finance_data', methods=['GET'])
def read_financeData():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    result = list(db.finance.find({},{'_id': False}))

    # 2. articles라는 키 값으로 articles 정보 보내주기
    return jsonify({'result': 'success', 'finance': result})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
