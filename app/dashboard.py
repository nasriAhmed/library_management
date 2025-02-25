from flask import Blueprint, render_template, jsonify
from app.logger import setup_logger

logger = setup_logger()

dashboard = Blueprint("dashboard", __name__, template_folder="../templates")


@dashboard.route("/logs")
def get_logs():
    """
    Endpoint pour récupérer les logs de l'application.

    Returns:
        dict: JSON contenant les logs en format texte.
    """
    try:
        with open("logs/app.log", "r") as log_file:
            logs = log_file.readlines()
        return jsonify({"logs": logs})
    except FileNotFoundError:
        return jsonify({"error": "Log file not found"}), 404


@dashboard.route("/")
def index():
    """
    Affiche la page du tableau de bord avec les logs.

    Returns:
        HTML: Template `dashboard.html` pour
        l'affichage des logs en temps réel.
    """
    return render_template("dashboard.html")
