from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.models import User, Post, CVocab, Strain, Animal, Tissue, Sequencing, Analysis
from app import db
from app import mysql


visuals = Blueprint('visuals', __name__)

@visuals.route('/wli/dels')
def gwlidel():
    data = []

    cur = mysql.connection.cursor()
    cur.execute("select * from groc_chr12")
    groc_fetch_data = cur.fetchall()

    pos = 2
    for var in groc_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("select chr, ending_position, starting_position from wli_dels_longranger_chr12")
    wli_dels_fetch_data = cur.fetchall()

    pos = 2
    for var in wli_dels_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    return render_template('gwlidel.html', title='HRDP', data=data)

@visuals.route('/wli/large')
def gwlilarge():
    data = []

    cur = mysql.connection.cursor()
    cur.execute("select * from groc_chr12")
    groc_fetch_data = cur.fetchall()

    pos = 2
    for var in groc_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("select a.id, a.ending_position, a.starting_position from sv_research_test_schema.wli_large_svs_longranger_chr12 a where a.starting_position < a.ending_position and abs(a.starting_position - a.ending_position) < 3000000")
    wli_dels_fetch_data = cur.fetchall()

    pos = 2
    for var in wli_dels_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    return render_template('gwlilarge.html', title='HRDP', data=data)

@visuals.route('/wmi/dels')
def gwmidel():
    data = []

    cur = mysql.connection.cursor()
    cur.execute("select * from groc_chr12")
    groc_fetch_data = cur.fetchall()

    pos = 2
    for var in groc_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("select chr, ending_position, starting_position from wmi_dels_longranger_chr12")
    wli_dels_fetch_data = cur.fetchall()

    pos = 2
    for var in wli_dels_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    return render_template('gwmidel.html', title='HRDP', data=data)

@visuals.route('/wmi/large')
def gwmilarge():
    data = []

    cur = mysql.connection.cursor()
    cur.execute("select * from groc_chr12")
    groc_fetch_data = cur.fetchall()

    pos = 2
    for var in groc_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("select a.id, a.ending_position, a.starting_position from sv_research_test_schema.wmi_large_svs_longranger_chr12 a where a.starting_position < a.ending_position and abs(a.starting_position - a.ending_position) < 5000000")
    wli_dels_fetch_data = cur.fetchall()

    pos = 2
    for var in wli_dels_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    return render_template('gwmilarge.html', title='HRDP', data=data)
