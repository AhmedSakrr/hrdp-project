from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.models import *
from app import db
from sqlalchemy import func, inspect

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

    view_column_list = ['RunID', 'Rat_Strain', 'Tissue_name', 'Platform']

    return render_template('view.html', title='Sequencing View', columnset=view_column_list, tableset=view_list)

@data.route("/data/view_detail/<string:run_id>")
def view_detail(run_id):

    tableset = {}
    columnset = {}

    column_list = ['Strain', 'Animal','Tissue','Sequencing','Analysis','LongRanger results','Deepvariant results','Supernova results' ]

    # collecting columns for each table
    strain_columns = Strain.metadata.tables['Strain'].columns.keys()
    animal_columns = Animal.metadata.tables['Animal'].columns.keys()
    tissue_columns = Tissue.metadata.tables['Tissue'].columns.keys()
    sequencing_columns = Sequencing.metadata.tables['Sequencing'].columns.keys()
    analysis_columns = Analysis.metadata.tables['Analysis'].columns.keys()
    deepvariant_results_columns = Deepvariant_results.metadata.tables['Deepvariant_results'].columns.keys()
    longRanger_results_columns = LongRanger_results.metadata.tables['LongRanger_results'].columns.keys()
    supernova_results_columns = Supernova_results.metadata.tables['Supernova_results'].columns.keys()

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
   
   
   # TODO must be fixed with this part
    Deepvariant_res = None
    LongRanger_res = None
    Supernova_res = None
    for analysis in analyses:
        deepvariant_result = Deepvariant_results.query.filter(Deepvariant_results.Analysis_ID == getattr(analysis, 'Analysis_ID')).all()
        longRanger_result = LongRanger_results.query.filter(LongRanger_results.Analysis_ID == getattr(analysis, 'Analysis_ID')).first()
        supernova_result = Supernova_results.query.filter(Supernova_results.Analysis_ID == getattr(analysis, 'Analysis_ID')).first()    
        
        if deepvariant_result !=None:
            Deepvariant_res = deepvariant_result

        if longRanger_result !=None:
            LongRanger_res = longRanger_result    
        
        if supernova_result !=None:
            Supernova_res = supernova_result

    # tableset setting
    tableset['Sequencing'] = sequencings
    tableset['Tissue'] = tissues
    tableset['Animal'] = animals
    tableset['Strain'] = strains
    tableset['Analysis'] = analyses
    tableset['Deepvariant results'] = Deepvariant_res
    tableset['LongRanger results'] = LongRanger_res
    tableset['Supernova results'] = Supernova_res


    # columnset filtering
    columnset['Analysis'] = analysis_columns.remove('Sequencing_ID')
    columnset['Sequencing'] = sequencing_columns.remove('Run_ID')
    columnset['Tissue'] = tissue_columns.remove('Animal_ID')
    columnset['Animal'] = animal_columns.remove('Strain_name')

    # columnset setting
    columnset['Sequencing'] = sequencing_columns
    columnset['Tissue'] = tissue_columns
    columnset['Animal'] = animal_columns
    columnset['Strain'] = strain_columns
    columnset['Analysis'] = analysis_columns
    if Deepvariant_res != None:
        columnset['Deepvariant results'] = deepvariant_results_columns
    if LongRanger_res != None:
        columnset['LongRanger results'] = longRanger_results_columns
    if Supernova_res != None:
        columnset['Supernova results'] = supernova_results_columns

    return render_template('view_detail.html', title='Sequencing Data', tableset=tableset, columnset=columnset,column_list=column_list, detail_target=run_id)

