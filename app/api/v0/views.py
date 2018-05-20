from flask_restful import Resource, reqparse

from app.models import Form, FIELD_TYPES, Field

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('id', type=int)
parser.add_argument('type', type=str)
parser.add_argument('form_id', type=int)
parser.add_argument('fields', action='append')


class FormView(Resource):

    def get(self):
        """Get all forms"""
        forms = Form.get_all()
        if not forms:
            return '', 404
        return forms, 200

    def post(self):
        """Create form"""
        args = parser.parse_args()
        name = args.get('name')
        if name:
            form = Form(name=name)
            form.save()
            return {'id': form.id, 'name': form.name}, 201
        else:
            return {'error': 'name is required argument'}, 400


class FormDetailView(Resource):

    def get(self, id):
        """Get detail information about form"""
        form = Form.query.filter_by(id=id).first()
        if form:
            return form.get_detail_information(), 200
        else:
            return '', 404


class FieldView(Resource):

    def get(self):
        """Get available types of fields"""
        return list(FIELD_TYPES.keys()), 200

    def post(self):
        """Add field to form"""
        args = parser.parse_args()
        type_field = args.get('type')
        name = args.get('name')
        form_id = args.get('form_id')
        if form_id and name and type_field:
            result = Field.create_field(name, form_id, type_field)
            if result.get('status') == 'success':
                return result.get('field').obj_to_dict(), 200
            else:
                return result, 400
        else:
            return {'status': 'error', 'message': 'Name, type, form_id'
                                                  ' are required parameters'}


class FormSubmitView(Resource):

    def post(self, id):
        """Submit form"""
        args = parser.parse_args()
        fields = args.get('fields')
        if not fields:
            return {'status': 'error', 'message': 'parameter fields are required'}, 400
        form = Form.query.filter_by(id=id).first()
        if not form:
            return {'status': 'error', 'message': 'form with this id does''not exist'}, 400
        result = form.submit_form(fields)
        if result['status'] == 'ok':
            return form.get_detail_information(), 200
        else:
            return result, 400
