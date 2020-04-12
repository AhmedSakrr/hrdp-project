from datetime import datetime
from app import db
from flask import current_app


class CVocab(db.Model):
    __tablename__ = "ControlledVocab"
    vocab = db.Column(db.Text, unique=True, primary_key=True)

    def __repr__(self):
        return f"Strain('{self.vocab}')"


class Strain(db.Model):
    __tablename__ = "Strain"
    ID = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False, primary_key=True)
    type = db.Column(db.String(10))
    living = db.Column(db.Boolean)
    source = db.Column(db.String(50))
    note = db.Column(db.Text)

    def __repr__(self):
        return f"Strain('{self.ID}', '{self.name}', '{self.type}', '{self.living}', '{self.source}', '{self.note}')"


class Animal(db.Model):
    __tablename__ = "Animal"
    animal_name = db.Column(db.String(50), nullable=False, primary_key=True)
    strain_name = db.Column(db.String(50), nullable=False) #, db.ForeignKey('strain.name')
    sex = db.Column(db.String(1))
    age = db.Column(db.String(50))
    generation = db.Column(db.String(50))
    euthanasia_date = db.Column(db.String(50))
    source = db.Column(db.String(50))
    note = db.Column(db.Text)

    def __repr__(self):
        return f"Animal('{self.animal_name}', '{self.strain_name}', '{self.sex}', '{self.age}', '{self.generation}', '{self.euthanasia_date}', '{self.source}', '{self.note}')"

class Tissue(db.Model):
    __tablename__ = "Tissue"
    ID = db.Column(db.String(50), nullable=False, unique=True, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    animal_ID = db.Column(db.String(50), db.ForeignKey('animal.name'), nullable=False)
    Transfer_History = db.Column(db.Text)
    note = db.Column(db.Text)

    def __repr__(self):
        return f"Strain('{self.ID}', '{self.type}', '{self.animal_ID}', '{self.Transfer_History}', '{self.note}')"

class Sequencing(db.Model):
    __tablename__ = "Sequencing"
    run_ID = db.Column(db.String(50), nullable=False, primary_key=True)
    platform = db.Column(db.String(50), db.ForeignKey('ControlledVocab.vocab'), nullable=False) # FK _controlled_vocab(vocab)
    DNA_source = db.Column(db.String(50), db.ForeignKey('Tissue.ID'), nullable=False) #FK sequencing_Tissue_ID_fk references
    Library_facility = db.Column(db.String(50))
    Sequencing_facility = db.Column(db.String(50))
    DNA_extraction_method = db.Column(db.String(50))
    DNA_concentration = db.Column(db.String(50))
    DNA_target_length = db.Column(db.String(10))
    DNA_extraction_technician = db.Column(db.String(50))
    DNA_extraction_date = db.Column(db.DateTime)
    DNA_extraction_facility = db.Column(db.String(50))
    Library_date = db.Column(db.DateTime)
    Library_kit = db.Column(db.String(50))
    Library_technician = db.Column(db.String(50))
    Sequencing_instrument = db.Column(db.String(50))
    Sequencing_technician = db.Column(db.String(50))
    Sequencing_date = db.Column(db.DateTime)
    Raw_data_read_length = db.Column(db.Integer)
    Raw_data_format = db.Column(db.String(50))
    Raw_data_read_count = db.Column(db.Integer)
    Raw_data_file_name = db.Column(db.String(100))
    Raw_data_available_from = db.Column(db.String(50))
    Raw_data_location = db.Column(db.String(50))
    Raw_data_backup_location = db.Column(db.String(50))
    Raw_data_coverage = db.Column(db.String(50))
    note = db.Column(db.Text)

    def __repr__(self):
        return f"Strain('{self.run_ID}', '{self.platform}', '{self.DNA_source}', '{self.Library_facility}', '{self.Sequencing_facility}'" \
               f", '{self.DNA_extraction_method}', '{self.DNA_concentration}', '{self.DNA_target_length}', '{self.DNA_extraction_technician}'" \
               f", '{self.DNA_extraction_date}', '{self.DNA_extraction_facility}', '{self.Library_date}', '{self.Library_kit}', '{self.Library_technician}'" \
               f", '{self.Sequencing_instrument}', '{self.Sequencing_technician}', '{self.Sequencing_date}', '{self.Raw_data_read_length}', '{self.Raw_data_format}'" \
               f", '{self.Raw_data_read_count}', '{self.Raw_data_file_name}', '{self.Raw_data_available_from}', '{self.Raw_data_location}', '{self.Raw_data_backup_location}'), '{self.Raw_data_coverage}'), '{self.note}')"


class Analysis(db.Model):
    __tablename__ = "Analysis"
    Analysis_ID = db.Column(db.String(50), nullable=False, primary_key=True)
    Sequencing_ID = db.Column(db.String(50), nullable=False) #FK references sequencing
    Software_name = db.Column(db.String(50), nullable=False) #FK _controlled_vocab_vocab_fk references _controlled_vocab(),
    Software_version = db.Column(db.String(50), nullable=False)
    Analyst_name = db.Column(db.String(50), nullable=False)
    # Analysis_status = db.Column(db.String(50))
    note = db.Column(db.Text)

    def __repr__(self):
        return f"Strain('{self.Analysis_ID}', '{self.Sequencing_ID}', '{self.Software_name}', '{self.Software_version}', '{self.Analyst_name}', '{self.Analysis_status}', '{self.note}'"




