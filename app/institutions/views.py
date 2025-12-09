from flask import Blueprint, render_template, request

institutions_bp = Blueprint(
    "institutions", __name__,
    template_folder="templates"
)
