from ast import literal_eval
from sqlalchemy.ext.declarative import declared_attr
import datetime

from app import db


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Form %s' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all forms"""
        forms = Form.query.all()
        data = []
        for form in forms:
            obj = {
                'id': form.id,
                'name': form.name,

            }
            data.append(obj)
        return data

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_detail_information(self):
        """Return detail info about form"""
        field_data = list()
        for key, field_type in FIELD_TYPES.items():
            items = field_type.query.filter_by(form_id=self.id).all()
            if items:
                for item in items:
                    field_data.append({'id': item.id, 'type_field': key, 'name': item.name,
                                       'value': item.get_value()})
        data = {"name": self.name, "id": self.id, "fields": field_data}
        return data

    def submit_form(self, fields):
        """Validate form fields"""
        for item in fields:
            dict_item = literal_eval(item)
            field = FIELD_TYPES.get(dict_item.get('type_field')) \
                .query.filter_by(id=dict_item.get('id')).first()
            if field:
                if field.form_id != self.id:
                    return {'status': 'error',
                            'message': '%s field with id = %i does''not  consist'
                                       'in form with id = %i'
                                       % (dict_item.get('type_field'),
                                          dict_item.get('id'),
                                          self.id)}
                if field.is_valid(dict_item.get('value')):
                    field.save()
                else:
                    return {'status': 'error',
                            'message': 'invalid value'
                                       ' for %s field with id = %i'
                                       % (dict_item.get('type_field'),
                                          dict_item.get('id'))}
        return {'status': 'ok'}


class Field(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    @declared_attr
    def form_id(self):
        return db.Column(db.Integer, db.ForeignKey('form.id'),
                         nullable=False)

    def __repr__(self):
        return 'Field %s' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def create_field(name, form_id, type_field):
        """Create needed field object"""
        if type_field in FIELD_TYPES:
            if not Form.query.filter_by(id=form_id).first():
                return {'status': 'error', 'message': 'form with this id does''not exist'}
            field = FIELD_TYPES.get(type_field)
            obj = field(name, form_id)
            obj.save()
            return {'status': 'success', 'field': obj}
        return {'status': 'error', 'message': 'invalid field type'}


class IntegerField(Field):
    value = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return 'IntegerField %s' % self.name

    def __init__(self, name, form_id, value=None):
        self.name = name
        self.form_id = form_id
        self.value = value

    def obj_to_dict(self):
        return {'id': self.id, 'name': self.name, 'form_id': self.form_id,
                'value': self.value, 'type': 'Integer'}

    def is_valid(self, value):
        if value:
            if isinstance(value, int):
                self.value = value
                return True
        return False

    def get_value(self):
        return self.value


class StringField(Field):
    value = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return 'StringField %s' % self.name

    def __init__(self, name, form_id, value=None):
        self.name = name
        self.form_id = form_id
        self.value = value

    def obj_to_dict(self):
        return {'id': self.id, 'name': self.name, 'form_id': self.form_id,
                'value': self.value, 'type': 'Text'}

    def is_valid(self, value):
        if value:
            if isinstance(value, str):
                self.value = value
            return True
        return False

    def get_value(self):
        return self.value


class DateField(Field):
    value = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return 'DateField %s' % self.name

    def __init__(self, name, form_id, value=None):
        self.name = name
        self.form_id = form_id
        self.value = value

    def obj_to_dict(self):
        return {'id': self.id, 'name': self.name, 'form_id': self.form_id,
                'value': self.get_value(), 'type': 'Date'}

    def is_valid(self, value):
        if value:
            try:
                date = datetime.datetime.strptime(value, '%Y-%m-%d')
                self.value = date
                return True
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        else:
            return True

    def get_value(self):
        if self.value:
            return datetime.datetime.strftime(self.value, '%Y-%m-%d')
        else:
            return None


# available field types
FIELD_TYPES = {
    'number': IntegerField,
    'text': StringField,
    'date': DateField,
}
