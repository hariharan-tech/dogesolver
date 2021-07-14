from flask import Flask , render_template , request
import math , cmath
import datetime

app = Flask(__name__)

def sb(ti):
    if ti[0]=="l":
        vl=ti[1]
        vp=ti[1]/((3)**(1/2))
    else:
        vl = ti[1]*((3)**(1 / 2))
        vp=ti[1]
    ip=vp/ti[2]
    il=ip
    ipr=cmath.polar(ip)[0]
    ipa=(cmath.polar(ip)[1]*57.324)
    p=(3**(1/2))*(cmath.polar(vl)[0])*(cmath.polar(ip)[0])*(math.cos(abs(cmath.polar(ip)[1]-cmath.polar(vp)[1])))
    q=(3**(1/2))*(cmath.polar(vl)[0])*(cmath.polar(ip)[0])*(math.sin(abs(cmath.polar(ip)[1]-cmath.polar(vp)[1])))
    s=(p**2 + q**2 )**(1/2)
    pf=math.cos(cmath.polar(vp)[1]-cmath.polar(ip)[1])
    if (cmath.polar(ip)[1]) <0:
        pftxt=" lagging"
    elif (cmath.polar(ip)[1]) >=0:
        pftxt="leading"
    else:
        pftxt="unity"
    return (vl,vp,ip,ipr,ipa,p,q,s,pf,pftxt,il)
    

def db(ti):
    vp=vl=ti[1]
    ip=vp/ti[2]
    il=ip*(3**(1/2))
    ipr=cmath.polar(ip)[0]
    ipa=(cmath.polar(ip)[1]*57.324)
    p=(3**(1/2))*(cmath.polar(vp)[0])*(cmath.polar(il)[0])*(math.cos(abs(cmath.polar(il)[1]-cmath.polar(vp)[1])))
    q=(3**(1/2))*(cmath.polar(vp)[0])*(cmath.polar(il)[0])*(math.sin(abs(cmath.polar(il)[1]-cmath.polar(vp)[1])))
    s=(p**2 + q**2 )**(1/2)
    pf=math.cos(cmath.polar(vp)[1]-cmath.polar(ip)[1])
    if (cmath.polar(ip)[1]) <0:
        pftxt=" lagging"
    elif (cmath.polar(ip)[1]) >=0:
        pftxt="leading"
    else:
        pftxt="unity"
    return (vl,vp,ip,ipr,ipa,p,q,s,pf,pftxt,il)


@app.route('/')
def Homepage():
    return render_template("homepage.html")

@app.route('/threephase',methods=['GET','POST'])
def threephase():
    if request.method=='POST':
        ptype=request.form['p_type']
        v_type=request.form['v_type']
        v=complex(request.form['v'])
        imp1=complex(request.form['imp1'])
        imp2=complex(request.form['imp2'])
        imp3=complex(request.form['imp3'])
        if ptype in ["1","2"] and (imp1==imp2==imp3):
            if ptype=="1":
                ptype="Star Connected Balanced"
                ti=(v_type,v,imp1)
                res=sb(ti)
                if v_type=="l":
                    v_type="Line Voltage"
                else:
                    v_type="Phase Voltage"
            else:
                ptype="Delta Connected Balanced"
                ti=(v_type,v,imp1)
                res=db(ti)
                if v_type=="l":
                    v_type="Line Voltage"
                else:
                    v_type="Phase Voltage"
                # (vl,vp,ip,ipr,ipa,p,q,s,pf,pftxt)
            return render_template('threephase.html',ptype=ptype,v_type=v_type,vl=res[0],vp=res[1],imp1=imp1,imp2=imp2,imp3=imp3,ip=res[2],ipr=res[3],ipa=res[4],p=res[5],q=res[6],s=res[7],pf=res[8],pftxt=res[9],il=res[10])
        else:
            return render_template('threephase.html')
    else:
        return render_template('threephase.html')

def retcolor(l):
    d={
                "0":"black",
                "1":"brown",
                "2":"red",
                "3":"orange",
                "4":"yellow",
                "5":"green",
                "6":"blue",
                "7":"violet",
                "8":"gray",
                "9":"white",
                "-1":"gold",
                "-2":"silver",
                "+ or - 5%":"gold",
                "+ or - 10%":"silver",
                "+ or - 1%":"brown",
                "+ or - 2%":"red",
                "+ or - 0.5%":"green",
                "+ or - 0.25%":"blue",
                "+ or - 0.10%":"violet",
                "+ or - 0.05%":"gray"
            }
    if len(l) == 4:
        return ([d[l[0]],d[l[1]],d[l[2]],d[l[3]]])
    else:
        return ([d[l[0]],d[l[1]],d[l[2]],d[l[3]],d[l[4]]])


@app.route('/fourband',methods=['GET','POST'])
def resultfour():
    if request.method =='POST':
        fband=request.form['firstband']
        sband=request.form['secondband']
        m=int(request.form['multiplier'])
        t=request.form['tolerance']
        r=str(int(fband+sband)*((10)**(m)))+" "+t+" Ohms"
        rl=retcolor([fband,sband,str(m),t])
        return render_template("resistorfour.html",r=r,firstcolor=rl[0],secondcolor=rl[1],mcolor=rl[2],tcolor=rl[3])
    else:
        return render_template("resistorfour.html")


@app.route('/fiveband',methods=['GET','POST'])
def resultfive():
    if request.method =='POST':
        fband=request.form['firstband']
        sband=request.form['secondband']
        tband=request.form['thirdband']
        m=int(request.form['multiplier'])
        print(m)
        t=request.form['tolerance']
        r=str(int(fband+sband+tband)*((10)**(m)))+" "+t+" Ohms"
        rl=retcolor([fband,sband,tband,str(m),t])
        return render_template("resistorfive.html",r=r,firstcolor=rl[0],secondcolor=rl[1],thirdcolor=rl[2],mcolor=rl[3],tcolor=rl[4])
    else:
        return render_template("resistorfive.html")

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@app.route('/astabletimer',methods=['GET','POST'])
def timerastable():
    if request.method=='POST':
        r1=float(request.form['r1'])*1000
        r2=float(request.form['r2'])*1000
        c=float(request.form['c1'])*((10)**(int(request.form['unitc'])))
        ont=0.693*(r1+r2)*c
        offt=0.693*r2*c
        duty=ont/(ont+offt)
        return render_template("astabletimer.html",ont=str(round(ont,5))+" s",onf=str(round((1/ont),5))+" Hz",offt=str(round(offt,5))+" s",offf=str(round((1/offt),5))+" Hz",duty=str(round(duty,5)*100)+" %")
    else:
        return render_template("astabletimer.html")

if __name__ == "__main__":
    app.run(debug=True)