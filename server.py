from flask import Flask, render_template, request, redirect, session

import random
app=Flask(__name__)
app.secret_key='secret'

@app.route('/')
def ninjaGold():
    if 'gold' not in session:
        session['gold']=0
    if 'energy' not in session:
        session['energy']=100
    if 'myActivities' not in session:
        session['myActivities']=[]
    if 'building' not in session:
        session['building']=None
    if session['energy']<0:
        session['energy']=0
        session['myActivities'].append(['You have died. START OVER'])
        session['color']='red'
    if session['energy']>100:
        session['energy']=100
    return render_template('index.html')

@app.route("/reset")
def destroy_session():
    session.pop('energy')
    session.pop('gold')
    session.pop('myActivities')
    session.pop('building')
    return redirect("/")

@app.route('/process', methods=['POST'])
def process():
    session['winLose']=round(int(random.random()*100))

    if request.form['building']=='farm':
        if session['energy']==0:
            session['myActivities'].append(['You have died. START OVER'])
            return redirect ('/')
        else:
            session['color']='green'
            session['building']='farm'
            session['farmMoney']=round(int(random.random()*15+5))
            session['gold']+=session['farmMoney']
            session['farmEnergy']=round(int(random.random()*15+5))
            session['energy']-=session['farmEnergy']
            session['myActivities'].append(['Earned '+str(session['farmMoney'])+' gold doing your cowperson business! Yawn but so productive! Lost '+str(session['farmEnergy'])+'% of your soul energy charge from back-breaking work'])
            return redirect ('/')

    elif request.form['building']=='cave':
        if session['energy']==0:
            session['myActivities'].append(['You have died. START OVER'])
            return redirect ('/')
        else:
            session['color']='green'
            session['building']='cave'
            session['caveMoney']=round(int(random.random()*20+10))
            session['gold']+=session['caveMoney']
            session['caveEnergy']=round(int(random.random()*20+10))
            session['energy']-=session['caveEnergy']
            session['myActivities'].append(['Earned '+str(session['caveMoney'])+' gold mining hydrogen flouride. Your abs may be made of steel but your back is howling is pain. Lost '+str(session['caveEnergy'])+'% of your soul energy charge.'])
            return redirect ('/')

    elif request.form['building']=='house' and session['energy'] is not 0:
        if session['energy']==0:
            session['myActivities'].append('You have died. START OVER')
            return redirect ('/')
        else:
            session['color']='green'
            session['building']='house'
            session['houseMoney']=round(int(random.random()*2))
            session['gold']+=session['houseMoney']
            session['houseEnergy']=round(int(random.random()*20))
            session['energy']+=session['houseEnergy']
            session['myActivities'].append(['Family gave you an allowance of '+str(session['houseMoney'])+' gold. You feel loved! Re-energized ' +str(session['houseEnergy'])+'% of your soul energy charge.'])
            print(session)
            return redirect ('/')

    else:
        if session['energy']==0:
            session['myActivities'].append(['You have died. START OVER'])
            return redirect ('/')
        else:
            session['building']='casino'
            session['casinoMoney']=round(int(random.random()*15+5))
            session['gold']+=session['casinoMoney']
            session['casinoEnergy']=round(int(random.random()*15+5))
            session['energy']-=session['casinoEnergy']
            if session['winLose']%2==0:
                session['color']='green'
                session['myActivities'].append('You lucky bug! Won '+str(session['casinoMoney'])+' gold but lost '+str(session['casinoEnergy'])+'% of your soul charge for the sin.')
                return redirect('/')
            else:
                session['color']='red'
                session['myActivities'].append('Oof! You were served with $'+str(session['casinoMoney'])+' gold but lost '+str(session['casinoEnergy'])+'% of your soul charge for the sin.')
                return redirect ('/')

if __name__=="__main__":
    app.run(debug=True)