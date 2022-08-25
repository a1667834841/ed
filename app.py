from flask import Flask,jsonify,render_template
from flask import request
import json
import huan_an_bussiness
import comLogger

logger = comLogger.get_logger()


app = Flask(__name__)

result = {
    "code":0,# 0正常 1异常
    "data":{}
}

@app.route('/')
def hello_world():
    return 'hello world!'

# 登录解析
# @app.route('/login',methods=['POST'])
# def login():
#     res = json.loads(request.data)
#     login_api.huai_an_jxjy(User())
#     print(res)
    
#     return common_struct(res)


@app.route('/huan_an/exam',methods=['POST'])
def huan_an_exam():
   
    res = json.loads(request.data)
    logger.info("huan_an_exam 被访问,params  %s",res)
    print(res)
    years = str.split(res["years"],",")
    huan_an_bussiness.exam(user_name= res["userName"],password= res["password"], years=years)
    return common_struct('成功')

@app.route('/huan_an/exam/batch',methods=['POST'])
def huan_an_exam_batch():
    res = json.loads(request.data)
    logger.info("huan_an_exam_batch 被访问,params:  %s",res)
    print(res)
    for userInfo in res:
        huan_an_bussiness.exam(user_name= userInfo["userName"],password= userInfo["password"], years=userInfo["years"])
        logger.debug(userInfo["userName"]+"考试成功")
    return common_struct('成功')

@app.route('/huan_an/exam/form',methods=['POST'])
def huan_an_exam_form():
    
    print('huai_an,request.form:',request.form)
    huan_an_bussiness.exam(user_name= request.form["userName"],password= request.form["password"], years=request.form["years"])
    return common_struct('成功')


@app.route('/index',methods=['GET'])
def index():
    return render_template("exam.html")

@app.route('/form',methods=['GET'])
def form():
    return render_template("form.html")




def common_struct(data, success=True, msg='error'):
    if success:
        output =  {'data': data, 'code': 1, 'message': 'success'}
    else:
        output =  {'data': data, 'code': 0, 'message': msg}
    return jsonify(output)




if __name__ == '__main__':
    print('api server is running')
    # 添加日志模块，将日志写入到指定文件中，打印DEBUG级别以下日志
    app.debug = True
    # handler = logging.FileHandler('logs/flask.log', encoding='UTF-8')
    # handler.setLevel(logging.DEBUG)
    # logging_format = logging.Formatter("%(asctime)s flask %(levelname)s %(message)s")
    # handler.setFormatter(logging_format)
    # app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=5000,debug=True) 



