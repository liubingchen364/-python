"""
论文搜索应用 - 使用 Serper API (Google 搜索)
"""

from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Serper API 密钥 - 替换成你自己的
SERPER_API_KEY = "1b5340257a00ef8ba607bba958ca813e63e0c1e4"  # 在这里填入你的 Serper API Key

PORT = int(os.environ.get('DEPLOY_RUN_PORT', 5000))


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search():
    """搜索 API - 使用 Serper"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': '请求数据为空'}), 400

        query = data.get('query', '').strip()
        count = data.get('count', 10)

        if not query:
            return jsonify({'error': '请输入搜索关键词'}), 400

        # 调用 Serper API
        url = "https://google.serper.dev/search"

        payload = {
            "q": f"{query} paper research",
            "num": count
        }

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            return jsonify({'error': '搜索服务暂时不可用'}), 500

        result = response.json()

        # 格式化结果
        results = []

        # Serper 返回的 organic 结果
        if 'organic' in result:
            for item in result['organic']:
                results.append({
                    'id': item.get('position', 0),
                    'title': item.get('title', '无标题'),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'summary': '',
                    'siteName': item.get('displayedLink', ''),
                    'publishTime': '',
                    'authorityLevel': 0,
                    'authorityDesc': '',
                })

        return jsonify({
            'success': True,
            'summary': '',
            'results': results,
            'total': len(results)
        })

    except Exception as e:
        print(f'搜索失败: {str(e)}')
        return jsonify({
            'error': '搜索失败，请稍后重试',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)