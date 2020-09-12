#import mysql.connector
#from mysql.connector import errorcode
import sqlite3
import uuid
import logging

def create_connection():
    try:
        db = sqlite3.connect('database.db')
        return db
    except:
        return None

def close_connection(db):
    db.close()


###############################
####### USER ACTIONS  ########
#############################
def signup(user_code, password):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        print('CREDENTIALS => ', user_code, password)
        cursor.execute("SELECT id, first_name, last_name, email, phone, role FROM Member WHERE user_code = ? AND pass = ?", (user_code, password))
        login_details = cursor.fetchone()
        close_connection(conn)
        return login_details
    except:
        close_connection(conn)
        return 0

def new_user(user_code, first_name, last_name, email, tel, password, role, prms_ary):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        #user_id = uuid.uuid4().int>>8
        user_id = uuid.uuid4().hex
        cursor.execute("INSERT INTO Member VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_id, user_code, first_name, last_name, email, tel, role, password))
        cursor.execute("INSERT INTO Permissions VALUES (?, ?, ?, ?, ?, ?)", (user_id, prms_ary[0], prms_ary[1], prms_ary[2], prms_ary[3], prms_ary[4]))
        conn.commit()
        response = user_id
        close_connection(conn)
        return response
    except Exception as e:
        logging.exception("Wrong user code or password.")

def get_user_with_permissions(state):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        if state == 'all':
            members = []
            cursor.execute("SELECT * FROM Member")
            _members = cursor.fetchall()
            for m in _members:
                _m = list(m)
                cursor.execute("SELECT * FROM Permissions WHERE member_id = ?", (m[0],))
                p = list(cursor.fetchone())
                _m.append(p)
                members.append(_m)
            close_connection(conn)
            return members
        else:
            return 'usao u else'
    except:
        close_connection(conn)
        return 'usao u except'

def get_user_without_permissions():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Member")
        _members = cursor.fetchall()
        members = []
        for _m in _members:
            members.append(list(_m))
        close_connection(conn)
        return members
    except Exception as e:
        logging.exception("Something went wrong with getting free members.")

def get_user(id):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Member WHERE id = ?", (id,))
        member = cursor.fetchone()
        close_connection(conn)
        return member
    except Exception as e:
        logging.exception("Something went wrong with getting free members.")

def update_user(user_id, first_name, last_name, email, tel, password, role):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Member SET first_name = ?, last_name = ?, email = ?, phone = ?, role = ?, pass = ? WHERE id = ?", (first_name, last_name, email, tel, password, role, user_id))
        conn.commit()
        close_connection(conn)
    except:
        close_connection(conn)
        return 0

def get_permissions(user_id):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Permissions WHERE member_id = ?", (user_id,))
        permissions = cursor.fetchone()
        close_connection(conn)
        return permissions
    except:
        close_connection(conn)
        return 0

def update_permissions(user_id, role_mm, team_all_mm, team_self_mm, task_revision, review_all_projects, task_list_management, project_self_management):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Permissions SET role_management = ?, team_all_management = ?, team_self_management = ?, task_revision = ?, review_all_projects = ?, task_list_management = ?, project_self_management = ? WHERE member_id = ?", (role_mm, team_all_mm, team_self_mm, task_revision, review_all_projects, task_list_management, project_self_management, user_id))
        conn.commit()
        close_connection(conn)
    except:
        close_connection(conn)
        return 0

def new_team(name, leader_id, active_project, members):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        team_id = uuid.uuid4().hex
        cursor.execute("INSERT INTO Team VALUES (?, ?, ?, ?)", (team_id, name, leader_id, active_project))
        for m in members:
            cursor.execute("INSERT INTO Member_team VALUES (?, ?)", (team_id, m))
        conn.commit()
        response = team_id
        close_connection(conn)
        return response
    except Exception as e:
        logging.exception("Something went wrong.")

def get_team(state):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        if state == 'all':
            cursor.execute("SELECT * FROM Team")
            _team = cursor.fetchall()
            team = []
            for _t in _team:
                team.append(list(_t))
            close_connection(conn)
            return team
        else:
            cursor.execute("SELECT * FROM Team WHERE id = ?", (state,))
            _team = cursor.fetchone()
            _team = list(_team)
            close_connection(conn)
            _members = get_team_members(state)
            _team.append(_members)
            return _team
    except:
        return 0

def get_team_by_leader(leader_id):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Team WHERE leader_id = ?", (leader_id,))
        team = list(cursor.fetchone())
        print('TEAM ==> ', team)
        close_connection(conn)
        return team
    except:
        close_connection(conn)
        return 'usao u except'

def get_project_by_member(member_id):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT team_id FROM Member_team WHERE member_id = ?", (member_id,))
        t = cursor.fetchone()
        cursor.execute("SELECT active_project FROM Team WHERE id = ?", (t[0],))
        p = cursor.fetchone()
        close_connection(conn)
        return p[0]
    except:
        close_connection(conn)
        return 'Ops nesto se dogodilo'

def get_team_members(team_id):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Member_team WHERE team_id = ?", (team_id,))
        _members = cursor.fetchall()
        m = []
        for _m in _members:
            cursor.execute("SELECT id, first_name, last_name, role FROM Member WHERE id = ?", (_m[1],))
            m.append(list(cursor.fetchone()))
        close_connection(conn)
        return m
    except:
        close_connection(conn)
        return 'usao u except'

def get_teamless_members():
    try:
        _m = get_user_without_permissions()
        conn = create_connection()
        cursor = conn.cursor()
        free = []
        for one in _m:
            cursor.execute("SELECT team_id FROM Member_team WHERE member_id = ?", (one[0],))
            check = cursor.fetchone()
            if not check:
                free.append(one)
        close_connection(conn)
        return free
    except Exception as e:
        logging.exception("Something went wrong with getting teamless members.")


def get_projects(state):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        if state == 'all':
            cursor.execute("SELECT * FROM Project_test")
            project_all = cursor.fetchall()
            #cursor.execute("SELECT * FROM Stage")
            #stage_all = cursor.fetchall()
            #cursor.execute("SELECT * FROM Golas")
            #goals_all = cursor.fetchall()
        else:
            project = []
            cursor.execute("SELECT project_id FROM Member_Project WHERE member_id = ?", (state,))
            _p = cursor.fetchall()
            #for p in _p:
            #    cursor.execute("SELECT * FROM Project WHERE id = ?", (p,))
            #    project.push(p)
        close_connection(conn)
        return project_all
    except:
        return 0

#def wrapper():
#    for s in stage_all:
#        for g in goals_all:
#            if s["id"] == g["stage_id"]
#            s
def new_project (team_id, title, client, description, customer_details, budget, budget_status, job_type, time_date_created, deadline):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        project_id = uuid.uuid4().hex
        cursor.execute("INSERT INTO Project_test VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (project_id, team_id, title, client, description, customer_details, budget, budget_status, job_type, time_date_created, deadline))
        cursor.execute("UPDATE Team SET active_project = ? WHERE id = ?", (project_id, team_id))
        conn.commit()
        response = project_id
        close_connection(conn)
        return response
    except Exception as e:
        logging.exception("Something went wrong.")

def new_stage (project_id, stage, description, resources, status, time_date_created, expected_time_of_finish):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        stage_id = uuid.uuid4().int>>8
        cursor.execute("INSERT INTO Stage VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (stage_id, project_id, stage, description, resources, status, time_date_created, expected_time_of_finish))
        conn.commit()
        response = stage_id
        close_connection(conn)
        return response
    except Exception as e:
        logging.exception("Something went wrong.")














###################################
####### PORTFOLIO ACTIONS  #######
#################################

def getAlbums(user_id):
    galleryDB = create_connection()
    cursor = galleryDB.cursor()
    cursor.execute("SELECT * FROM portfolio WHERE user_id = %s", (user_id,))
    albums = cursor.fetchall()
    photos = getPhotos(cursor, user_id)
    close_connection(galleryDB)
    return albums, photos

#   moras dodati tag ovdje
def newAlbum(user_id, title, sub_title, desc, location, category, model, camera, quote, quote_vis, head_img, images, date, time):
    galleryDB = create_connection()
    cursor = galleryDB.cursor()
    album_id = uuid.uuid1().int>>8
    cursor.execute("INSERT INTO portfolio VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (album_id, title, sub_title, desc, location, category, model, camera, quote, quote_vis, head_img, date, time, user_id))
    for i in images:
        photo_id = uuid.uuid1().int>>8
        cursor.execute("INSERT INTO photographs VALUES (%s, %s, %s, %s, %s)", (photo_id, i[0], i[1], album_id, user_id))
    galleryDB.commit()
    close_connection(galleryDB)
    portfolio = getAlbums(user_id)
    return portfolio

#####################################
####### PHOTOGRAPHS ACTIONS  #######
###################################

def getPhotos(cursor, user_id):
    cursor.execute("SELECT * FROM photographs WHERE user_id = %s", (user_id,))
    photos = cursor.fetchall()
    return photos