import json
import random
import csv
from lorem_text import lorem


class HistoireDeCasGenerator:

    def _generate_conditions():
        data = {
            "diabetes": random.getrandbits(1),
            "hypertension": random.getrandbits(1),
            "heart_condition": random.getrandbits(1),
            "asthma": random.getrandbits(1),
            "cholesterol": random.getrandbits(1)
        }
        return json.dumps(data)
    
    def _generate_allergies():
        data = {
            "topical_antibiotics": random.getrandbits(1),
            "topical_corticosteroids": random.getrandbits(1),
            "decongestant_eye_drops": random.getrandbits(1),
            "anesthetics": random.getrandbits(1),
            "preservatives": random.getrandbits(1)
        }
        return json.dumps(data)
    
    def _generate_medications():
        data = {
            "amiodarone": random.getrandbits(1),
            "digoxin": random.getrandbits(1),
            "isotretinoin": random.getrandbits(1),
            "chloroquine": random.getrandbits(1),
            "methylprednisolone": random.getrandbits(1)
        }
        return json.dumps(data)
    
    def _generate_trouble_vision():
        data = {
            "glaucoma": random.getrandbits(1),
            "cataract": random.getrandbits(1),
            "strabismus": random.getrandbits(1),
            "double_vision": random.getrandbits(1),
            "flash": random.getrandbits(1),
            "floaters": random.getrandbits(1),
            "macular_degeneration": random.getrandbits(1)
        }
        return json.dumps(data)
    
    def _generate_antecedants_familiaux():
        data = {
            "retinal_detachment": random.getrandbits(1),
            "macular_degeneration": random.getrandbits(1),
            "glaucoma": random.getrandbits(1)
        }
        return json.dumps(data)
    
    def _generate_antecedants_oculaires():
        data = {
            "surgery": random.getrandbits(1),
            "trauma": random.getrandbits(1),
            "retinal_detachment": random.getrandbits(1)
        }
        return json.dumps(data)

    @staticmethod
    def generate_csv():

        num_objects = 1000

        csv_file = "./DB/seeds/004-histoireDeCas.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            
            conditions = [HistoireDeCasGenerator._generate_conditions() for _ in range(num_objects)]
            allergies = [HistoireDeCasGenerator._generate_allergies() for _ in range(num_objects)]
            medications = [HistoireDeCasGenerator._generate_medications() for _ in range(num_objects)]
            trouble_vision = [HistoireDeCasGenerator._generate_trouble_vision() for _ in range(num_objects)]
            antecedants_familiaux = [HistoireDeCasGenerator._generate_antecedants_familiaux() for _ in range(num_objects)]
            antecedants_oculaires = [HistoireDeCasGenerator._generate_antecedants_oculaires() for _ in range(num_objects)]
            writer.writerow(["ID", "conditions", "allergies", "medications", "trouble_vision", "antecedants_familiaux", "antecedants_oculaires", "notes", "examen_ID"])
            for i in range(1, num_objects):
                writer.writerow([i, conditions[i], allergies[i], medications[i], trouble_vision[i], antecedants_familiaux[i], antecedants_oculaires[i], lorem.paragraph(), i])
        

class ExamensGenerator:

    def _generate_RX():
        def round_to_increment(value, increment):
            return round(value / increment) * increment

        data = {
            "Sphere_LE": "{:.2f}".format(round_to_increment(random.uniform(-20, 20), 0.25)),
            "Ast_LE": "{:.2f}".format(round_to_increment(random.uniform(-20, 20), 0.25)),
            "Axis_LE": round_to_increment(random.uniform(0, 180), 1),
            "Add_LE": "{:.2f}".format(round_to_increment(random.uniform(0, 5), 0.25)),
            "Acuity_LE": round_to_increment(random.uniform(1/6, 6/6), 1/6),
            "Sphere_RE": "{:.2f}".format(round_to_increment(random.uniform(-20, 20), 0.25)),
            "Ast_RE": "{:.2f}".format(round_to_increment(random.uniform(-20, 20), 0.25)),
            "Axis_RE": round_to_increment(random.uniform(0, 180), 1),
            "Add_RE": "{:.2f}".format(round_to_increment(random.uniform(0, 5), 0.25)),
            "Acuity_RE": round_to_increment(random.uniform(1/6, 6/6), 1/6)
        }

        return json.dumps(data)

    def _generate_lens_type():
        data = {
            "single_vision_lenses": random.getrandbits(1),
            "progressive_lenses": random.getrandbits(1),
            "office_lenses": random.getrandbits(1),
            "bifocal_lenses": random.getrandbits(1)
        }
        return json.dumps(data)
    
    def _generate_contact_lens_type():
        data = {
            "single_vision_contact_lenses": random.getrandbits(1),
            "multifocal_contact_lenses": random.getrandbits(1),
            "mono_vision_contact_lenses": random.getrandbits(1)
        }
        return json.dumps(data)

    @staticmethod
    def generate_csv():
        # Number of JSON objects you want to generate
        num_objects = 1000

        # Write JSON objects to a CSV file
        csv_file = "./DB/seeds/006-examens.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            
            RX_objectives = [ExamensGenerator._generate_RX() for _ in range(num_objects)]
            RX_subjective = [ExamensGenerator._generate_RX() for _ in range(num_objects)]
            lens_types = [ExamensGenerator._generate_lens_type() for _ in range(num_objects)]
            contact_lens_types = [ExamensGenerator._generate_contact_lens_type() for _ in range(num_objects)]
            old_rx = [ExamensGenerator._generate_RX() for _ in range(num_objects)]

            writer.writerow(["ID", "RX_objective", "RX_subjective", "contact_lens_type", "lens_type", "old_RX", "patient_ID", "optometriste_ID", "histoireDeCas_ID"])
            for i in range(0, num_objects):
                writer.writerow([i + 1, RX_objectives[i], RX_subjective[i], contact_lens_types[i], lens_types[i], old_rx[i], random.uniform(0, 250), random.uniform(0, 100), i + 1])
