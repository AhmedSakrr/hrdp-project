from datetime import datetime
from app import db
from flask import current_app

class CVocab(db.Model):
    __tablename__ = "ControlledVocab"
    vocab = db.Column(db.Text, unique=True, primary_key=True)

class Analysis(db.Model):
    __tablename__ = "Analysis"
    Analysis_ID = db.Column(db.String(50), nullable=False, primary_key=True)
    Sequencing_ID = db.Column(db.String(50), nullable=False) #FK references sequencing
    Software_name = db.Column(db.String(50), nullable=False) #FK _controlled_vocab_vocab_fk references _controlled_vocab(),
    Software_version = db.Column(db.String(50), nullable=False)
    Results_dir = db.Column(db.String(50), nullable=False)
    Analysis_date = db.Column(db.String(50))
    Note = db.Column(db.Text)

class Animal(db.Model):
    __tablename__ = "Animal"
    Animal_name = db.Column(db.String(50), nullable=False, unique=True, primary_key=True)
    Strain_name = db.Column(db.String(50), nullable=False) #, db.ForeignKey('strain.name')
    Sex = db.Column(db.String(1))
    Age = db.Column(db.String(50))
    Generation = db.Column(db.String(50))
    Euthanasia_date = db.Column(db.String(50))
    Source = db.Column(db.String(50))
    Note = db.Column(db.Text)

class Sequencing(db.Model):
    __tablename__ = "Sequencing"
    Run_ID = db.Column(db.String(50), nullable=False, unique=True, primary_key=True)
    DNA_source = db.Column(db.String(50), db.ForeignKey('Tissue.ID'),
                           nullable=False)  # FK sequencing_Tissue_ID_fk references
    Platform = db.Column(db.String(50), db.ForeignKey('ControlledVocab.vocab'), nullable=False) # FK _controlled_vocab(vocab)
    DNA_extraction_method = db.Column(db.String(50))
    DNA_concentration = db.Column(db.String(50))
    DNA_target_length = db.Column(db.String(10))
    DNA_extraction_facility = db.Column(db.String(50))
    Library_kit = db.Column(db.String(50))
    Library_facility = db.Column(db.String(50))
    Sequencing_instrument = db.Column(db.String(50))
    Sequencing_date = db.Column(db.String(50))
    Sequencing_facility = db.Column(db.String(50))
    Sequencing_notes = db.Column(db.Text)
    Raw_data_dir_name = db.Column(db.String(100))
    Raw_data_format = db.Column(db.String(50))
    Raw_data_file_size_GB = db.Column(db.Integer)
    Raw_data_available_from = db.Column(db.String(50))
    Note = db.Column(db.Text)

class Strain(db.Model):
    __tablename__ = "Strain"
    ID = db.Column(db.String(50), nullable=False)
    Name = db.Column(db.String(50), nullable=False, unique=True, primary_key=True)
    Type = db.Column(db.String(10))
    Living = db.Column(db.Boolean)
    Source = db.Column(db.String(50))
    Note = db.Column(db.Text)

class Tissue(db.Model):
    __tablename__ = "Tissue"
    ID = db.Column(db.String(50), nullable=False, unique=True, primary_key=True)
    Type = db.Column(db.String(50), nullable=False)
    Animal_ID = db.Column(db.String(50), db.ForeignKey('animal.name'), nullable=False)
    Transfer_History = db.Column(db.Text)
    Note = db.Column(db.Text)

class Deepvariant_results(db.Model):
    __tablename__ = "Deepvariant_results"

    index = db.Column(db.Integer, primary_key=True)
    Analysis_ID = db.Column(db.String(50), db.ForeignKey('Analysis.Analysis_ID'))
    Chr = db.Column(db.String(10))
    Biallelic_Deletion = db.Column(db.INTEGER)
    Biallelic_Insertion = db.Column(db.INTEGER)
    Biallelic_SNP = db.Column(db.INTEGER)
    Multiallelic_Complex = db.Column(db.INTEGER)
    Multiallelic_Deletion = db.Column(db.INTEGER)
    Multiallelic_Insertion = db.Column(db.INTEGER)
    Multiallelic_SNP = db.Column(db.INTEGER)
    RefCall = db.Column(db.INTEGER)
    Transition = db.Column(db.INTEGER)
    Transversion = db.Column(db.INTEGER)

