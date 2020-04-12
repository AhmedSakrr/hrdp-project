from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.models import CVocab, Strain, Animal, Tissue, Sequencing, Analysis
from app import db


data = Blueprint('data', __name__)

@data.route('/')
@data.route('/data/hrdp')
def data_hrdp():

    tableset = {}
    columnset = {}

    # strain
    # data list
    strains = Strain.query.all()
    # column list
    strain_columns = Strain.metadata.tables['Strain'].columns.keys()

    tableset['strain'] = strains
    columnset['strain'] = strain_columns

    # animal
    # data list
    animals = Animal.query.all()
    # column list
    animal_columns = Animal.metadata.tables['Animal'].columns.keys()

    tableset['animal'] = animals
    columnset['animal'] = animal_columns

    # tissue
    # data list
    tissues = Tissue.query.all()
    # column list
    tissue_columns = Tissue.metadata.tables['Tissue'].columns.keys()

    tableset['tissue'] = tissues
    columnset['tissue'] = tissue_columns

    # sequencing
    # data list
    sequencing_columns = Sequencing.metadata.tables['Sequencing'].columns.keys()
    sequencings = Sequencing.query.all()

    tableset['sequencing'] = sequencings
    columnset['sequencing'] = sequencing_columns

    # analysis
    # data list
    analyses = Analysis.query.all()
    # column list
    analysis_columns = Analysis.metadata.tables['Analysis'].columns.keys()

    tableset['analysis'] = analyses
    columnset['analysis'] = analysis_columns

    return render_template('data_hrdp.html', title='HRDP', tableset=tableset, columnset=columnset)


@data.route('/view')
def view():
    # sequencing
    # data list
    view_list = db.session.query(
        Sequencing.run_ID.label("RunID"),
        Sequencing.platform.label("Platform"),
        Sequencing.Raw_data_coverage.label("Raw_data_coverage"),
        Animal.strain_name.label("Rat_Strain"),
        Tissue.type.label("Tissue_name")).join(Tissue).join(Animal, Tissue.animal_ID == Animal.animal_name).all()

    view_column_list = ['RunID', 'Platform', 'Raw_data_coverage', 'Tissue_name', 'Rat_Strain']

    return render_template('view.html', title='Sequencing View', tableset=view_list, columnset=view_column_list)


@data.route("/data/view_detail/<string:run_id>")
def view_detail(run_id):

    tableset = {}
    columnset = {}

    # collecting columns for each table
    strain_columns = Strain.metadata.tables['Strain'].columns.keys()
    animal_columns = Animal.metadata.tables['Animal'].columns.keys()
    tissue_columns = Tissue.metadata.tables['Tissue'].columns.keys()
    sequencing_columns = Sequencing.metadata.tables['Sequencing'].columns.keys()
    analysis_columns = Analysis.metadata.tables['Analysis'].columns.keys()

    # collecting data from each table
    # sequencing
    sequencings = Sequencing.query.filter(Sequencing.run_ID == run_id).first()

    # tissue
    tissue_id = getattr(sequencings, 'DNA_source')
    tissues = Tissue.query.filter(Tissue.ID == tissue_id).first()

    # animal
    animal_name = getattr(tissues, 'animal_ID')
    animals = Animal.query.filter(Animal.animal_name == animal_name).first()

    # strain
    strain_name = getattr(animals, 'strain_name')
    strains = Strain.query.filter(Strain.name == strain_name).first()

    # analysis
    analyses = Analysis.query.filter(Analysis.Sequencing_ID == run_id).all()

    # tableset setting
    tableset['sequencing'] = sequencings
    tableset['tissue'] = tissues
    tableset['animal'] = animals
    tableset['strain'] = strains
    tableset['analysis'] = analyses

    # columnset filtering
    columnset['analysis'] = analysis_columns.remove('Sequencing_ID')
    columnset['sequencing'] = sequencing_columns.remove('run_ID')
    columnset['tissue'] = tissue_columns.remove('ID')
    columnset['animal'] = animal_columns.remove('animal_name')
    columnset['strain'] = strain_columns.remove('name')

    # columnset setting
    columnset['sequencing'] = sequencing_columns
    columnset['tissue'] = tissue_columns
    columnset['animal'] = animal_columns
    columnset['strain'] = strain_columns
    columnset['analysis'] = analysis_columns

    return render_template('view_detail.html', title='Sequencing Data', tableset=tableset, columnset=columnset)



