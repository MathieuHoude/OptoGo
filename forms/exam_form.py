from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, IntegerField, SelectField, StringField
from wtforms.validators import NumberRange, ValidationError

def validate_rx_add(form, field):
    value = float(field.data)
    if value % 0.25 != 0:
        raise ValidationError('Value must be in steps of 0.25')

class ExamForm(FlaskForm):
    ID = StringField('ID')
    patient_ID = IntegerField('ID patient')
    optometriste_ID = IntegerField('ID optometriste')
    histoireDeCas_ID = IntegerField('ID histoire de cas')
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    old_RX_Sphere_LE = SelectField('Sphère', choices=choices, validators=[validate_rx_add])
    old_RX_Ast_LE = SelectField('Ast', choices=choices, validators=[validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    old_RX_Axis_LE = SelectField('Axe', choices=choices)
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    old_RX_Add_LE = SelectField('Add', choices=choices, validators=[validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    old_RX_Acuity_LE = SelectField('Acuité', choices=choices)

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    old_RX_Sphere_RE = SelectField('Sphere', choices=choices, validators=[validate_rx_add])
    old_RX_Ast_RE = SelectField('Ast', choices=choices, validators=[validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    old_RX_Axis_RE = SelectField('Axe', choices=choices)
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    old_RX_Add_RE = SelectField('Add', choices=choices, validators=[validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    old_RX_Acuity_RE = SelectField('Acuité', choices=choices)

    lens_type_single_vision_lenses = BooleanField('Verres simple vision')
    lens_type_progressive_lenses = BooleanField('Verres progressifs')
    lens_type_office_lenses = BooleanField('Verres offices')
    lens_type_bifocal_lenses = BooleanField('Verres bifocaux')

    contact_lens_type_single_vision_contact_lenses = BooleanField('VC simple vision')
    contact_lens_type_multifocal_contact_lenses = BooleanField('VC multifocaux')
    contact_lens_type_mono_vision_contact_lenses = BooleanField('VC mono-vision')

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_objective_Sphere_LE = SelectField('Sphere', choices=choices, validators=[validate_rx_add])
    RX_objective_Ast_LE = SelectField('Ast', choices=choices, validators=[validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    RX_objective_Axis_LE = SelectField('Axe', choices=choices)
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_objective_Add_LE = SelectField('Add', choices=choices, validators=[validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    RX_objective_Acuity_LE = SelectField('Acuité', choices=choices)

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_objective_Sphere_RE = SelectField('Sphere', choices=choices, validators=[validate_rx_add])
    RX_objective_Ast_RE = SelectField('Ast', choices=choices, validators=[validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    RX_objective_Axis_RE = SelectField('Axe', choices=choices)
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_objective_Add_RE = SelectField('Add', choices=choices, validators=[validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    RX_objective_Acuity_RE = SelectField('Acuité', choices=choices)

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_subjective_Sphere_LE = SelectField('Sphere', choices=choices, validators=[validate_rx_add])
    RX_subjective_Ast_LE = SelectField('Ast', choices=choices, validators=[validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    RX_subjective_Axis_LE = SelectField('Axe', choices=choices)
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_subjective_Add_LE = SelectField('Add', choices=choices, validators=[validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    RX_subjective_Acuity_LE = SelectField('Acuité', choices=choices)

    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(-80, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_subjective_Sphere_RE = SelectField('Sphere', choices=choices, validators=[validate_rx_add])
    RX_subjective_Ast_RE = SelectField('Ast', choices=choices, validators=[validate_rx_add])
    choices = [(str(x), str(x)) for x in range(0, 181)]  # Generating options from 0 to 180
    RX_subjective_Axis_RE = SelectField('Axe', choices=choices)
    choices = [("%.2f" % (x / 4.0), "%.2f" % (x / 4.0)) for x in range(0, 81)]  # Generating options from -20 to 20 by steps of 0.25
    RX_subjective_Add_RE = SelectField('Add', choices=choices, validators=[validate_rx_add])
    choices = [(1/6, '1/6'), (2/6, '2/6'), (3/6, '3/6'), (4/6, '4/6'), (5/6, '5/6'), (6/6, '6/6')]
    RX_subjective_Acuity_RE = SelectField('Acuité', choices=choices)

    periode_validite = IntegerField('Période de validité')