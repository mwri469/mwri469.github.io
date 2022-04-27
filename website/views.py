from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Stock
from . import db
import json
import finnhub

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        ticker = request.form.get('stock')
        num_shares = request.form.get('num_shares')
        b_price = request.form.get('b_price')
        if len(ticker) < 1:
            flash('Ticker is not valid', category='error')
        else:
            # Commit stock info to the database
            new_stock = Stock(ticker=ticker,
                              num_shares=num_shares,
                              user_id=current_user.id,
                              b_price=b_price)
            db.session.add(new_stock)
            db.session.commit()
            flash('Stock added', category='success')
    return render_template("home.html", user=current_user, get_price=get_price())

def get_price(ticker='AAPL'):
    finnhub_client = finnhub.Client(api_key="c9h8fjiad3iblo2fuab0")
    return finnhub_client.quote(ticker)

@views.route('/portfolio', methods=['GET'])
@login_required
def portfolio(get_price = get_price):
    return render_template("portfolio.html", get_price=get_price,user=current_user)

@views.route('/delete-stock', methods=['POST'])
def delete_stock():
    stock = json.loads(request.data)
    stockId = stock['stockId']
    stock = Stock.query.get(stockId)
    if stock:
        if stock.user_id == current_user.id:
            db.session.delete(stock)
            db.session.commit()

    return jsonify({})

@views.route('/get-price', methods=['GET'])
def get_stock_price():
    stock = json.loads(request.data)
    ticker = stock['ticker']
    stock = Stock.query.get(ticker)
    finnhub_client = finnhub.Client(api_key="c9h8fjiad3iblo2fuab0")
    if stock:
        if stock.user_id == current_user.id:
            return finnhub_client.quote(ticker)