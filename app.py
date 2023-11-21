from flask import Flask, render_template, request, redirect, url_for
import pdfkit
import json
from flask import make_response

import io
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    topic = request.form.get('topic')
    num_paragraphs = int(request.form.get('num_paragraphs'))
    main_bodies = []
    for i in range(1, num_paragraphs + 1):
        main_body_topic = request.form.get(f'main_body_{i}_topic')
        num_aspects = int(request.form.get(f'main_body_{i}_num_aspects'))
        aspects = []
        for j in range(1, num_aspects + 1):
            aspect = request.form.get(f'main_body_{i}_aspect_{j}')
            support = request.form.get(f'main_body_{i}_support_{j}')
            what_else = request.form.get(f'main_body_{i}_else_{j}')
            aspects.append({'aspect': aspect, 'support': support,'what_else': what_else})
        main_bodies.append({'topic': main_body_topic, 'aspects': aspects})
    return render_template('preview.html', topic=topic, main_bodies=main_bodies)

@app.route('/download_preview')
def download_preview():
    topic = request.args.get('topic')

    # 尝试从参数中解析 JSON 数据
    main_bodies_json = request.args.get('main_bodies')
    try:
        main_bodies = json.loads(main_bodies_json) if main_bodies_json else []
    except json.JSONDecodeError:
        main_bodies = []

    rendered = render_template('preview.html', topic=topic, main_bodies=main_bodies)

    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=preview.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)