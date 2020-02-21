from flask import Flask, render_template, request, redirect
import base64
import hashlib
import pandas as pd

app = Flask(__name__)

def short(url):
    data_file = open('db.txt', "r")
    data_str = data_file.read()
    data_file.close()
    rows = data_str.split('\n')
    df_data = pd.DataFrame([] if len(rows)==1 else [row.split(', ') for row in rows[1:]], columns=['url', 'short_url'])
    list_url = df_data.index[df_data['url'] == url].tolist()
    if len(list_url)>0:
        return df_data.iloc[list_url[0]]['short_url']
    prime = 400651    
    d_id = len(df_data)
    real_id = d_id%prime
    short_url = base64.b64encode(hashlib.md5((str(real_id)).encode('utf-8')).digest(), altchars=b"-_")[:6].decode("utf-8")
    if d_id>=prime:
      rows[real_id+1] = url+', '+short_url
    else:
      rows.append(url+', '+short_url)
    db_file = open('db.txt', "w")
    db_file.write('\n'.join(rows))
    db_file.close()
    return short_url


@app.route('/', methods=['GET', 'POST'])
def main():
    try:
        if request.method == 'POST':
            url = request.form.get('url')
            return render_template('main.html', newUrl=short(url))
        return render_template('main.html')
    except:
        return '<span style="color:red;font-weight:bold;">System Error</span>'
@app.route("/<url_key>")
def redirect_to_url(url_key):
    try:
        data_file = open('db.txt', "r")
        data_str = data_file.read()
        data_file.close()
        rows = data_str.split('\n')
        df_data = pd.DataFrame([] if len(rows)==1 else [row.split(', ') for row in rows[1:]], columns=['url', 'short_url'])
        list_url = df_data.index[df_data['short_url'] == url_key].tolist()
        if len(list_url)==0:
            return '<span style="color:red;font-weight:bold;">Not Found</span>'
        return redirect(df_data.iloc[list_url[0]]['url'])
    except:
        return '<span style="color:red;font-weight:bold;">System Error</span>'

if __name__ == '__main__':
    app.debug = True
    app.run()