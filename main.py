# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import calendar
import random
import csv
from random import randint
from urllib.request import urlopen
import webbrowser
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from werkzeug.utils import secure_filename
from PIL import Image

import urllib.request
import urllib.parse

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error as mse


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="customer_relationship_emp"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

 
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM rt_retailer WHERE uname = %s AND pass = %s AND status=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('rt_home'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login.html',msg=msg)

@app.route('/login_emp', methods=['GET', 'POST'])
def login_emp():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM rt_employee WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('emp_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_emp.html',msg=msg)


@app.route('/login_cus', methods=['GET', 'POST'])
def login_cus():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM rt_customer WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login_cus.html',msg=msg)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login_admin.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    act=request.args.get("act")
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        
    
        
        mycursor = mydb.cursor()

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
    
        mycursor.execute("SELECT count(*) from rt_customer where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]
    
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM rt_customer")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO rt_customer(id,name,address,city,mobile,email,uname,pass,create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,address,city,mobile,email,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()            
            #print(mycursor.rowcount, "Registered Success")
            msg="sucess"
            #if mycursor.rowcount==1:
            return redirect(url_for('register',act='1'))
        else:
            msg='Already Exist'
    return render_template('register.html',msg=msg,act=act)

@app.route('/reg_retailer', methods=['GET', 'POST'])
def reg_retailer():
    msg=""
    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        
    
        
        mycursor = mydb.cursor()

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
    
        mycursor.execute("SELECT count(*) from rt_retailer where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]

        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM rt_retailer")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO rt_retailer(id,name,address,city,mobile,email,uname,pass,create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,address,city,mobile,email,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()            
            #print(mycursor.rowcount, "Registered Success")
            msg="sucess"
            #if mycursor.rowcount==1:
            return redirect(url_for('login'))
        else:
            msg='Already Exist'
    return render_template('reg_retailer.html',msg=msg)

@app.route('/add_emp', methods=['GET', 'POST'])
def add_emp():
    msg=""
    email=""
    mess=""
    uname=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        mobile=request.form['mobile']
        email=request.form['email']
        empid=request.form['empid']
        pass1=request.form['pass']
        
    
        
        

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
    
        mycursor.execute("SELECT count(*) from rt_employee where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]

        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM rt_employee")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO rt_employee(id,name,retailer,city,mobile,email,uname,pass,create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,uname,city,mobile,email,empid,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()
            mess="Employee Details - Employee ID: "+empid+", Password:"+pass1
            #print(mycursor.rowcount, "Registered Success")
            msg="success"
            
        else:
            msg='fail'


    mycursor.execute("SELECT * FROM rt_employee where retailer=%s",(uname,))
    data = mycursor.fetchall()
    if act=="del":
        did = request.args.get('did')
        mycursor.execute('delete from rt_employee WHERE id = %s', (did, ))
        mydb.commit()
        return redirect(url_for('add_emp'))
    
    return render_template('add_emp.html',msg=msg,data=data,mess=mess,email=email)


@app.route('/rt_home', methods=['GET', 'POST'])
def rt_home():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM rt_product where retailer=%s",(uname,))
    data2 = mycursor.fetchall()

    if act=="del":
        did = request.args.get('did')
        mycursor.execute("SELECT * FROM rt_product where id=%s",(did,))
        dd = mycursor.fetchone()
        os.remove("static/upload/"+dd[6])
        mycursor.execute('delete from rt_product WHERE id = %s', (did, ))
        mydb.commit()
        return redirect(url_for('rt_home'))
    
    return render_template('rt_home.html',data=data,uname=uname,data2=data2,act=act)


@app.route('/emp_home', methods=['GET', 'POST'])
def emp_home():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM rt_employee where uname=%s",(uname,))
    data = mycursor.fetchone()
    retailer=data[2]
    
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(retailer,))
    data1 = mycursor.fetchone()

    mycursor.execute("SELECT * FROM rt_cart c,rt_product p where c.pid=p.id && c.status=1 && p.retailer=%s && c.deliver_st=0",(retailer,))
    data2 = mycursor.fetchall()

    if act=="ok":
        rid = request.args.get('rid')
        mycursor.execute('update rt_cart set deliver_st=1 WHERE id = %s', (rid, ))
        mydb.commit()
        msg="ok"
    
    return render_template('emp_home.html',msg=msg,data=data,uname=uname,data2=data2,act=act)


@app.route('/emp_process', methods=['GET', 'POST'])
def emp_process():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM rt_employee where uname=%s",(uname,))
    data = mycursor.fetchone()
    retailer=data[2]
    
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(retailer,))
    data1 = mycursor.fetchone()

    mycursor.execute("SELECT * FROM rt_cart c,rt_product p where c.pid=p.id && c.status=1 && p.retailer=%s && c.deliver_st=1",(retailer,))
    data2 = mycursor.fetchall()
    
    return render_template('emp_process.html',data=data,uname=uname,data2=data2,act=act)

@app.route('/emp_inventory', methods=['GET', 'POST'])
def emp_inventory():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM rt_employee where uname=%s",(uname,))
    data = mycursor.fetchone()
    retailer=data[2]
    
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(retailer,))
    data1 = mycursor.fetchone()

    mycursor.execute("SELECT * FROM rt_product where retailer=%s order by status desc",(retailer,))
    data2 = mycursor.fetchall()


    
    return render_template('emp_inventory.html',data=data,uname=uname,data2=data2,act=act)

@app.route('/emp_cus', methods=['GET', 'POST'])
def emp_cus():
    msg=""
    data2=[]
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM rt_employee where uname=%s",(uname,))
    data = mycursor.fetchone()
    retailer=data[2]
    
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(retailer,))
    data1 = mycursor.fetchone()

    mycursor.execute("SELECT distinct(uname) FROM rt_cart where retailer=%s",(retailer,))
    dd = mycursor.fetchall()
    for ds in dd:
        mycursor.execute("SELECT * FROM rt_customer where uname=%s",(ds[0],))
        dd2 = mycursor.fetchone()
        data2.append(dd2)

    
    return render_template('emp_cus.html',data=data,uname=uname,data2=data2,act=act)

