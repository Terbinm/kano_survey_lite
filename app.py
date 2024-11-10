# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
from constants import KANO_SETTINGS, KANO_COLORS, KANO_TEXT_COLORS, KANO_BG_COLORS, KANO_DESCRIPTIONS
from models import db, Survey, Response, Question
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
    """取得啟用的問題清單"""
    return [q.to_dict() for q in Question.query.filter_by(active=True).order_by(Question.order).all()]


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
    # 取得所有問題（包括已停用的）
    all_questions = Question.query.all()
    questions_dict = {q.id: q for q in all_questions}

    # 取得所有回應
    responses = Response.query.all()

    # 初始化結果統計
    results = {}
    categories = ['A', 'O', 'M', 'I', 'R', 'Q']

    # 為所有問題初始化計數器
    for question_id in questions_dict.keys():
        results[question_id] = {cat: 0 for cat in categories}

    # 統計每個問題的各分類數量
    for response in responses:
        if response.question_id in results:
            results[response.question_id][response.kano_category] += 1

    return render_template('results.html',
                           results=results,
                           questions=questions_dict,
                           categories=categories)


@app.route('/responses')
def view_responses():
    """查看個別回應"""
    surveys = Survey.query.order_by(Survey.timestamp.desc()).all()

    # 取得所有問題（包括已停用的）
    all_questions = Question.query.all()
    questions_dict = {q.id: q for q in all_questions}

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
                           questions=questions_dict,
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


@app.route('/questions/manage')
def manage_questions():
    """問題管理頁面"""
    questions = Question.query.order_by(Question.order).all()
    return render_template('manage_questions.html', questions=questions)

@app.route('/questions/bulk-import', methods=['POST'])
def bulk_import_questions():
    """批量導入問題"""
    try:
        content = request.form.get('content', '').strip()
        if not content:
            return jsonify({'status': 'error', 'message': '請提供問題內容'}), 400

        # 刪除現有問題
        if request.form.get('clear_existing') == 'true':
            Question.query.delete()

        # 處理每一行問題
        order = Question.query.count()  # 從現有問題數量開始計數
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):  # 跳過空行和註解
                continue

            # 分割正向和反向問題
            parts = line.split(',', 1)
            if len(parts) != 2:
                continue

            positive, negative = parts[0].strip(), parts[1].strip()
            if positive.endswith(';'):  # 移除可能的分號
                positive = positive[:-1].strip()
            if negative.endswith(';'):
                negative = negative[:-1].strip()

            # 創建新問題
            question = Question(
                positive=positive,
                negative=negative,
                order=order
            )
            db.session.add(question)
            order += 1

        db.session.commit()
        return jsonify({'status': 'success', 'message': '問題導入成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """更新單個問題"""
    try:
        question = Question.query.get_or_404(question_id)
        data = request.get_json()

        if 'positive' in data:
            question.positive = data['positive']
        if 'negative' in data:
            question.negative = data['negative']
        if 'order' in data:
            question.order = data['order']
        if 'active' in data:
            question.active = data['active']

        db.session.commit()
        return jsonify({'status': 'success', 'data': question.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """刪除問題"""
    try:
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.context_processor
def utility_processor():
    """提供模板使用的工具函數"""
    return {
        'kano_settings': KANO_SETTINGS,
        'kano_colors': KANO_COLORS,
        'kano_text_colors': KANO_TEXT_COLORS,
        'kano_bg_colors': KANO_BG_COLORS,
        'kano_descriptions': KANO_DESCRIPTIONS
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)  # 啟動服務器