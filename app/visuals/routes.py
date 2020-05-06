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
    cur.execute("select starting_position, ending_position, starting_position from wli_dels_longranger_chr12")
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

    print(":::::::::::::::::::::::::::::::::", data)

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
    cur.execute("select starting_position, ending_position, starting_position from wmi_dels_longranger_chr12")
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
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", data)

    return render_template('gwmilarge.html', title='HRDP', data=data)

@visuals.route('/geoChart/large')
def geoChart():
    data = [
        ['City', 'Population', 'Area'],
        ['Rome', 2761477, 1285.31],
        ['Milan', 1324110, 181.76],
        ['Naples', 959574, 117.27],
        ['Turin', 907563, 130.17],
        ['Palermo', 655875, 158.9],
        ['Genoa', 607906, 243.60],
        ['Bologna', 380181, 140.7],
        ['Florence', 371282, 102.41],
        ['Fiumicino', 67370, 213.44],
        ['Anzio', 52192, 43.43],
        ['Ciampino', 38262, 11]
    ]
    return render_template('geochart.html', title='HRDP', data=data)
