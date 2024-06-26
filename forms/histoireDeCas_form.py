from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, HiddenField
from wtforms.validators import Length, Optional

class HistoireDeCasForm(FlaskForm):
    ID = HiddenField("ID", validators=[Optional()])
    conditions_diabetes = BooleanField('Diabète')
    conditions_hypertension = BooleanField('Hypertension artérielle')
    conditions_heart_condition = BooleanField('Troubles cardiaques')
    conditions_asthma = BooleanField('Asthme')
    conditions_cholesterol = BooleanField('Taux de cholesterol élevé')
    allergies_topical_antibiotics = BooleanField('Antibiotiques topiques')
    allergies_topical_corticosteroids = BooleanField('Corticostéroïdes topiques')
    allergies_decongestant_eye_drops = BooleanField('Collyres de décongestion')
    allergies_anesthetics = BooleanField('Anesthésiques')
    allergies_preservatives = BooleanField('Conservateurs dans les collyres')
    medications_amiodarone = BooleanField('Amiodarone')
    medications_digoxin = BooleanField('Digoxine')
    medications_isotretinoin = BooleanField('Isotrétinoïne')
    medications_chloroquine = BooleanField('Chloroquine')
    medications_methylprednisolone = BooleanField('Méthylprednisolone')
    trouble_vision_glaucoma = BooleanField('Glaucome')
    trouble_vision_cataract = BooleanField('Cataracte')
    trouble_vision_strabismus = BooleanField('Strabisme')
    trouble_vision_double_vision = BooleanField('Vision double')
    trouble_vision_flash = BooleanField('Perception de flash')
    trouble_vision_floaters = BooleanField('Mouches volantes')
    trouble_vision_macular_degeneration = BooleanField('Dégénérescence maculaire')
    antecedants_familiaux_retinal_detachment = BooleanField('Décollement de la rétine')
    antecedants_familiaux_macular_degeneration = BooleanField('Dégénérescence maculaire')
    antecedants_familiaux_glaucoma = BooleanField('Glaucome')
    antecedants_oculaires_surgery = BooleanField('Chirurgie aux yeux')
    antecedants_oculaires_trauma = BooleanField('Traumatisme aux yeux')
    antecedants_oculaires_retinal_detachment = BooleanField('Décollement de la rétine')
    notes = StringField('Notes', validators=[Length(max=2000)], default='')