@app.route('/rt_sales', methods=['GET', 'POST'])
def rt_sales():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM rt_cart c,rt_product p where c.pid=p.id && c.status=1 && p.retailer=%s",(uname,))
    data2 = mycursor.fetchall()


    
    return render_template('rt_sales.html',data=data,uname=uname,data2=data2,act=act)

@app.route('/add_cat', methods=['GET', 'POST'])
def add_cat():
    msg=""
    act = request.args.get("act")
    fnn=""
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()
        
    if request.method=='POST':
        category=request.form['category']

        mycursor.execute("SELECT max(id)+1 FROM rt_category")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO rt_category(id,retailer,category) VALUES (%s, %s, %s)"
        val = (maxid,uname,category)
        mycursor.execute(sql, val)
        mydb.commit()            
        #print(mycursor.rowcount, "Registered Success")
        result="sucess"
        if mycursor.rowcount==1:
            return redirect(url_for('add_cat',act='1'))
        else:
            msg='Already Exist'

    if act=="del":
        did = request.args.get('did')
        mycursor.execute('delete from rt_category WHERE id = %s', (did, ))
        mydb.commit()
        return redirect(url_for('add_cat'))

    
        
    mycursor.execute("SELECT * FROM rt_category where retailer=%s",(uname,))
    data2 = mycursor.fetchall()
    
    return render_template('add_cat.html',msg=msg,uname=uname,data=data,data2=data2,act=act)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    msg=""
    act = request.args.get("act")
    fnn=""
    uname=""
    if 'username' in session:
        uname = session['username']
        
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM rt_category where retailer=%s",(uname,))
    data1 = mycursor.fetchall()

    
        
    if request.method=='POST':
        category=request.form['category']
        product=request.form['product']
        price=request.form['price']
        qty=request.form['qty']
        details=request.form['details']
        
    
        file = request.files['file']
        mycursor.execute("SELECT max(id)+1 FROM rt_product")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
            
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fn=file.filename
            fnn="P"+str(maxid)+fn  
            #fn1 = secure_filename(fn)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fnn))
                
        
        
        sql = "INSERT INTO rt_product(id,retailer,category,product,price,quantity,photo,details) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,uname,category,product,price,qty,fnn,details)
        mycursor.execute(sql, val)
        mydb.commit()            
        #print(mycursor.rowcount, "Registered Success")
        result="sucess"
        if mycursor.rowcount==1:
            return redirect(url_for('add_product',act='1'))
        else:
            msg='Already Exist'

    

    
        
    mycursor.execute("SELECT * FROM rt_product")
    data2 = mycursor.fetchall()
    
    return render_template('add_product.html',msg=msg,uname=uname,data=data,data1=data1,act=act)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    act=request.args.get("act")
    pid=request.args.get("pid")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM rt_product where id=%s",(pid,))
    data2 = mycursor.fetchone()

    if request.method=='POST':
        product=request.form['product']
        price=request.form['price']
        qty=request.form['qty']
        details=request.form['details']
        mycursor.execute("update rt_product set product=%s,price=%s,quantity=%s,details=%s where id=%s",(product,price,qty,details,pid))
        mydb.commit()

        mycursor.execute("SELECT * FROM rt_product where id=%s",(pid,))
        dd3 = mycursor.fetchone()
        if dd3[5]>dd3[9]:
            mycursor.execute("update rt_product set status=0 where id=%s",(pid,))
            mydb.commit()
    
        return redirect(url_for('rt_home'))
        
    
    return render_template('edit.html',data=data,uname=uname,data2=data2,act=act)



