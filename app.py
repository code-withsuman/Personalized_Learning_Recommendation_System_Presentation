"""
EduAura: Personalized Learning Recommendation System
Main Flask Application connecting all 15 Project Modules.
"""

import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, Response, send_file

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, get_db
from modules.module1_student import register_student, authenticate_student, get_student_by_id, get_all_students
from modules.module2_collection import load_or_generate_dataset
from modules.module3_preprocessing import get_clean_data
from modules.module4_eda import run_exploratory_analysis
from modules.module7_training import train_and_persist_all_models
from modules.module8_recommendation import generate_personalized_recommendation, get_all_db_resources
from modules.module10_evaluation import get_evaluation_metrics
from modules.module11_visualization import get_cohort_visualization_data
from modules.module12_dashboard import assemble_student_dashboard_context
from modules.module13_admin import authenticate_admin, get_admin_system_metrics, add_new_resource, delete_resource, delete_student
from modules.module14_feedback import submit_feedback, get_all_feedback, get_feedback_summary
from modules.module15_reports import generate_student_markdown_report, generate_cohort_summary_report

app = Flask(__name__)
app.secret_key = "eduaura_super_secret_production_key_2026"

# ---------------------------------------------------------
# Application Initialization
# ---------------------------------------------------------
def startup_checks():
    init_db()
    clean_df = get_clean_data()
    run_exploratory_analysis(clean_df)
    train_and_persist_all_models(clean_df)
    print("EduAura Initialization Complete: Database ready, EDA charts rendered, ML models trained.")

startup_checks()


# ---------------------------------------------------------
# Core Navigation Routes
# ---------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "student_login":
            email_or_id = request.form.get("email_or_id", "").strip()
            password = request.form.get("password", "").strip()
            student = authenticate_student(email_or_id, password)
            if student:
                session.clear()
                session["student_id"] = student["student_id"]
                session["student_name"] = student["name"]
                flash(f"Welcome back, {student['name']}!", "success")
                return redirect(url_for("student_dashboard"))
            else:
                flash("Invalid Student ID/Email or Password.", "danger")

        elif action == "student_register":
            form_data = {k: request.form.get(k) for k in request.form}
            success, msg = register_student(form_data)
            if success:
                flash("Registration successful! You may now sign in.", "success")
            else:
                flash(f"Registration failed: {msg}", "danger")

        elif action == "admin_login":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            admin = authenticate_admin(username, password)
            if admin:
                session.clear()
                session["admin_user"] = admin["username"]
                session["admin_name"] = admin["name"]
                flash("Logged in to Administrator Portal.", "success")
                return redirect(url_for("admin_dashboard"))
            else:
                flash("Invalid Administrator credentials.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("index"))


# ---------------------------------------------------------
# Student Dashboard (Module 1, 8, 11, 12, 14)
# ---------------------------------------------------------
@app.route("/dashboard")
def student_dashboard():
    student_id = session.get("student_id")
    if not student_id:
        flash("Please log in to view your personalized dashboard.", "warning")
        return redirect(url_for("login"))

    context = assemble_student_dashboard_context(student_id)
    if not context:
        flash("Student profile not found.", "danger")
        return redirect(url_for("login"))

    return render_template("student_dashboard.html",
                           student=context["student"],
                           recommendation=context["recommendation"],
                           radar=context["radar"],
                           feedback_history=context["feedback_history"])


# ---------------------------------------------------------
# Admin Dashboard (Module 13)
# ---------------------------------------------------------
@app.route("/admin")
def admin_dashboard():
    if not session.get("admin_user"):
        flash("Admin credentials required to view this page.", "danger")
        return redirect(url_for("login"))

    metrics = get_admin_system_metrics()
    students = get_all_students()
    resources = get_all_db_resources()
    feedbacks = get_all_feedback()

    return render_template("admin_dashboard.html",
                           metrics=metrics,
                           students=students,
                           resources=resources,
                           feedbacks=feedbacks)


@app.route("/admin/add-resource", methods=["POST"])
def admin_add_resource():
    if not session.get("admin_user"):
        return redirect(url_for("login"))

    data = {k: request.form.get(k) for k in request.form}
    success, msg = add_new_resource(data)
    if success:
        flash("New learning resource added successfully!", "success")
    else:
        flash(f"Error adding resource: {msg}", "danger")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete-resource/<int:resource_id>", methods=["POST"])
def admin_delete_resource(resource_id):
    if not session.get("admin_user"):
        return redirect(url_for("login"))
    delete_resource(resource_id)
    flash("Resource deleted successfully.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete-student/<student_id>", methods=["POST"])
def admin_delete_student(student_id):
    if not session.get("admin_user"):
        return redirect(url_for("login"))
    delete_student(student_id)
    flash(f"Student {student_id} removed from database.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/retrain", methods=["POST"])
def admin_retrain():
    if not session.get("admin_user"):
        return redirect(url_for("login"))
    df = get_clean_data()
    train_and_persist_all_models(df)
    run_exploratory_analysis(df)
    flash("ML Pipelines re-trained and EDA charts refreshed successfully.", "success")
    return redirect(url_for("admin_dashboard"))


# ---------------------------------------------------------
# EDA & Analytics (Module 4)
# ---------------------------------------------------------
@app.route("/eda")
def eda_view():
    return render_template("eda.html")


# ---------------------------------------------------------
# ML Models & Clustering Evaluation (Modules 6, 7, 10)
# ---------------------------------------------------------
@app.route("/models")
def model_results_view():
    eval_data = get_evaluation_metrics()
    return render_template("model_results.html", eval_data=eval_data)


# ---------------------------------------------------------
# Reports & Result Module (Module 15)
# ---------------------------------------------------------
@app.route("/reports")
def reports_view():
    cohort_report = generate_cohort_summary_report()
    sample_students = get_all_students()[:8]
    return render_template("reports.html", cohort_report=cohort_report, sample_students=sample_students)


@app.route("/download/report/<student_id>")
def download_student_report(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash("Student record not found.", "danger")
        return redirect(url_for("reports_view"))

    md_content = generate_student_markdown_report(student)
    filename = f"EduAura_Diagnostic_Report_{student_id}.md"

    return Response(
        md_content,
        mimetype="text/markdown",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )


@app.route("/download/dataset")
def download_clean_dataset():
    path = os.path.join(os.path.dirname(__file__), "data", "student_clean.csv")
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name="clean_student_data.csv")
    flash("Dataset file not available.", "danger")
    return redirect(url_for("eda_view"))


# ---------------------------------------------------------
# AJAX Feedback Endpoint (Module 14)
# ---------------------------------------------------------
@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    student_id = request.form.get("student_id", "Anonymous")
    resource_title = request.form.get("resource_title", "Unknown Resource")
    rating = int(request.form.get("rating", 5))
    is_useful = int(request.form.get("is_useful", 1))
    comment = request.form.get("comment", "")

    submit_feedback(student_id, resource_title, rating, is_useful, comment)
    return jsonify({"success": True, "message": "Feedback recorded."})


# ---------------------------------------------------------
# Main Execution Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting EduAura Flask Application on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
