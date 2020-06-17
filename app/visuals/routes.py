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
    cur.execute("select CONCAT(\"GGG_\", CHROM), starting_position_POS, ending_position_ALT from groc_svs_summary where WLI='1'")
    groc_fetch_data = cur.fetchall()

    pos = 2
    for var in groc_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    # cur = mysql.connection.cursor()
    # cur.execute("select starting_position, ending_position, starting_position from wli_dels_longranger_chr12")
    # wli_dels_fetch_data = cur.fetchall()
    #
    # pos = 2
    # for var in wli_dels_fetch_data:
    #     source_list = list(var[1:3])
    #     target_list = list(var[0:3])
    #     for i in range(len(source_list)):
    #         target_list.insert(i + pos, source_list[i])
    #         data.append(target_list)
    #
    # cur.close()
    print("gwlidelgwlidelgwlidelgwlidelgwlidelgwlidelgwlidelgwlidel", data)
    return render_template('gwlidel.html', title='HRDP', data=data)

@visuals.route('/wli/large')
def gwlilarge():
    data = []

    # cur = mysql.connection.cursor()
    # cur.execute("select * from sv_research_test_schema.groc_chr12")
    # groc_fetch_data = cur.fetchall()
    #
    # pos = 2
    # for var in groc_fetch_data:
    #     source_list = list(var[1:3])
    #     target_list = list(var[0:3])
    #     for i in range(len(source_list)):
    #         target_list.insert(i + pos, source_list[i])
    #         data.append(target_list)
    #
    # cur.close()

    cur = mysql.connection.cursor()
    cur.execute(
        "select cast(substring_index(a.CHROM, 'chr', -1) as unsigned) as chr, CASE WHEN ALT LIKE '\<%' THEN CAST(substring_index(substring_index(a.INFO, ';', 1), '=', -1) AS unsigned) ELSE CAST(substring_index(substring_index(substring_index(ALT, ':', -1), '[', 1), ']', 1) AS unsigned) END AS END, POS from tsv_wli_dels_longranger a where cast(substring_index(a.CHROM, 'chr', -1) as unsigned) != 0 order by chr")
    wli_dels_fetch_data = cur.fetchall()

    pos = 2
    for var in wli_dels_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    print("wlilongrangerwlilongrangerwlilongrangerwlilongrangerwlilongrangerwlilongrangerwlilongrangerwlilongranger", data)

    return render_template('gwlilarge.html', title='HRDP', data=data)

@visuals.route('/wmi/dels')
def gwmidel():
    data = []

    cur = mysql.connection.cursor()
    cur.execute("select CONCAT(\"GGG_\", CHROM), starting_position_POS, ending_position_ALT from groc_svs_summary where WMI='1'")
    groc_fetch_data = cur.fetchall()

    pos = 2
    for var in groc_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()

    # cur = mysql.connection.cursor()
    # cur.execute("select cast(substring_index(a.CHROM, 'chr', -1) as unsigned) as chr, CASE WHEN ALT LIKE '\<%' THEN CAST(substring_index(substring_index(a.INFO, ';', 1), '=', -1) AS unsigned) ELSE CAST(substring_index(substring_index(substring_index(ALT, ':', -1), '[', 1), ']', 1) AS unsigned) END AS END, POS from tsv_wmi_dels_longranger a where cast(substring_index(a.CHROM, 'chr', -1) as unsigned) != 0 order by chr")
    # wmi_dels_fetch_data = cur.fetchall()
    #
    #
    # pos = 2
    # for var in wmi_dels_fetch_data:
    #     source_list = list(var[1:3])
    #     target_list = list(var[0:3])
    #     for i in range(len(source_list)):
    #         target_list.insert(i + pos, source_list[i])
    #         data.append(target_list)
    #
    # # print(data)
    # cur.close()

    print("gwmidelgwmidelgwmidelgwmidelgwmidelgwmidelgwmidelgwmidelgwmidelgwmidelgwmidelgwmidelgwmidelgwmidel", data)


    return render_template('gwmidel.html', title='HRDP', data=data)

@visuals.route('/wmi/large')
def gwmilarge():
    data = []

    cur = mysql.connection.cursor()
    cur.execute("select cast(substring_index(a.CHROM, 'chr', -1) as unsigned) as chr, CASE WHEN ALT LIKE '\<%' THEN CAST(substring_index(substring_index(a.INFO, ';', 1), '=', -1) AS unsigned) ELSE CAST(substring_index(substring_index(substring_index(ALT, ':', -1), '[', 1), ']', 1) AS unsigned) END AS END, POS from tsv_wmi_dels_longranger a where cast(substring_index(a.CHROM, 'chr', -1) as unsigned) != 0 order by chr")
    groc_fetch_data = cur.fetchall()

    pos = 2
    for var in groc_fetch_data:
        source_list = list(var[1:3])
        target_list = list(var[0:3])
        for i in range(len(source_list)):
            target_list.insert(i + pos, source_list[i])
            data.append(target_list)

    cur.close()
    print("wmilongrangerwmilongrangerwmilongrangerwmilongrangerwmilongrangerwmilongrangerwmilongrangerwmilongrangerwmilongranger", data)
    # cur = mysql.connection.cursor()
    # cur.execute("select a.CHROM, CASE WHEN ALT LIKE '\<%' THEN substring_index(substring_index(a.INFO, ';', 1), '=', -1) ELSE substring_index(substring_index(substring_index(ALT, ':', -1), '[', 1), ']', 1) END AS END, POS from tsv_wli_dels_longranger a")
    # wli_dels_fetch_data = cur.fetchall()
    #
    # pos = 2
    # for var in wli_dels_fetch_data:
    #     source_list = list(var[1:3])
    #     target_list = list(var[0:3])
    #     for i in range(len(source_list)):
    #         target_list.insert(i + pos, source_list[i])
    #         data.append(target_list)
    #
    # cur.close()
    # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", data)

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
