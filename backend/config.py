
try:
    import os
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/threatdb")
except Exception as e:
    raise RuntimeError("Failed to load configuration: {}".format(e))


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Threat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threat_category = db.Column(db.String(120))
    cleaned_description = db.Column(db.Text)
    severity_score = db.Column(db.Integer)

# backend/app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Threat
from config import DATABASE_URL

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/api/threats", methods=["GET"])
def get_threats():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    category = request.args.get("category")
    search = request.args.get("search")

    query = Threat.query
    if category:
        query = query.filter(Threat.threat_category.ilike(f"%{category}%"))
    if search:
        query = query.filter(Threat.cleaned_description.ilike(f"%{search}%"))

    threats = query.paginate(page=page, per_page=limit, error_out=False).items
    return jsonify([{
        "id": t.id,
        "threat_category": t.threat_category,
        "cleaned_description": t.cleaned_description,
        "severity_score": t.severity_score
    } for t in threats])

@app.route("/api/threats/<int:threat_id>", methods=["GET"])
def get_threat(threat_id):
    threat = Threat.query.get(threat_id)
    if not threat:
        return jsonify({"error": "Not Found"}), 404
    return jsonify({
        "id": threat.id,
        "threat_category": threat.threat_category,
        "cleaned_description": threat.cleaned_description,
        "severity_score": threat.severity_score
    })

@app.route("/api/threats/stats", methods=["GET"])
def get_stats():
    total = Threat.query.count()
    categories = db.session.query(Threat.threat_category, db.func.count()).group_by(Threat.threat_category).all()
    severity = db.session.query(Threat.severity_score, db.func.count()).group_by(Threat.severity_score).all()
    return jsonify({
        "total_threats": total,
        "by_category": dict(categories),
        "by_severity": dict(severity)
    })

if __name__ == "__main__":
    app.run(debug=True)
