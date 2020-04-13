from datetime import datetime
from app import db
from flask import current_app


class CVocab(db.Model):
    __tablename__ = "ControlledVocab"
    vocab = db.Column(db.Text, unique=True, primary_key=True)

    def __repr__(self):
        return f"Strain('{self.vocab}')"


class Analysis(db.Model):
    __tablename__ = "Analysis"
    Analysis_ID = db.Column(db.String(50), nullable=False, primary_key=True)
    Sequencing_ID = db.Column(db.String(50), nullable=False) #FK references sequencing
    Software_name = db.Column(db.String(50), nullable=False) #FK _controlled_vocab_vocab_fk references _controlled_vocab(),
    Software_version = db.Column(db.String(50), nullable=False)
    Results_dir = db.Column(db.String(50), nullable=False)
    Analysis_date = db.Column(db.String(50))
    note = db.Column(db.Text)

    def __repr__(self):
        return f"Strain('{self.Analysis_ID}', '{self.Sequencing_ID}', '{self.Software_name}', '{self.Software_version}', '{self.Results_dir}', '{self.Analysis_date}', '{self.note}'"


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

    def __repr__(self):
        return f"Animal('{self.Animal_name}', '{self.Strain_name}', '{self.Sex}', '{self.Age}', '{self.Generation}', '{self.Euthanasia_date}', '{self.Source}', '{self.Note}')"


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

    def __repr__(self):
        return f"Strain('{self.Run_ID}', '{self.DNA_source}', '{self.Platform}', '{self.DNA_extraction_method}', '{self.DNA_concentration}', '{self.DNA_target_length}', '{self.DNA_extraction_technician}'" \
               f", '{self.DNA_extraction_facility}', '{self.Library_kit}', '{self.Library_facility}'" \
               f", '{self.Sequencing_instrument}', '{self.Sequencing_date}', '{self.Sequencing_facility}', '{self.Sequencing_notes}'" \
               f", '{self.Raw_data_dir_name}', '{self.Raw_data_format}', '{self.Raw_data_file_size_GB}', '{self.Raw_data_available_from}', '{self.Note}'))"


class Strain(db.Model):
    __tablename__ = "Strain"
    ID = db.Column(db.String(50), nullable=False)
    Name = db.Column(db.String(50), nullable=False, unique=True, primary_key=True)
    Type = db.Column(db.String(10))
    Living = db.Column(db.Boolean)
    Source = db.Column(db.String(50))
    Note = db.Column(db.Text)

    def __repr__(self):
        return f"Strain('{self.ID}', '{self.name}', '{self.type}', '{self.living}', '{self.source}', '{self.note}')"


class Tissue(db.Model):
    __tablename__ = "Tissue"
    ID = db.Column(db.String(50), nullable=False, unique=True, primary_key=True)
    Type = db.Column(db.String(50), nullable=False)
    Animal_ID = db.Column(db.String(50), db.ForeignKey('animal.name'), nullable=False)
    Transfer_History = db.Column(db.Text)
    Note = db.Column(db.Text)

    def __repr__(self):
        return f"Strain('{self.ID}', '{self.type}', '{self.animal_ID}', '{self.Transfer_History}', '{self.note}')"




