ALTER TABLE prescriptions
ADD CONSTRAINT FK_examens_prescriptions FOREIGN KEY (examen_ID) REFERENCES examens(ID) ON DELETE NO ACTION;