from flask import Flask, render_template, request
from flask_cors import CORS

from calculator import latexEval
from predictComp import expLatex

import latex2mathml.converter

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/imgdata/<data>', methods=['GET'])
def apiclientCall(data):
    print("iNside")
    finalVal = data.replace("SLASH", "/")
    print("canvas to flask called : ")
    return expLatex(finalVal)

@app.route('/cal/<data>', methods=['GET'])
def getCalValue(data):
    print("calculator called")
    finalVal = data.replace("FSLASH", "\\")
    finalVal = finalVal.replace("SLASH", "/")
    result = latexEval(finalVal)
    return str(result)

@app.route('/mathml/<equation>', methods=['GET'])
def getMathMlValue(equation):
    mathml_output = ""
    print("MathMl called")
    finalVal = equation.replace("FSLASH", "\\")
    finalVal = finalVal.replace("SLASH", "/")
    mathml_output = latex2mathml.converter.convert(finalVal)
    return mathml_output


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)