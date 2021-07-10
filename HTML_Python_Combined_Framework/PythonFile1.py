import io
import warnings
from base64 import *
from datetime import datetime, timedelta

import PIL
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy
import pandas as pd
import yfinance
from flask import Flask, redirect, url_for, render_template, request, session, jsonify

warnings.filterwarnings("ignore")

print(str(datetime.now() - timedelta(days=1))[:10], str(datetime.now() + timedelta(days=1))[:10])
img = io.BytesIO()
app = Flask(__name__)
app.secret_key = "4D3%3j&f191lak2*ff"
app.permanent_session_lifetime = timedelta(minutes=10)
listkey = {"Sri": "Inside"}


@app.route("/")
def home():
    return render_template("HTMLFile1.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user_ = request.form["value"]
            password = request.form['pass']
            try:
                if listkey[user_] == password:

                    session["user"] = user_
                    return redirect(url_for("user"))
                else:
                    return render_template("Loginfile.html", invalid=True)
            except KeyError:
                return render_template("SignUp.html")
        except KeyError:
            ress = request.form["layout2"]
            return render_template("Loginfile.html", invalid=ress)
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("Loginfile.html", invalid=False)


@app.route("/user", methods=["GET", "POST"])
def user():
    if "user" in session:
        user_ = session["user"]
        return render_template("Loggedin.html", username=user_)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/stocks", methods=["GET", "POST"])
def stocks():
    if "user" in session:
        return render_template("Stock_Display.html", signed_in=True)
    return render_template("Stock_Display.html")


@app.route("/stocks/sender", methods=["GET", "POST"])
def stocks_sender():
    asks = ["Ticker", "Ticker2", "Ticker3"]
    ask2 = ["A", "B", "C"]
    if request.method == "POST":
        stock_val = {}
        for ask in asks:
            try:
                if datetime.now().weekday() > 4:
                    if datetime.now().weekday() == 5:
                        stock_val[ask2[asks.index(ask)]] = f'~{yfinance.Ticker(request.form[ask]).info["regularMarketPrice"]: .2f}'
                    elif datetime.now().weekday() == 6:
                        stock_val[ask2[asks.index(ask)]] = f'~{yfinance.Ticker(request.form[ask]).info["regularMarketPrice"]: .2f}'
                elif datetime.now().hour < 9:
                    stock_val[ask2[asks.index(ask)]] = f'~{yfinance.Ticker(request.form[ask]).info["regularMarketPrice"]: .2f}'

                elif datetime.now().hour == 9:
                    if datetime.now().minute < 30:
                        stock_val[ask2[asks.index(ask)]] = f'~{yfinance.Ticker(request.form[ask]).info["regularMarketPrice"]: .2f}'
                else:

                    stock_val[ask2[asks.index(ask)]] = f'~{yfinance.Ticker(request.form[ask]).info["regularMarketPrice"]}'
            except KeyError:
                stock_val[ask2[asks.index(ask)]] = '?'
        return jsonify(stock_val)
    return redirect(url_for("stocks"))


@app.route("/stocks/image/sender", methods=["GET", "POST"])
def create_stock():
    """
    Gets the historical data from yahoo finance

    :return: the bytes format of static/testsave.png (will be renamed soon)
    """
    global img
    print("Started")
    if request.method == "POST":
        fig, ax = plt.subplots(3, figsize=(10, 10))

        data: list = [request.form.get("Ticker"), request.form.get("Ticker2"), request.form.get("Ticker3")]
        for data_var in data:
            if data_var is "":
                del data[data.index(data_var)]
        print('Completed 1/3')
        if len(data) >= 1:
            for data_ in data:
                try:
                    if data_ == '':
                        continue

                    if type(ax) == numpy.ndarray:

                        self_ax = ax[data.index(data_)]
                    else:
                        self_ax = ax
                    print(data_)
                    df = yfinance.Ticker(data_).history(period='70d', threads=False)
                    moveAvgData = {"df_50": df["Close"].rolling(50).mean(),
                                   "df_200": df["Close"].rolling(200).mean(),
                                   "df_Y": df["Close"].rolling(365).mean()}
                    apdict = mpf.make_addplot(pd.DataFrame(moveAvgData), ax=self_ax)
                    self_ax.set_title(data_)
                    self_ax.tick_params(axis='x', labelsize=8, rotation=2)
                    a = mpf.plot(df,
                                 type='candle', style='yahoo', volume=False,
                                 addplot=apdict, warn_too_much_data=10000000,
                                 ax=self_ax)
                    fig.savefig("static/testsave.png")
                    # img = figure.print_png("static/testsave.png")
                    plt.close()
                    print(a, "Finalized")
                except TypeError as error:
                    print(str(error))
        else:
            fig.savefig("static/testsave.png")

        pil_img = PIL.Image.open("static/testsave.png", mode='r')
        img = io.BytesIO()
        pil_img.save(img, format="PNG")
        return jsonify(b64encode(img.getvalue()).decode('ascii'))
    return redirect(url_for("stocks"))


if __name__ == '__main__':
    app.run(host="localhost", port=9342, debug=True)
