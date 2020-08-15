from flask import Flask, request, render_template, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from mastodon import Mastodon
import re, random, string
import html2text

BOT_NAME = '@ask_me_bot'
DOMAIN   = 'thu.closed.social'

WORK_URL = 'https://closed.social'

token = open('token.secret','r').read().strip('\n')
th = Mastodon(
    access_token = token,
    api_base_url = 'https://' + DOMAIN
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

h2t = html2text.HTML2Text()
h2t.ignore_links = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acct = db.Column(db.String(64))
    disp = db.Column(db.String(64))
    avat = db.Column(db.String(256))
    url  = db.Column(db.String(128))
    secr = db.Column(db.String(16))

    def __init__(self, acct):
        self.acct = acct

    def __repr__(self):
        return '@%s[%s]'%(self.acct, self.disp)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)
@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

@app.route('/askMe/')
def root():
    return app.send_static_file('ask.html')

@app.route('/askMe/inbox/', methods=['POST'])
def set_inbox():
    acct = request.form.get('username')
    if not re.match('[a-z0-9_]{1,30}(@[a-z\.-_]+)?', acct):
        return '无效的闭社id', 422

    r = th.conversations()
    for conv in r:
        status = conv.last_status
        account = status.account
        #print(account)
        if acct == account.acct:
            pt = h2t.handle(status.content).strip()

            x = re.findall('新建(\[[a-z]{1,32}\])?', pt)
            if not x:
                return '私信格式无效，请检查并重新发送', 422

            secr = x[0][1:-1] if x[0] else ''.join(random.choice(string.ascii_lowercase) for i in range(16))

            u = User.query.filter_by(acct=acct).first()
            if not u:
                u = User(acct)
                db.session.add(u)

            u.disp = account.display_name
            u.url  = account.url
            u.avat = account.avatar
            u.secr = secr
            db.session.commit()

            th.status_post(f"@{acct} 设置成功! 当前提问箱链接 {WORK_URL}/askMe/{acct}/{secr}\n(如需在微信等无链接预览的平台分享，建议先发给自己，点开，再点击分享到朋友圈等)", 
                    in_reply_to_id=status.id,
                    visibility='direct'
                    )

            return acct + '/' + secr
    
    return '未找到私信，请确认已发送且是最近发送', 404

@app.route('/askMe/<acct>/<secr>')
def inbox(acct, secr):
    u = User.query.filter_by(acct=acct, secr=secr).first()
    if not u:
        abort(404)
    
    return render_template('inbox.html', acct=u.acct, disp=u.disp, url=u.url, avat=u.avat)

if __name__ == '__main__':
    app.run(debug=True)