class LongRanger_results(db.Model):
    __tablename__ = "LongRanger_results"

    Analysis_ID = db.Column(db.String(50), db.ForeignKey('Analysis.Analysis_ID'), primary_key=True)
    instrument_ids = db.Column(db.String(20))
    gems_detected = db.Column(db.INTEGER)
    mean_dna_per_gem = db.Column(db.Float)
    bc_on_whitelist = db.Column(db.Float)
    bc_mean_qscore = db.Column(db.Float)
    n50_linked_reads_per_molecule = db.Column(db.Integer)
    corrected_loaded_mass_ng = db.Column(db.Float)
    snps_phased = db.Column(db.Float)
    genes_phased_lt_100kb = db.Column(db.Float)
    longest_phase_block = db.Column(db.Integer)
    n50_phase_block = db.Column(db.Integer)
    molecule_length_mean = db.Column(db.Float)
    molecule_length_stddev = db.Column(db.Float)
    number_reads = db.Column(db.Integer)
    median_insert_size = db.Column(db.Integer)
    mean_depth = db.Column(db.Float)
    zero_coverage = db.Column(db.Float)
    mapped_reads = db.Column(db.Float)
    pcr_duplication = db.Column(db.Float)
    on_target_bases = db.Column(db.String(50))
    r1_q20_bases_fract = db.Column(db.Float)
    r1_q30_bases_fract = db.Column(db.Float)
    r2_q20_bases_fract = db.Column(db.Float)
    r2_q30_bases_fract = db.Column(db.Float)
    si_q20_bases_fract = db.Column(db.Float)
    si_q30_bases_fract = db.Column(db.Float)
    bc_q20_bases_fract = db.Column(db.Float)
    bc_q30_bases_fract = db.Column(db.Float)
    large_sv_calls = db.Column(db.Integer)
    short_deletion_calls = db.Column(db.Integer)

class Supernova_results(db.Model):
    __tablename__ = "Supernova_results"

    Analysis_ID = db.Column(db.String(50), db.ForeignKey('Analysis.Analysis_ID'), primary_key=True)
    assembly_size = db.Column(db.Integer)
    barcode_fraction = db.Column(db.Integer)
    bases_per_read = db.Column(db.Float)
    bridge_1_50 = db.Column(db.Float)
    bridge_50= db.Column(db.Float)
    bridge_model_badness_of_fit = db.Column(db.Float)
    checksum = db.Column(db.Float)
    contig_N50 = db.Column(db.Integer)
    dinucleotide_percent = db.Column(db.Float)
    dup_perc = db.Column(db.Float)
    edge_N50 = db.Column(db.Integer)
    effective_coverage = db.Column(db.Float)
    est_genome_size = db.Column(db.Integer)
    gc_percent = db.Column(db.Float)
    hetdist = db.Column(db.Integer)
    high_AT_index = db.Column(db.Float)
    likely_sequencers = db.Column(db.String(50))
    lw_mean_mol_len = db.Column(db.Float)
    m10 = db.Column(db.Float)
    median_ins_sz = db.Column(db.Integer)
    nreads = db.Column(db.Integer)
    p10 = db.Column(db.Float)
    phase_block_N50 = db.Column(db.Integer)
    placed_perc = db.Column(db.Float)
    proper_pairs_perc = db.Column(db.Float)
    q30_r2_perc = db.Column(db.Float)
    raw_coverage = db.Column(db.Float)
    read_rate_DF_1_threaded = db.Column(db.Float)
    read_rate_IO_10_threaded = db.Column(db.Float)
    read_rate_IO_1_threaded = db.Column(db.Float)
    repfrac = db.Column(db.Float)
    rpb_N50 = db.Column(db.Integer)
    scaffold_N50 = db.Column(db.Integer)
    scaffolds_10kb_plus = db.Column(db.Integer)
    scaffolds_1kb_plus = db.Column(db.Integer)
    unbar_perc = db.Column(db.Float)
    valid_bc_perc = db.Column(db.Float)

