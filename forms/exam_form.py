from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, IntegerField, SelectField
from wtforms.validators import NumberRange, ValidationError

def validate_rx_add(form, field):
    value = field.data
    if value % 0.25 != 0:
        raise ValidationError('Value must be in steps of 0.25')

class ExamForm(FlaskForm):
    diabetes = BooleanField('Diabète')
    hypertension = BooleanField('Hypertension artérielle')
    heart_condition = BooleanField('Troubles cardiaques')
    asthma = BooleanField('Asthme')
    cholesterol = BooleanField('Taux de cholesterol élevé')
    topical_antibiotics = BooleanField('Antibiotiques topiques')
    topical_corticosteroids = BooleanField('Corticostéroïdes topiques')
    decongestant_eye_drops = BooleanField('Collyres de décongestion')
    anesthetics = BooleanField('Anesthésiques')
    preservatives = BooleanField('Conservateurs dans les collyres')
    amiodarone = BooleanField('Amiodarone')
    digoxin = BooleanField('Digoxine')
    isotretinoin = BooleanField('Isotrétinoïne')
    chloroquine = BooleanField('Chloroquine')
    methylprednisolone = BooleanField('Méthylprednisolone')
    glaucoma = BooleanField('Glaucome')
    cataract = BooleanField('Cataracte')
    strabismus = BooleanField('Strabisme')
    double_vision = BooleanField('Vision double')
    flash = BooleanField('Perception de flash')
    floaters = BooleanField('Mouches volantes')
    macular_degeneration = BooleanField('Dégénérescence maculaire')
    family_retinal_detachment = BooleanField('Décollement de la rétine')
    family_macular_degeneration = BooleanField('Dégénérescence maculaire')
    family_glaucoma = BooleanField('Glaucome')
    surgery = BooleanField('Chirurgie aux yeux')
    trauma = BooleanField('Traumatisme aux yeux')
    retinal_detachment = BooleanField('Décollement de la rétine')

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    old_RX_Sphere_LE = SelectField('Sphère', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    old_RX_Ast_LE = SelectField('Ast', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    old_RX_Axis_LE = SelectField('Axe', choices=choices, validators=[NumberRange(min=0, max=180)])
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    old_RX_Add_LE = SelectField('Add', choices=choices, validators=[NumberRange(min=0, max=5), validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    old_RX_Acuity_LE = SelectField('Acuité', choices=choices, validators=[NumberRange(min=0.33, max=1)])

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    old_RX_Sphere_RE = SelectField('Sphere', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    old_RX_Ast_RE = SelectField('Ast', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    old_RX_Axis_RE = SelectField('Axe', choices=choices, validators=[NumberRange(min=0, max=180)])
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    old_RX_Add_RE = SelectField('Add', choices=choices, validators=[NumberRange(min=0, max=5), validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    old_RX_Acuity_RE = SelectField('Acuité', choices=choices, validators=[NumberRange(min=0.33, max=1)])

    single_vision_lenses = BooleanField('Verres simple vision')
    progressive_lenses = BooleanField('Verres progressifs')
    office_lenses = BooleanField('Verres offices')
    bifocal_lenses = BooleanField('Verres bifocaux')

    single_vision_contact_lenses = BooleanField('VC simple vision')
    multifocal_contact_lenses = BooleanField('VC multifocaux')
    mono_vision_contact_lenses = BooleanField('VC mono-vision')

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_objective_Sphere_LE = SelectField('Sphere', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    RX_objective_Ast_LE = SelectField('Ast', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    RX_objective_Axis_LE = SelectField('Axe', choices=choices, validators=[NumberRange(min=0, max=180)])
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_objective_Add_LE = SelectField('Add', choices=choices, validators=[NumberRange(min=0, max=5), validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    RX_objective_Acuity_LE = SelectField('Acuité', choices=choices, validators=[NumberRange(min=0.33, max=1)])

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_objective_Sphere_RE = SelectField('Sphere', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    RX_objective_Ast_RE = SelectField('Ast', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    RX_objective_Axis_RE = SelectField('Axe', choices=choices, validators=[NumberRange(min=0, max=180)])
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_objective_Add_RE = SelectField('Add', choices=choices, validators=[NumberRange(min=0, max=5), validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    RX_objective_Acuity_RE = SelectField('Acuité', choices=choices, validators=[NumberRange(min=0.33, max=1)])

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_subjective_Sphere_LE = SelectField('Sphere', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    RX_subjective_Ast_LE = SelectField('Ast', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    RX_subjective_Axis_LE = SelectField('Axe', choices=choices, validators=[NumberRange(min=0, max=180)])
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_subjective_Add_LE = SelectField('Add', choices=choices, validators=[NumberRange(min=0, max=5), validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    RX_subjective_Acuity_LE = SelectField('Acuité', choices=choices, validators=[NumberRange(min=0.33, max=1)])

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_subjective_Sphere_RE = SelectField('Sphere', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    RX_subjective_Ast_RE = SelectField('Ast', choices=choices, validators=[NumberRange(min=-20.0, max=20.0), validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    RX_subjective_Axis_RE = SelectField('Axe', choices=choices, validators=[NumberRange(min=0, max=180)])
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_subjective_Add_RE = SelectField('Add', choices=choices, validators=[NumberRange(min=0, max=5), validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    RX_subjective_Acuity_RE = SelectField('Acuité', choices=choices, validators=[NumberRange(min=0.33, max=1)])