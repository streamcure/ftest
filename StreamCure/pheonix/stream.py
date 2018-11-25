from flask import *
import MySQLdb
from flask.globals import request, session

con=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306,db='mj')
cmd=con.cursor()

sc=Flask(__name__)
sc.secret_key='k'
@sc.route('/')
def main():
    return render_template('index.html')

@sc.route('/lgn')
def lgn():
    return render_template('Login.html')


@sc.route('/Dctrreglink')
def Dctrreglink():
    cmd.execute("select * from department")
    result = cmd.fetchall()
    return render_template('Dctrreg.html',data=result)
@sc.route('/deptreglink',methods=["GET","POST"])
def deptreglink():
    return render_template('deptreg.html')
@sc.route('/Schedulelink')
def Schedulelink():
    cmd.execute("select * from doctorreg")
    result = cmd.fetchall()
    return render_template('Schedule.html',data=result)

@sc.route('/ad')
def ad():
    return render_template('adminhome.html')

@sc.route('/insertdoc',methods=['POST','GET'])
def insertdoc():
    name = request.form['txtdname']
    gender = request.form['radio']
    contctno = request.form['txtcontno']
    aadhaarno = request.form['txtaadhaarno']
    meritalstatus=request.form['mradio']
    address = request.form['txtaddress']
    contactaddress = request.form['txtcontactaddress']
    qualification = request.form['txtqual']
    specialization=request.form['txtspecialization']
    experience = request.form["txtexprns"]
    dateofjoining=request.form['txtdateofjoining']
    email = request.form['txtemail']
    Dname=request.form.get('selectdept')


    cmd.execute("insert into doctorreg values(null,'" + name + "','" + gender + "',"+ contctno +","+aadhaarno+",'"+meritalstatus+"','"+address +"','"+contactaddress+"', '"+qualification+"','"+specialization+"'"+experience+",'"+dateofjoining+"','"+email+"','"+str(Dname)+"')")
    con.commit()
    return '''<script>alert('Successfully inserted');window.location='/Dctrreglink'</script>'''


@sc.route('/appointmentlink')
def appointmentlink():
    return render_template('appointment.html')



@sc.route('/add')
def add():
    return render_template('adminhome.html')

@sc.route('/billlink')
def billlink():
    return render_template('bill.html')




@sc.route('/login',methods=['POST','GET'])
def login():
    username=request.form['txtusername']
    password=request.form['txtpwd']

    #print(username)
    cmd.execute("select * from login where username='"+username+"' and password='"+password+"'")
    re=cmd.fetchone()
    if re is None:
        return ''' <script> alert("Invalid username or password");window.location='/login' </script>'''
    elif re[2]=='admin':

        return render_template('adminhome.html')
    elif re[2]=='doctor':
        return render_template('dl.html')
    else:
        return ''' <script> alert("Invalid username or password");window.location='/login' </script> '''

@sc.route('/viewappointmentlink')
def viewappointmentlink():

    return render_template('viewappointment.html')


@sc.route('/viewdl')
def viewdl():
    return render_template('dl.html')



@sc.route('/prescriptionlink')
def prescriptionlink():
    return render_template('prescription.html')

@sc.route('/viewmedicalstatuslink')
def viewmedicalstatuslink():
   return render_template('MedicalStatus.html')




@sc.route('/depreg',methods=['POST','GET'])
def depreg():
    deptname=request.form['txtname']
    txthod=request.form['txthod']


    cmd.execute("insert into department values(null,'"+deptname+"','"+txthod+"')")
    con.commit()
    return '''<script>alert('Successfully inserted');window.location='/selectdep'</script>'''

# @sc.route('/depreg',methods=['POST','GET'])
#
# def appointment():
#     name=request.form['txtname']
#     txthod=request.form['txthod']
#
#
#     cmd.execute("insert into department values(null,'"+deptname+"','"+txthod+"')")
#     con.commit()
#     return '''<script>alert('Successfully inserted');window.location='/selectdep'</script>'''



@sc.route('/insertschedule',methods=['POST','GET'])
def insertschedule():
    name = request.form['selectdname']
    day = request.form['selectday']
    frmtime = request.form['txtfrom']
    totime = request.form['txtto']


    cmd.execute("insert into schedule values(null,'" + name + "','" + day + "','"+ frmtime +"','"+totime +"')")
    con.commit()
    return '''<script>alert('Successfully scheduled');window.location='/add'</script>'''


@sc.route('/insertbill',methods=['POST','GET'])
def insertbill():
    docname = request.form['txtdoc']
    pname = request.form['txtpat']
    amount = request.form['txtconsult']


    cmd.execute("insert into bill values(null,'" + docname + "','" + pname + "','"+ amount + "')")
    con.commit()
    return '''<script>alert('Successfully inserted');window.location='/add'</script>'''



