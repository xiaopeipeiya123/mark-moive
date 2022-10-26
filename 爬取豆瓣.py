from flask import Flask, request, jsonify, url_for
import requests
import json
import os
import pandas as pd
from bs4 import BeautifulSoup


def movie_info(movie_name):
    url = 'https://movie.douban.com/j/subject_suggest?q=' + movie_name
    html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}).text
    json_data = json.loads(html)
    # 多个结果分别并保存
    result = []
    for i in range(len(json_data)):
        movie_year = json_data[i]['year']
        movel_subtitle = json_data[i]['sub_title']
        movie_title = json_data[i]['title']
        movie_img = json_data[i]['img']
        result.append([movie_year, movel_subtitle, movie_title, movie_img])
    return result


def pandas_to_html(df):
    # style
    styles = [
        dict(selector="th", props=[("font-size", "100%"),
                                      ("text-align", "center"),
                                        ("font-weight", "bold"),
                                        ("color", "#6D7993"),
                                        ("background-color", "#E1E1E1")]),
        dict(selector="td", props=[("font-size", "100%"),
                                    ("text-align", "center")]),
        dict(selector="caption", props=[("caption-side", "bottom")])
    ]

    for i in range(len(df)):
        img_url = df['movie_img'][i]
        img_name = df['movie_title'][i] + '.jpg'
        img_path = 'static/img/' + img_name
        if not os.path.exists(img_path):
            with open(img_path, 'wb') as f:
                f.write(requests.get(img_url).content)
        df['movie_img'][i] = '<img src="' + img_path + '" width="100px" height="150px" />'
    return df.style.set_table_styles(styles).render()


app = Flask(__name__)

@app.route('/')
def index():
    # 读取html文件
    with open('static\html\index.HTML', 'r', encoding='utf-8') as f:
        # 引入样式表
        html = f.read().replace('style.css', url_for('static', filename='css/style.css'))
        html = html.replace('iconfont.css', url_for('static', filename='html/ico/iconfont.css'))

    return html

@app.route('/search')
def search():
    movie_name = request.args.get('movie_name')
    result = movie_info(movie_name)
    df = pd.DataFrame(result, columns=['movie_year', 'movel_subtitle', 'movie_title', 'movie_img'])
    return pandas_to_html(df)

if __name__ == '__main__':
    app.run()