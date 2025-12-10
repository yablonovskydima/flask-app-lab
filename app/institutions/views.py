from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from app.institutions.institution_forms import EducationInstitutionForm
from app.institutions.type_forms import InstitutionTypeForm
from app.institutions.models import EducationInstitution, InstitutionType
from flask_login import current_user
from app import db

institutions_bp = Blueprint(
    "institutions", __name__,
    template_folder="templates"
)

@institutions_bp.route("/institutions/create", methods=["GET", "POST"])
def create_institution():
    form = EducationInstitutionForm()

    form.set_type_choices()
    form.set_author_choices()

    if form.validate_on_submit():
        institution = EducationInstitution(
            name=form.name.data,
            address=form.address.data,
            description=form.description.data,
            type_id=form.type_id.data,
            author_id=form.author_id.data
        )

        db.session.add(institution)
        db.session.commit()

        flash("Institution successfully created!", "success")
        return redirect(url_for("institutions.list_institutions"))

    return render_template("institutions/create_institution.html", form=form)

@institutions_bp.route("/types/create", methods=["GET", "POST"])
def create_institution_type():
    form = InstitutionTypeForm()
    if form.validate_on_submit():
        existing = InstitutionType.query.filter_by(type_name=form.type_name.data.strip()).first()
        if existing:
            flash("Institution type with this name already exists.", "warning")
            return redirect(url_for("institutions.create_institution_type"))

        new_type = InstitutionType(
            type_name=form.type_name.data.strip(),
            description=form.description.data.strip() if form.description.data else None
        )
        db.session.add(new_type)
        db.session.commit()

        flash("Institution type created successfully.", "success")
        return redirect(url_for("institutions.list_institutions"))

    return render_template("types/create_institution_type.html", form=form)


@institutions_bp.route("/institutions")
def list_institutions():
    institutions = EducationInstitution.query.all()
    return render_template("institutions/list_institutions.html", institutions=institutions)

@institutions_bp.route("/types")
def list_institution_types():
    types = InstitutionType.query.order_by(InstitutionType.type_name).all()
    return render_template("types/list_institution_types.html", types=types)

@institutions_bp.route("/institutions/<int:id>/edit", methods=["GET", "POST"])
def edit_institution(id):
    institution = EducationInstitution.query.get_or_404(id)

    if institution.author_id != current_user.id:
        abort(403)

    form = EducationInstitutionForm(obj=institution)
    form.set_type_choices()
    form.set_author_choices()

    form.author_id.data = institution.author_id
    form.author_id.render_kw = {"disabled": "disabled"}

    if form.validate_on_submit():
        institution.name = form.name.data
        institution.address = form.address.data
        institution.description = form.description.data
        institution.type_id = form.type_id.data

        db.session.commit()
        flash("Institution updated successfully.", "success")
        return redirect(url_for("institutions.list_institutions"))

    return render_template("institutions/edit_institution.html", form=form)

@institutions_bp.route("/institutions/<int:id>/delete", methods=["POST"])
def delete_institution(id):
    institution = EducationInstitution.query.get_or_404(id)

    if institution.author_id != current_user.id:
        abort(403)

    db.session.delete(institution)
    db.session.commit()
    flash("Institution deleted successfully.", "success")
    return redirect(url_for("institutions.list_institutions"))

@institutions_bp.route("/types/<int:id>/edit", methods=["GET", "POST"])
def edit_type(id):
    institution_type = InstitutionType.query.get_or_404(id)
    form = InstitutionTypeForm(obj=institution_type)

    if form.validate_on_submit():
        institution_type.type_name = form.type_name.data
        institution_type.description = form.description.data

        db.session.commit()
        flash("Institution type updated successfully.", "success")
        return redirect(url_for("institutions.list_institution_types"))

    return render_template("types/edit_type.html", form=form, type=institution_type)



@institutions_bp.route("/types/<int:id>/delete", methods=["POST"])
def delete_type(id):
    institution_type = InstitutionType.query.get_or_404(id)

    db.session.delete(institution_type)
    db.session.commit()

    flash("Institution type deleted successfully.", "success")
    return redirect(url_for("institutions.list_institution_types"))