@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    cnt=0
    uname=""
    data=[]
    mess=""
    email=""
    st=""
    act = request.args.get('act')
    bt = request.args.get('bt')
    cat = request.args.get('cat')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_customer where uname=%s",(uname,))
    usr = mycursor.fetchone()

    mycursor.execute('SELECT count(*) FROM rt_cart WHERE uname=%s && status=0', (uname,))
    cart_n = mycursor.fetchone()[0]


    data2=[]
    mycursor.execute("SELECT * FROM rt_retailer")
    dtr1 = mycursor.fetchall()
    for dt1 in dtr1:
        dt2=[]
        mycursor.execute("SELECT * FROM rt_category where retailer=%s",(dt1[6],))
        dtr2 = mycursor.fetchall()
        dt2.append(dt1[1])
        dt2.append(dtr2)
        data2.append(dt2)

    cc=""
    if cat is None:
        cc=""
    else:
        cc="1"
    ####
    if act=="ct":
        rt=request.args.get("rt")
        mycursor.execute("SELECT * FROM rt_product where category=%s && retailer=%s",(cat,rt))
        data1 = mycursor.fetchall()

        for dd in data1:
            dt=[]
            dt.append(dd[0])
            dt.append(dd[1])
            dt.append(dd[2])
            dt.append(dd[3])
            dt.append(dd[4])
            dt.append(dd[5])
            dt.append(dd[6])
            dt.append(dd[7])
            dt.append(dd[8])
            dt.append(dd[9])

            mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(dd[1],))
            dd2 = mycursor.fetchone()
            dt.append(dd2[1])
            data.append(dt)
            
    ####
    elif bt=="1":
        getval=request.args.get("getval")
        cat="%"+getval+"%"
        prd="%"+getval+"%"
        det="%"+getval+"%"
        mycursor.execute("SELECT * FROM rt_product where category like %s || product like %s || details like %s",(cat,prd,det))
        data1 = mycursor.fetchall()

        for dd in data1:
            dt=[]
            dt.append(dd[0])
            dt.append(dd[1])
            dt.append(dd[2])
            dt.append(dd[3])
            dt.append(dd[4])
            dt.append(dd[5])
            dt.append(dd[6])
            dt.append(dd[7])
            dt.append(dd[8])
            dt.append(dd[9])

            mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(dd[1],))
            dd2 = mycursor.fetchone()
            dt.append(dd2[1])
            data.append(dt)

    else:
        mycursor.execute("SELECT * FROM rt_product order by rand() limit 0,12")
        data1 = mycursor.fetchall()

        for dd in data1:
            dt=[]
            dt.append(dd[0])
            dt.append(dd[1])
            dt.append(dd[2])
            dt.append(dd[3])
            dt.append(dd[4])
            dt.append(dd[5])
            dt.append(dd[6])
            dt.append(dd[7])
            dt.append(dd[8])
            dt.append(dd[9])

            mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(dd[1],))
            dd2 = mycursor.fetchone()
            dt.append(dd2[1])
            data.append(dt)
            
            

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    if act=="cart":
        pid = request.args.get('pid')
        mycursor.execute('SELECT count(*) FROM rt_cart WHERE uname=%s && pid = %s && status=0', (uname, pid))
        num = mycursor.fetchone()[0]

        mycursor.execute("SELECT * FROM rt_product where id=%s",(pid,))
        pdata = mycursor.fetchone()
        price=pdata[4]
        cat=pdata[3]
        retailer=pdata[1]
        if num==0:
            mycursor.execute("SELECT max(id)+1 FROM rt_cart")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                
            sql = "INSERT INTO rt_cart(id, uname, pid, status, rdate, price,category, retailer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, uname, pid, '0', rdate, price, cat, retailer)
            mycursor.execute(sql,val)
            mydb.commit()
            return redirect(url_for('userhome',act='mail',prid=str(pid)))

    mycursor.execute("SELECT count(*) FROM rt_cart where uname=%s && status=0",(uname,))
    cnt = mycursor.fetchone()[0]
    if cnt>0:
        msg="1"
    else:
        msg=""

    if act=="mail":
        prid=request.args.get("prid")
        mycursor.execute('SELECT count(*) FROM rt_product WHERE id=%s && status=0 && quantity<5',(prid,))
        nn = mycursor.fetchone()[0]
        if nn>0:
            st="1"
            mycursor.execute('SELECT * FROM rt_product WHERE id=%s && status=0 && quantity<5',(prid,))
            dd = mycursor.fetchone()

            mess="Product ID"+str(prid)+", Product:"+dd[3]+", Low Quantity "+str(dd[5])

            mycursor.execute("update rt_product set status=1 where id=%s ",(prid,))
            mydb.commit()
            
            mycursor.execute('SELECT * FROM rt_retailer WHERE uname=%s',(dd[1],))
            pd1 = mycursor.fetchone()
            email=pd1[5]
            print("mail sent "+email)
        
        
    
    return render_template('userhome.html',msg=msg,uname=uname,usr=usr,data=data,cnt=cnt,data2=data2,cart_n=cart_n,st=st,mess=mess,email=email)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    msg=""
    uname=""
    act=request.args.get("act")
    st=""
    pid=""
    did=""
    total=0
    amount=""
    pdata=[]
    pdata1=[]
    mess=""
    email=""
            
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    mycursor.execute("SELECT * FROM rt_customer where uname=%s",(uname,))
    usr = mycursor.fetchone()
    email=usr[5]
    name=usr[1]

    mycursor.execute('SELECT count(*) FROM rt_cart WHERE uname=%s && status=0', (uname,))
    cart_n = mycursor.fetchone()[0]

    mycursor.execute('SELECT count(*) FROM rt_cart WHERE uname=%s && status=0 && check_st=0', (uname,))
    cn = mycursor.fetchone()[0]
    if cn>0:
        mycursor.execute('SELECT sum(amount) FROM rt_cart WHERE uname=%s && status=0 && check_st=0', (uname,))
        total = mycursor.fetchone()[0]

    mycursor.execute("SELECT distinct(category) FROM rt_category")
    data2 = mycursor.fetchall()
    
    mycursor.execute("SELECT count(*) FROM rt_cart where uname=%s && status=0",(uname, ))
    cnt = mycursor.fetchone()[0]
    
    
    mycursor.execute('SELECT c.id,p.product,p.price,p.details,p.photo,c.rdate,c.quantity,c.amount,c.check_st,av_product FROM rt_cart c,rt_product p where c.pid=p.id and c.uname=%s and c.status=0', (uname, ))
    data = mycursor.fetchall()

    mycursor.execute("SELECT * FROM rt_cart where uname=%s && status=0",(uname, ))
    dr = mycursor.fetchall()

        
    i=0
    mul=0
    if request.method=='POST':
        ch=request.form['ch']
        
        qty=request.form.getlist('qty[]')
        rid=request.form.getlist('rid[]')

        if ch=="1":

            mycursor.execute("update rt_cart set check_st=0,av_product=0 where uname=%s && status=0",(uname, ))
            mydb.commit()
        
            for d1 in rid:
                user_qty=int(qty[i])

                
                
                mycursor.execute("SELECT price FROM rt_cart where id=%s",(d1, ))
                d2 = mycursor.fetchone()[0]
                mul=d2*user_qty

                mycursor.execute("SELECT * FROM rt_cart where id=%s",(d1, ))
                d3 = mycursor.fetchone()
                prid=d3[2]

                                
                mycursor.execute("SELECT * FROM rt_product where id=%s",(prid, ))
                pr = mycursor.fetchone()
                pr_qty=pr[5]
                
                

                rqty=pr[9]-d3[7]
                av_qty=pr_qty-rqty
                
                rqty1=rqty+user_qty
                mycursor.execute("update rt_product set required_qty=%s where id=%s ",(rqty1,prid))
                mydb.commit()

                if av_qty<user_qty:
                    mycursor.execute("update rt_cart set check_st=1,av_product=%s where id=%s && pid=%s",(av_qty,d1,prid))
                    mydb.commit()
                    
                
                mycursor.execute("update rt_cart set quantity=%s,amount=%s where id=%s ",(user_qty,mul,d1))
                mydb.commit()
                i+=1

                
            return redirect(url_for('cart',act='mail'))
        elif ch=="2":
            print("buy")
            if total>0:
                return redirect(url_for('cart',act='otp'))
            else:
                msg="2"
        elif ch=="3":
            print("check otp")
            otp=request.form['otp']
            mycursor.execute('SELECT * FROM rt_customer WHERE uname=%s',(uname,))
            r1 = mycursor.fetchone()
            if r1[9]==otp:
                return redirect(url_for('cart',act='yes'))
            else:
                msg="4"

    if act=="del":
        did=request.args.get("did")
        mycursor.execute('SELECT * FROM rt_cart WHERE id=%s',(did,))
        dd1 = mycursor.fetchone()
        pid1=dd1[2]
        mycursor.execute("update rt_product set required_qty=required_qty-%s where id=%s",(dd1[7],pid1))
        mydb.commit()
        mycursor.execute("delete from rt_cart where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('cart'))
        
    #send mail for products required  
    if act=="mail":
        print("mail")
        mycursor.execute('SELECT count(*) FROM rt_product WHERE required_qty>quantity && status=0')
        pn = mycursor.fetchone()[0]

        
        if pn>0:
            st="1"
           
            mycursor.execute('SELECT * FROM rt_product WHERE required_qty>quantity && status=0')
            pdata = mycursor.fetchall()

            for rr in pdata:
                dt=[]
                ret=rr[1]
                mycursor.execute('SELECT * FROM rt_retailer WHERE uname=%s',(ret,))
                pd1 = mycursor.fetchone()

                pname=rr[3]
                pid=rr[0]
                email=pd1[5]
                avp=rr[5]
                rp=rr[9]

                mess="Product ID: "+str(pid)+", Product: "+pname+", Availble only "+str(avp)+", Required "+str(rp)
                mycursor.execute("update rt_product set status=1 where id=%s ",(rr[0],))
                mydb.commit()
                    
                dt.append(mess)
                dt.append(email)
                pdata1.append(dt)
            

    if act=="otp":
        rn=randint(1000,9999)
        mess="OTP: "+str(rn)
        mycursor.execute("update rt_customer set otp=%s where uname=%s",(str(rn),uname))
        mydb.commit()
        
        
    #payment
    if act=="yes":

        mycursor.execute('SELECT * FROM rt_cart WHERE uname=%s && status=0 && check_st=0', (uname,))
        qc = mycursor.fetchall()
        for rc in qc:
            uq=rc[7]
            mycursor.execute("update rt_product set quantity=quantity-%s,required_qty=required_qty-%s where id=%s",(uq,uq,rc[2]))
            mydb.commit()
        
        mycursor.execute("SELECT max(id)+1 FROM rt_purchase")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        mycursor.execute('update rt_cart set status=1,bill_id=%s WHERE uname=%s && status=0 && check_st=0', (maxid, uname ))
        mydb.commit()

        sql = "INSERT INTO rt_purchase(id, uname, amount, rdate) VALUES (%s, %s, %s, %s)"
        val = (maxid, uname, total, rdate)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('cart', act='success'))
    if act=="success":
        mycursor.execute('SELECT amount FROM rt_purchase WHERE uname=%s order by id desc limit 0,1', (uname,))
        amount = mycursor.fetchone()[0]
        mess="Dear "+name+", Amount Rs."+str(amount)+" Purchased Success"
        msg="3"

    '''if request.method=='POST':
        amount=request.form['amount']
        print("test")
        return redirect(url_for('payment', amount=amt))'''
            
    return render_template('cart.html',msg=msg,uname=uname,usr=usr,data=data,cnt=cnt,data2=data2,cart_n=cart_n,total=total,act=act,pdata1=pdata1,st=st,mess=mess,email=email)



