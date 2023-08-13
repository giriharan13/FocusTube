from flask import Flask,render_template,url_for,flash,redirect
from forms import SearchForm
from bs4 import  BeautifulSoup
import requests
from youtubesearchpython import  VideosSearch


app = Flask(__name__)



app.config['SECRET_KEY'] = "1c56dc3f7255179e99c523583670239f";


# web scraping function
links = []
def webscrape(data):
    links.clear()
    res = VideosSearch(f'{data} youtube videos')
    print(res.result())
    for i in res.result()["result"]:
        print(i)
        links.append(f"https://www.youtube.com/embed/{i['link'].split('=')[-1]}")
    '''soup = BeautifulSoup(req,lxml)
    print(soup.prettify())'''




@app.route('/',methods=["GET","POST"])
def home():
    form = SearchForm()
    if(form.validate_on_submit()):
        flash("got input","success")
        webscrape(form.user_input.data)
        print(links)
        return redirect(url_for("result"))
    return render_template("home.html",form=form)

@app.route("/result")
def result():
    print(links)
    return render_template("result.html",links=links)


if __name__=='__main__':
    app.run(debug=True)