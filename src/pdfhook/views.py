from flask import request, render_template, jsonify, Response, url_for
import io, os
from src.main import db
from src.pdfhook import (
    blueprint,
    tasks,
    queries,
    serializers
    )


pdf_serializer = serializers.PDFFormSerializer()

@blueprint.route('/', methods=['POST'])
def post_pdf():
    # get pdf
    if not request.files:
        abort(404)
    file_storage = request.files['file']
    filename = os.path.basename(file_storage.filename)
    temp_pdf_path = os.path.join(
        tasks.TEMP_FOLDER_PATH, 'tmp-' + filename)
    raw_pdf_data = file_storage.read()
    with open(temp_pdf_path, 'wb') as temp_pdf:
        temp_pdf.write(raw_pdf_data)
    field_definitions = tasks.build_fdf_map(temp_pdf_path)
    pdf = queries.create_pdf_form(
        original_pdf_title=filename,
        original_pdf=raw_pdf_data,
        fdf_mapping=field_definitions
        )
    return jsonify(pdf_serializer.dump(pdf).data)


@blueprint.route('/<int:pdf_id>/', methods=['POST'])
def fill_pdf(pdf_id):
    pdf = queries.get_pdf(id=pdf_id)
    data = request.get_json()
    results = tasks.fill_pdf(pdf, data)
    return Response(results)