@sc.route('/selectdep')
def selectdep():

    cmd.execute("select * from department")
    result=cmd.fetchall()
    return render_template('viewdep.html',data=result)


@sc.route('/delete',methods=['POST','GET'])
def delete():

    id=request.args.get('id')

    cmd.execute("delete from department where dpid="+str(id)+"")
    cmd.execute("select * from department")
    result=cmd.fetchall()
    con.commit()
    return render_template('viewdep.html',data=result)



@sc.route('/insertpresc',methods=['POST','GET'])
def insertpresc():
    name = request.form['txtptnnm']
    prescrp = request.form['txtpres']


    cmd.execute("insert into prescription values(null,'" + name + "','" + prescrp +"')")
    con.commit()
    return '''<script>alert('Successfully inserted');window.location='/viewdl'</script>'''


@sc.route('/signup',methods=['GET'])
def signup():
    name=request.args.get('name')


@sc.route('/login1',methods=['POST','GET'])
def login1():
    un=request.args.get('uname')
    pwd=request.args.get('password')
    cmd.execute("select * from login where username='" + un + "' and password='" + pwd + "' and type='user'")
    re = cmd.fetchone()
    if re is None:
        reslt={"task":"Failed"}
        return jsonify(reslt)
    else:
        cmd.execute("select pid from patientreg where email='"+un+"'")
        s=cmd.fetchone()
        reslt = {"task": s[0]}
        return jsonify(reslt)


@sc.route('/patientreg',methods=['POST','GET'])
def patientreg():
    try:
        name=request.args.get('name')
        address=request.args.get('address')
        email=request.args.get('email')
        mobile=request.args.get('mobileno')
        aadhaar=request.args.get('aadhaarno')
        pwd=request.args.get('password')
        cmd.execute("insert into patientreg values (Null,'"+name+"','"+address+"','"+email+"','"+mobile+"','"+aadhaar+"')")
        cmd.execute("insert into login values('"+email+"','"+pwd+"','user')")
        con.commit()

        reslt = {"task": "ok"}
        return jsonify(reslt)
    except Exception as e:
        print(str(e))
        reslt = {"task": "failed"}
        return jsonify(reslt)

@sc.route('/personaldetails',methods=['POST','GET'])
def personaldetails():

        pid=request.args.get('pid')

        cmd.execute("select * from patientreg where pid='"+pid+"'")
        rowheader=[x[0] for x in cmd.description]
        jsondata=[]
        re=cmd.fetchall()
        for r in re:
            jsondata.append(dict(zip(rowheader,r)))
        return jsonify(jsondata)


@sc.route('/viewbooking',methods=['POST','GET'])
def viewbooking():

        pid=request.args.get('pid')

        cmd.execute("select date,tokenno from appointment where pid='"+pid+"'")
        rowheader=[x[0] for x in cmd.description]
        jsondata=[]
        re=cmd.fetchall()
        for r in re:
            jsondata.append(dict(zip(rowheader,r)))
            print(jsondata)
        return jsonify(jsondata)

@sc.route('/selectdctr',methods=['POST','GET'])
def selectdctr():

        cmd.execute("select did,name from doctorreg")

        rowheader=[x[0] for x in cmd.description]
        jsondata=[]
        re=cmd.fetchall()
        for r in re:
            jsondata.append(dict(zip(rowheader,r)))
        print(jsondata)
        return jsonify(jsondata)

@sc.route('/scheduleview',methods=['POST','GET'])
def scheduleview():

        did=request.args.get('did')

        cmd.execute("select * from schedule where did='"+str(did)+"'")
        rowheader=[x[0] for x in cmd.description]
        jsondata=[]
        re=cmd.fetchall()
        for r in re:
            jsondata.append(dict(zip(rowheader,r)))
            print(jsondata)
        return jsonify(jsondata)


@sc.route('/insertappointment',methods=['POST','GET'])
def insertappointment():


        date=request.args.get('date')
        sid=request.args.get('sid')
        pid=request.args.get('pid')

        cmd.execute("select max(tokenno) from appointment where sid="+sid+" and date='"+date+"'")
        s=cmd.fetchone()
        tno=0
        try:
            tno=int(s[0])+1
        except:
            tno=1
        cmd.execute("insert into appointment values(null,'"+date+"','"+str(sid)+"','"+str(pid)+"','"+str(tno)+"')")
        con.commit()

        jsondata={"tid":str(tno)}
        return jsonify(jsondata)


if __name__=='__main__':
    sc.run(host="192.168.43.128",port=5000)

