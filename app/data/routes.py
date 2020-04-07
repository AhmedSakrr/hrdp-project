from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app.models import User, Post, CVocab, Strain, Animal, Tissue, Sequencing, Analysis


data = Blueprint('data', __name__)

@data.route('/data/hrdp')
def data_hrdp():

    tableset = {}
    columnset = {}

    # strain
    # data list
    cvocabs = CVocab.query.all()
    # column list
    cvocab_columns = CVocab.metadata.tables['ControlledVocab'].columns.keys()

    tableset['cvocab'] = cvocabs
    columnset['cvocab'] = cvocab_columns

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
    sequencing_list =[]
    sequencings = Sequencing.query.with_entities(Sequencing.run_ID, Sequencing.platform, Sequencing.Raw_data_coverage)
    # column list
    # sequencing_columns = Sequencing.metadata.tables['Sequencing'].columns['run_ID', 'platform', 'Raw_data_coverage']
    sequencing_columns = Tissue.metadata.tables['Sequencing'].columns.keys()
    print(sequencing_columns)
    print(type(sequencing_columns))
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

# int: type (안써도 된다 - more specific하게 지정한것)
@data.route("/data/hrdp/sequencing/<string:run_id>")
def sequencing(run_id):

    tableset = {}
    columnset = {}

    # get_or_404 is relative of get(), 404 is not found
    sequencings = Sequencing.query.all()
    # sequencings = Sequencing.query.get(run_id)
    sequencing_columns = Sequencing.metadata.tables['Sequencing'].columns.keys()
    # print("::::::::::::::::::::::::::::::::zzzzzzzzzzzzz::::", seq_data)
    # print("::::::::::::::::::::::::::::::::zzzzzzzzzzzzz::::", sequencing_columns)
    # post = Post.query.get_or_404(post_id)

    tableset['sequencing'] = sequencings
    columnset['sequencing'] = sequencing_columns

    return render_template('hrdp_sequencing.html', title='Sequencing Data', tableset=tableset, columnset=columnset)



