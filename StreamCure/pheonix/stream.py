from flask import *
import MySQLdb
from flask.globals import request, session

con=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306,db='mj')
cmd=con.cursor()

sc=Flask(__name__)
sc.secret_key='k'
@sc.route('/')
def main():
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
    address = request.form['txtaddress']
    qualification = request.form['txtqual']
    experience = request.form["txtexprns"]
    email = request.form['txtemail']
    uname = request.form['txtuname']
    Dname=request.form.get('selectdept')


    cmd.execute("insert into doctorreg values(null,'" + name + "','" + gender + "',"+ contctno +",'"+address +"', '"+qualification+"',"+experience+",'"+email+"','"+uname+"','"+str(Dname)+"')")
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

if __name__=='__main__':
    sc.run(debug=True)

