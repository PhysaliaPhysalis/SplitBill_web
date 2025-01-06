from flask import Flask, render_template, request, redirect, url_for
# render_template: 渲染 HTML 模板文件
# request: 获取客户端发送的数据，例如表单数据
# redirect: 实现页面跳转
# url_for: 生成路由地址

# 创建 Flask 应用
app = Flask(__name__)

# 全局变量存储账单
bills = []

class Bill:
    def __init__(self, sort, cost, payer, num_of_people, note):
        self.sort = sort
        self.cost = float(cost)
        self.payer = payer
        self.num_of_people = int(num_of_people)
        self.note = note

    def split(self):
        capitation = self.cost / self.num_of_people
        return round(capitation, 2)

    def __str__(self):
        return (f"类别: {self.sort}, 金额: {self.cost}, 付款人: {self.payer}, "
                f"均摊人数: {self.num_of_people}, 备注: {self.note}")

# 路由（Route）是指 URL（统一资源定位符）和后台代码逻辑之间的映射关系。它告诉 Web 应用程序，当用户访问某个特定的 URL 时，应该运行哪段代码或返回什么内容。

@app.route('/')  #当用户访问 /（根路径）时，运行 index() 函数。
def index():
    return render_template('index.html', bills=bills)

@app.route('/add', methods=['POST']) #当用户访问 /add 时，运行添加账单的函数。
def add_bill():
    sort = request.form.get('sort')
    cost = request.form.get('cost')
    payer = request.form.get('payer')
    num_of_people = request.form.get('num_of_people')
    note = request.form.get('note')

    new_bill = Bill(sort, cost, payer, num_of_people, note)
    bills.append(new_bill)
    return redirect(url_for('index'))


@app.route('/calculate') #当用户访问 /calculate 时，运行账单加总计算的函数。
def calculate():
    payer_dict = {}
    for bill in bills:
        capitation = bill.split()
        if bill.payer not in payer_dict:
            payer_dict[bill.payer] = 0
        payer_dict[bill.payer] += capitation
    return render_template('calculate.html', payer_dict=payer_dict)

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)