@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    uname=""
    act=request.args.get("act")
    data2=[]
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_customer where uname=%s",(uname,))
    usr = mycursor.fetchone()
    
    
    mycursor.execute("SELECT * FROM rt_purchase where uname=%s",(uname, ))
    data1=mycursor.fetchall()

    if act=="view":
        rid=request.args.get("rid")
        mycursor.execute("SELECT * FROM rt_cart where uname=%s &&bill_id=%s",(uname,rid))
        data2=mycursor.fetchall()

        
    return render_template('purchase.html',usr=usr,uname=uname,data1=data1,act=act,data2=data2)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    msg=""
    cnt=0
    uname=""
    data=[]
    mess=""
    email=""
    st=""
    act = request.args.get('act')
    bt = request.args.get('bt')
    cat = request.args.get('cat')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_customer where uname=%s",(uname,))
    usr = mycursor.fetchone()

    mycursor.execute("update rt_product set scount=0")
    mydb.commit()

    mycursor.execute("SELECT * FROM rt_cart where status=1")
    dd=mycursor.fetchall()
    for ds in dd:
        pid=ds[2]
        qty=ds[7]
        mycursor.execute("update rt_product set scount=scount+%s where id=%s",(qty,pid))
        mydb.commit()

    mycursor.execute("SELECT * FROM rt_product order by scount desc limit 0,12")
    data1 = mycursor.fetchall()

    for dd in data1:
        dt=[]
        dt.append(dd[0])
        dt.append(dd[1])
        dt.append(dd[2])
        dt.append(dd[3])
        dt.append(dd[4])
        dt.append(dd[5])
        dt.append(dd[6])
        dt.append(dd[7])
        dt.append(dd[8])
        dt.append(dd[9])

        mycursor.execute("SELECT * FROM rt_retailer where uname=%s",(dd[1],))
        dd2 = mycursor.fetchone()
        dt.append(dd2[1])
        data.append(dt)

    
    cname=[]
    dd2=[]
    mycursor.execute("SELECT * FROM rt_product where scount>0 order by scount desc limit 0,5")
    data11 = mycursor.fetchall()
    for ds11 in data11:
        cname.append(ds11[3])
        dd2.append(ds11[10])
    
    
    mycursor.execute("SELECT id,pid,status,price,quantity FROM rt_cart")
    data3 = mycursor.fetchall()
    with open('static/data.csv','w') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(col[0] for col in mycursor.description)
        for row in data3:
            writer.writerow(row)

    with open('static/data.csv') as input, open('static/data.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(col[0] for col in mycursor.description)
        for row in data3:
            if row or any(row) or any(field.strip() for field in row):
                writer.writerow(row)
            
    ##Decision Tree Algorithm

    df = pd.read_csv("static/data.csv")
    df.head()
    for col in df.columns:
        print(df[col].value_counts())
    #df= df.drop(['amount'],1)
    #df.head()
    
    from sklearn import preprocessing
    #le_status = preprocessing.LabelEncoder()
    #le_status.fit(['status','1'])
    #X[:,1] = le_status.transform(X[:,1])
    df = df.fillna(df.mean()) # updates the df
    df.corr()

    x = df.iloc[:,0:-1].values
    y = df.iloc[:,-1:].values

    x_train, x_test, y_train, y_test = train_test_split(x, y)

    print(x_train)
    print(y_train)

    print(len(x_train),len(x_test))

    dt_regressor = DecisionTreeRegressor()
    dt_regressor.fit(x_train, y_train)

    y_pred_dt = dt_regressor.predict(x_test)

    print(r2_score(y_test, y_pred_dt))
    print(mse(y_test, y_pred_dt)**0.5)
    #
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    cc=['green','blue','yellow','orange','pink']
    plt.bar(doc, values, color =cc,
            width = 0.6)
 
    mycursor.execute("SELECT sum(scount) FROM rt_product")
    getv = mycursor.fetchone()[0]
    gv=int(getv)
    plt.ylim((1,gv))
    plt.xlabel("Product")
    plt.ylabel("Sales Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    plt.xticks(rotation=20,size=8)
    plt.savefig('static/'+fn)
    
    plt.close()

    '''from sklearn.model_selection import train_test_split
    X_trainset, X_testset, y_trainset, y_testset = train_test_split(X, y, test_size=0.3, random_state=3)
    print(X_trainset.shape)
    print(y_trainset.shape)

    print(X_testset.shape)
    print(y_testset.shape)


    saleCount = DecisionTreeClassifier(criterion="entropy", max_depth = 4)
    saleCount # it shows the default parameters

    saleCount.fit(X_trainset,y_trainset)

    #prediction
    predTree = saleCount.predict(X_testset)
    print (predTree [0:5])
    print (y_testset [0:5])

    from sklearn import metrics
    import matplotlib.pyplot as plt
    print("DecisionTrees's Accuracy: ", metrics.accuracy_score(y_testset, predTree))'''


        

    return render_template('predict.html',usr=usr,uname=uname,data1=data1,act=act,data=data)


@app.route('/view', methods=['GET', 'POST'])
def view():
    uname=""
    amount=0
    if 'username' in session:
        uname = session['username']
    
    bid = request.args.get('bid')
    cursor = mydb.cursor()
    cursor.execute('SELECT c.id,p.product,p.price,p.detail,p.photo,c.rdate FROM rt_cart c,rt_product p where c.pid=p.id and c.bill_id=%s', (bid, ))
    data = cursor.fetchall()

    return render_template('view.html', data=data)



@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM rt_retailer")
    data = mycursor.fetchall()

    if act=="yes":
        did=request.args.get("did")
        mycursor.execute("update rt_retailer set status=1 where id=%s",(did,))
        mydb.commit()
        return redirect(url_for("admin"))
    return render_template('admin.html',data=data)

##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


