import pandas as pd
from models import db, Threat
from app import app

def ingest_data(csv_path):
    df = pd.read_csv(csv_path)
    with app.app_context():
        db.drop_all()
        db.create_all()
        for _, row in df.iterrows():
            threat = Threat(
                threat_category=row['Threat Category'],
                cleaned_description=row['Cleaned Threat Description'],
                severity_score=row['Severity Score']
            )
            db.session.add(threat)
        db.session.commit()

if __name__ == "__main__":
    ingest_data("../data/threats.csv")
