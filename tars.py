







from flask import Flask, Response

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False



@app.route('/sms_webhook')
def inbound():
    response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Touchdown, Bo Jackson!</Message>
</Response>"""
    return Response(response, content_type='text/xml')


if __name__ == '__main__':
    app.run(debug=True)