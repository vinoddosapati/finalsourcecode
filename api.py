from flask import Flask, render_template, request
from flask_cors import CORS

from calculator import latexEval
from predictComp import expLatex

import latex2mathml.converter

app = Flask(__name__)
CORS(app)

# render home page
@app.route('/')
def home():
    return render_template('index.html')

# api call to generate latex expression
@app.route('/imgdata/<data>', methods=['GET'])
def apiclientCall(data):
    print("iNside")
    finalVal = data.replace("SLASH", "/")
    print("canvas to flask called : ")
    return expLatex(finalVal)

# api call to calculate equation
@app.route('/cal/<data>', methods=['GET'])
def getCalValue(data):
    print("calculator called")
    finalVal = data.replace("FSLASH", "\\")
    finalVal = finalVal.replace("SLASH", "/")
    result = latexEval(finalVal)
    return str(result)

# api call to generate mathml for latex expression
# https://pypi.org/project/latex2mathml/
@app.route('/mathml/<equation>', methods=['GET'])
def getMathMlValue(equation):
    mathml_output = ""
    print("MathMl called")
    finalVal = equation.replace("FSLASH", "\\")
    finalVal = finalVal.replace("SLASH", "/")
    mathml_output = latex2mathml.converter.convert(finalVal)
    return mathml_output

# flask application hosting address
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)