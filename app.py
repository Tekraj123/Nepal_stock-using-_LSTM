# import os 
# import sys
# from src.exception import CustomException
# from src.pipeline.model_predict import predictionPipeline 
# from flask import Flask,render_template,request


# app = Flask(__name__) 
# @app.route("/")
# def index():
#     return render_template('index.html')

# @app.route("/prediction",methods=['GET','POST'])
# def  predict():
#     if request.method=='GET':
#         return render_template('index.html')

#     else:
#         symbol=request.form.get('symbol')
#         prediction=predictionPipeline(symbol)
#         stock_price=prediction.predict()

#         return render_template ("",stock_value=stock_price)



# if __name__=="__main__":
#     app.run(host="0.0.0.0")

    










# import os
# import sys
# from src.exception import CustomException
# from src.pipeline.model_predict import predictionPipeline

# from flask import Flask, render_template, request

# app = Flask(__name__)


# @app.route("/")
# def index():
#     return render_template('index.html')


# @app.route("/prediction", methods=['GET', 'POST'])
# def predict():
#     if request.method == 'GET':
#         return render_template('index.html')

#     else:
#         symbol = request.form.get('symbol')
#         prediction = predictionPipeline(symbol)
#         stock_price = prediction.predict()

#         # stock_price is expected to be a dict like:
#         # {"Day 1": 1450.20, "Day 2": 1462.50, ..., "Day 7": 1489.75}

#         return render_template(
#             "result.html",
#             stock_value=stock_price,
#             symbol=symbol.upper()
#         )


# # if __name__ == "__main__":
#     app.run(host="0.0.0.0")




import os
import sys
from src.exception import CustomException
from src.pipeline.model_predict import predictionPipeline

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/prediction", methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('index.html')

    else:
        symbol = request.form.get('symbol')
        print(f"\n>>> [DEBUG] symbol received: {repr(symbol)}")

        if not symbol:
            return "ERROR: No symbol received from form.", 400

        prediction = predictionPipeline(symbol)
        stock_price = prediction.predict()
        print(f">>> [DEBUG] stock_price: {repr(stock_price)}")

        if stock_price is None:
            return (
                f"ERROR: predict() returned None for symbol '{symbol}'. "
                "Check model_predict.py — predict() must return a dict.",
                500
            )

        # Convert numpy floats/arrays -> plain Python floats
        # so Jinja2 can format/round them without errors
        clean_prices = {
            key: float(val.item() if hasattr(val, 'item') else val)
            for key, val in stock_price.items()
        }
        print(f">>> [DEBUG] clean_prices: {clean_prices}")

        return render_template(
            "result.html",
            stock_value=clean_prices,
            symbol=symbol.upper()
        )




if __name__ == "__main__":
    app.run(host="0.0.0.0")