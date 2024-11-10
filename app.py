# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Survey, Response
from config import Config
import os
import json
from datetime import datetime


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 確保資料庫目錄存在
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # 初始化資料庫
    db.init_app(app)

    # 在應用程式環境中建立資料表
    with app.app_context():
        db.create_all()
        print("資料庫表格已建立")

    return app


app = create_app()


def get_questions():
    """取得問卷問題"""
    return [
        {
            'id': 1,
            'positive': "如果藏壽司提供線上訂位系統，可以提前預約座位，您會覺得如何？",
            'negative': "如果只能現場排隊，無法預約座位，您會覺得如何？"
        },
        {
            'id': 2,
            'positive': "如果藏壽司提供手機APP叫號，可以即時查看目前叫到幾號，您會覺得如何？",
            'negative': "如果藏壽司只提供傳統紙本叫號，無法遠端查看進度，您會覺得如何？"
        },
        {
            'id': 3,
            'positive': "如果藏壽司提供行動支付（如：Apple Pay、LINE Pay等）結帳選項，您會覺得如何？",
            'negative': "如果藏壽司只接受現金和信用卡支付，您會覺得如何？"
        },
        {
            'id': 4,
            'positive': "如果每5盤壽司就可以扭一次蛋，有機會獲得限定商品，您會覺得如何？ ",
            'negative': "如果沒有任何集點或扭蛋活動，您會覺得如何？"
        },
        {
            'id': 5,
            'positive': "如果可以透過平板點餐，讓喜愛的壽司以專屬軌道方式直送座位，您會覺得如何？",
            'negative': "如果只能等待一般迴轉轉盤送餐，無法以專屬軌道方式送餐，您會覺得如何？"
        },
        {
            'id': 6,
            'positive': "如果每盤壽司在迴轉轉盤上有次數上限避免因運轉時間過長而不新鮮，您會覺得如何？",
            'negative': "如果每盤壽司在迴轉轉盤上沒有次數上限避免浪費食物，您會覺得如何？"
        },
        {
            'id': 7,
            'positive': "如果菜單提供多國語言（中、英、日）對照與詳細食材說明，您會覺得如何？",
            'negative': "如果菜單只有中文說明，且無詳細食材標示，您會覺得如何？"
        },
        {
            'id': 8,
            'positive': "如果座位旁有電子螢幕即時顯示用餐盤數，方便計算消費金額，您會覺得如何？",
            'negative': "如果需要自行數盤子或等結帳時才知道總數，您會覺得如何？"
        },
        {
            'id': 9,
            'positive': "如果透過社群網站可以查看未來一週的季節限定壽司或活動排程，您會覺得如何？ ",
            'negative': "如果無法預知的季節限定壽司或活動排程，需要每次到店詢問，您會覺得如何？"
        },
        {
            'id': 10,
            'positive': "如果店內播放輕柔的日式音樂，音量適中，您會覺得如何？",
            'negative': "如果店內無背景音樂，只有機器運轉與人聲，您會覺得如何？"
        },
    ]


def calculate_kano_category(positive, negative):
    """計算 KANO 分類"""
    kano_matrix = {
        '1,1': 'Q', '1,2': 'A', '1,3': 'A', '1,4': 'A', '1,5': 'O',
        '2,1': 'R', '2,2': 'I', '2,3': 'I', '2,4': 'I', '2,5': 'M',
        '3,1': 'R', '3,2': 'I', '3,3': 'I', '3,4': 'I', '3,5': 'M',
        '4,1': 'R', '4,2': 'I', '4,3': 'I', '4,4': 'I', '4,5': 'M',
        '5,1': 'R', '5,2': 'R', '5,3': 'R', '5,4': 'R', '5,5': 'Q'
    }
    key = f"{positive},{negative}"
    return kano_matrix.get(key, 'Q')


@app.route('/')
def index():
    """問卷填寫頁面"""
    return render_template('survey.html', questions=get_questions())


@app.route('/submit', methods=['POST'])
def submit_survey():
    """提交問卷"""
    try:
        data = request.get_json()
        print("收到的資料:", data)  # 偵錯用

        # 建立新的問卷記錄
        survey = Survey()
        db.session.add(survey)
        db.session.flush()  # 取得 survey.id

        # 處理每個問題的回應
        for question_id, responses in data.items():
            # 轉換問題 ID 為整數
            q_id = int(question_id)
            pos_response = int(responses['positive'])
            neg_response = int(responses['negative'])

            # 計算 KANO 分類
            category = calculate_kano_category(pos_response, neg_response)

            # 建立回應記錄
            response = Response(
                survey_id=survey.id,
                question_id=q_id,
                positive_response=pos_response,
                negative_response=neg_response,
                kano_category=category
            )
            db.session.add(response)

        db.session.commit()
        return jsonify({'status': 'success'})

    except Exception as e:
        print("錯誤:", str(e))  # 偵錯用
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/results')
def view_results():
    """查看統計結果"""
    # 取得所有回應
    responses = Response.query.all()

    # 初始化結果統計
    results = {}
    categories = ['A', 'O', 'M', 'I', 'R', 'Q']
    questions = get_questions()

    # 初始化每個問題的分類計數
    for question in questions:
        results[question['id']] = {cat: 0 for cat in categories}

    # 統計每個問題的各分類數量
    for response in responses:
        results[response.question_id][response.kano_category] += 1

    return render_template('results.html',
                           results=results,
                           questions=questions,
                           categories=categories)


@app.route('/responses')
def view_responses():
    """查看個別回應"""
    surveys = Survey.query.order_by(Survey.timestamp.desc()).all()
    questions = get_questions()

    # 建立選項對照表
    response_options = {
        1: '滿意',
        2: '有些滿意',
        3: '無所謂',
        4: '有些不滿意',
        5: '不滿意'
    }

    return render_template('responses.html',
                           surveys=surveys,
                           questions=questions,
                           response_options=response_options)


# KANO 分類說明
kano_descriptions = {
    'A': '魅力品質 - 提供時會令顧客滿意，但不提供也不會不滿意',
    'O': '一維品質 - 提供時會令顧客滿意，不提供會令顧客不滿意',
    'M': '必要品質 - 提供時顧客視為理所當然，不提供會令顧客不滿意',
    'I': '無差異品質 - 提供與否都不會影響顧客滿意度',
    'R': '反向品質 - 提供反而會令顧客不滿意',
    'Q': '可疑結果 - 問卷回答可能有誤'
}


@app.template_filter('format_datetime')
def format_datetime(value):
    """格式化日期時間"""
    if value is None:
        return ""
    return value.strftime('%Y-%m-%d %H:%M:%S')


@app.context_processor
def utility_processor():
    """提供模板使用的工具函數"""
    return {
        'kano_descriptions': kano_descriptions,
    }

@app.route('/delete_survey/<int:survey_id>', methods=['POST'])
def delete_survey(survey_id):
    """刪除問卷"""
    try:
        survey = Survey.query.get_or_404(survey_id)
        # 先刪除所有關聯的回應
        Response.query.filter_by(survey_id=survey_id).delete()
        # 再刪除問卷本身
        db.session.delete(survey)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)  # 啟動服務器