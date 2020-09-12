from flask import Flask, jsonify, request, Response
from api import app
from api import db_connection as db
from api import operations as opr
import simplejson as json
from datetime import date, datetime



def error(status=500, text="An error happened"):
    return jsonify({"error": text}), status

@app.route('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    post_data = request.get_json()
    user_code = post_data.get('userCode')
    password = post_data.get('pass')
    user = db.signup(user_code, password)
    print('USER => ', user)
    if user == 0:
        return error()
    else:
        _p = db.get_permissions(user[0])
        user_permissions = {
            'rm': _p[1],
            'tm': _p[2],
            'pm': _p[3],
            'pmso': _p[4],
            'poa': _p[5]
        }
    return jsonify({
        'user' : user,
        'permissions' : user_permissions,
        'status': 'success'
    })

@app.route('/data/access-level=?<lvl>', methods=['GET'])
def handle_data_content(lvl):
    cases = {
            1: 'basic',
            2: 'overview',
            3: 'mid',
            4: 'advance',
            5: 'high'
        }
    func = cases.get(lvl, "Invalid index")
    func()

@app.route('/member', methods=['GET','POST'])
def handle_base_member(state):
    if request.method == 'GET':
        _members = db.get_user_with_permissions(state)
        members = []
        for _m in _members:
            m = {
                'id': _m[0],
                'name': _m[2] + ' ' + _m[3],
                'role': _m[6],
                'email': _m[4],
                'tel': _m[5],
                'permissions': {
                    'rm': _m[8][1],
                    'tm': _m[8][2],
                    'pm': _m[8][3],
                    'pmso': _m[8][4],
                    'poa': _m[8][5]
                }
            }
            members.append(m)
        return jsonify({
            'status': 'success',
            'members': members
        })
    elif request.method == 'POST':
        post_data = request.get_json()
        user_code = post_data.get('userCode')
        first_name = post_data.get('firstName')
        last_name = post_data.get('lastName')
        email = post_data.get('email')
        tel = post_data.get('tel')
        role = post_data.get('role')
        password = post_data.get('pass')
        prms_ary = post_data.get('memberPermissions')
        m = db.new_user(user_code, first_name, last_name, email, tel, password, role, prms_ary)
        if m:
            return jsonify ({
                'status': 'success',
                'member': m
            })
        else:
            return jsonify ({
                'status': 'unseccessful'
            })

@app.route('/team/member/free', methods=['GET'])
def handle_teamless_member():
    tl_members = db.get_free_members()
    if tl_members:
        return jsonify ({
            'status': 'success',
            'free_members': tl_members
        })
    else:
        return jsonify ({
            'status': 'unseccessful'
        })

@app.route('/team/<state>', methods=['GET','POST'])
def handle_base_team(state):
    if request.method == 'GET':
        if state == 'all':
            team = []
            _team = db.get_team(state)
            if _team:
                for _t in _team:
                    br = 0
                    _t.append(db.get_team_members(_t[0]))
                    t = {
                        'id': _t[0],
                        'name': _t[1],
                        'leaderId': _t[2],
                        'activeProject': _t[3],
                        'membersNum': br,
                        'members': []
                    }
                    for _m in _t[4]:
                        br = br + 1
                        t['membersNum'] = br
                        m = {
                            'id': _m[0],
                            'name': _m[1] + ' ' + _m[2],
                            'profileImg': 'profile_img.jpg',
                            'role': _m[3]
                        }
                        t['members'].append(m)
                    team.append(t)
            else:
                _members = db.get_teamless_members()
                members = []
                for _m in _members:
                    m = {
                        'id': _m[0],
                        'name': _m[2] + ' ' + _m[3],
                        'role': _m[6]
                    }
                    members.append(m)
                return jsonify({
                    'status': 'success',
                    'teams': 'none',
                    'members': members
                })
        else:
            print('ELSE')
        #portfolio = db.getAlbums(user_id)
        return jsonify({
            'status': 'success',
            'teams': team
        })
    elif request.method == 'POST':
        post_data = request.get_json()
        name = post_data.get('name')
        leader_id = post_data.get('leaderId')
        active_project = post_data.get('activeProject')
        members = post_data.get('members')
        t = db.new_team(name, leader_id, active_project, members)
        if t:
            return jsonify ({
                'status': 'success',
                'team': t
            })
        else:
            return jsonify ({
                'status': 'unseccessful'
            })

@app.route('/team/management/project/<member_id>', methods=['GET'])
def handle_project_id_request(member_id):
    project_id = db.get_project_by_member(member_id)
    return jsonify ({
            'status': 'success',
            'project': project_id
        })

@app.route('/team/management/leader/<leader_id>', methods=['GET'])
def handle_get_team_by_leader(leader_id):
    _t = db.get_team_by_leader(leader_id)
    members = db.get_team_members(_t[0])
    br = 0
    t = {
        'id': _t[0],
        'name': _t[1],
        'leaderId': _t[2],
        'activeProject': _t[3],
        'membersNum': br,
        'members': []
    }
    for _m in members:
        br = br + 1
        t['membersNum'] = br
        m = {
            'id': _m[0],
            'name': _m[1] + ' ' + _m[2],
            'img': 'profile_img.jpg',
            'role': _m[3]
        }
        t['members'].append(m)
    return jsonify ({
        'status': 'success',
        'team': t
    })

@app.route('/project/<state>', methods=['GET','POST'])
def handle_base_project(state):
    if request.method == 'GET':
        if state == 'all':
            _projects = db.get_projects(state)
            projects = []
            for _p in _projects:
                _team = db.get_team(_p[1])
                _leader = db.get_user(_team[2])
                p = {
                    'id': _p[0],
                    'title': _p[2],
                    'team': {
                        'id': _team[0],
                        'name': _team[1],
                        'leader': {
                            'id': _leader[0],
                            'name': str(_leader[2]) + ' ' + str(_leader[3]),
                            'profileImg': 'profile_img.jpg'
                        }
                    },
                    'client': _p[3],
                    'description': _p[4],
                    'customerDetails': _p[5],
                    'budget': _p[6],
                    'budgetStatus': _p[7],
                    'jobType': _p[8],
                    'created': _p[9],
                    'deadline': _p[10],
                }
                projects.append(p)
            return jsonify ({
                'status': 'success',
                'projects': projects
            })
        else:
            return 'Too bad for ya'
        return jsonify({
            'status': 'success',
            'portfolio': portfolio
        })
    elif request.method == 'POST':
        post_data = request.get_json()
        td = datetime.now()
        team_id = post_data.get('teamId')
        title = post_data.get('title')
        client = post_data.get('client')
        description = post_data.get('description')
        customer_details = post_data.get('customerDetails')
        budget = post_data.get('budget')
        budget_status = post_data.get('budgetStatus')
        job_type = post_data.get('jobType')
        time_date_created = td.strftime('%b') + ' ' + td.strftime('%d') + ' ' + td.strftime('%Y')
        deadline = post_data.get('deadline')
        p = db.new_project(team_id, title, client, description, customer_details, budget, budget_status, job_type, time_date_created, deadline)
        if p:
            return jsonify ({
                'status': 'success',
                'project': p
            })
        else:
            return jsonify ({
                'status': 'unseccessful'
            })


#galleryDB = mysql.connector.connect(user='u359858934_admin',passwd='Y8y7E}99txbE>V7',
#                                    host='81.16.28.1',
#                                    database='u359858934_galleryDB')

#id = uuid.uuid4().int>>8
#print("id: ", id)
#name = "Matea"
#last_name = "Radaković"
#user = "mr1204"
#password = "mateamatea"
#email = "mateaa98@hotmail.com"
#img = "23879HTR27094HFGQ308794HG025"

#cursor = galleryDB.cursor()
#cursor.execute("INSERT INTO user VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, name, last_name, user, password, email, img))

#galleryDB.commit()
#galleryDB.close()
