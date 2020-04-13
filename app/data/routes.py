from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.models import CVocab, Strain, Animal, Tissue, Sequencing, Analysis
from app import db
from sqlalchemy import func


data = Blueprint('data', __name__)

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

@data.route('/')
@data.route('/view')
def view():
    # sequencing
    # data list
    view_list = db.session.query(
        Sequencing.Run_ID.label("RunID"),
        Animal.Strain_name.label("Rat_Strain"),
        Tissue.Type.label("Tissue_name"),
        Sequencing.Platform.label("Platform")).join(Tissue).join(Animal, Tissue.Animal_ID == Animal.Animal_name).all()
        # .options(func.replace(Sequencing.Raw_data_coverage, 'None', '')).all()
                 # , synchronize_session=False

    view_column_list = ['RunID', 'Rat_Strain', 'Tissue_name', 'Platform']
    # view_column_list = ['RunID', 'Rat_Strain', 'Tissue_name', 'Platform', 'Raw_data_coverage']

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
    sequencings = Sequencing.query.filter(Sequencing.Run_ID == run_id).first()

    # tissue
    tissue_id = getattr(sequencings, 'DNA_source')
    tissues = Tissue.query.filter(Tissue.ID == tissue_id).first()

    # animal
    animal_name = getattr(tissues, 'Animal_ID')
    animals = Animal.query.filter(Animal.Animal_name == animal_name).first()

    # strain
    strain_name = getattr(animals, 'Strain_name')
    strains = Strain.query.filter(Strain.Name == strain_name).first()

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
    columnset['sequencing'] = sequencing_columns.remove('Run_ID')
    columnset['tissue'] = tissue_columns.remove('ID')
    columnset['animal'] = animal_columns.remove('Animal_name')
    columnset['strain'] = strain_columns.remove('Name')

    # columnset setting
    columnset['sequencing'] = sequencing_columns
    columnset['tissue'] = tissue_columns
    columnset['animal'] = animal_columns
    columnset['strain'] = strain_columns
    columnset['analysis'] = analysis_columns

    return render_template('view_detail.html', title='Sequencing Data', tableset=tableset, columnset=columnset)



