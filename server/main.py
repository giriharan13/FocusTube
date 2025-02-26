from flask import Flask,render_template,url_for,flash,redirect,request
from .forms import SearchForm
from .models import Search

from flask import Blueprint,render_template,jsonify
from flask_login import login_required,current_user
import requests
import os

main = Blueprint('main',__name__)




@main.route('/home',methods=["GET","POST"])
@main.route('/',methods=["GET","POST"])
@login_required
def home():
    current_user_id = current_user.id

    if not current_user_id:
        flash('You must be logged in to access this page.', 'warning')
        return redirect(url_for('auth.login'))

    form = SearchForm()
    if(form.validate_on_submit()):
        search = Search()
        search.query = form.query.data
        current_user.searches.append(search)
        search.save()
        return redirect(url_for("main.result",q=form.query.data))
    return render_template("home.html",form=form)

@main.route('/about',methods=['GET'])
def about():
    return render_template("about.html")


def get_result(query, pageToken):
    youtube_data_api_uri = f"https://www.googleapis.com/youtube/v3/search?key={os.environ['YOUTUBE_DATA_API_KEY']}&q={query}&type=video&part=snippet"
    if(pageToken):
        youtube_data_api_uri+=f"&pageToken={pageToken}"
    response = requests.get(youtube_data_api_uri , headers={"Accept":"application/json"})
    print(response.json())
    return response.json()

def extract_links(items):
    links = []
    for item in items:
        links.append(item["id"]["videoId"])
    return links

    

@main.route("/result")
@login_required
def result():
    search_query = request.args.get('q')
    page_token = request.args.get('pageToken')
    result = get_result(search_query,page_token)
    links = extract_links(result["items"])
    return render_template("result.html",links=links,total_results=result["pageInfo"]["totalResults"],results_per_page=result["pageInfo"]["resultsPerPage"],query=search_query,previous_page_token=result.get("prevPageToken"), next_page_token=result.get("nextPageToken"))

