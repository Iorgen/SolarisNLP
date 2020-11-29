from flask_restplus import fields, Model, reqparse
import werkzeug


recognizer_response_fields = Model('RecognizerOut', {
    "closest_person_ids": fields.List(fields.Integer)
})

recognize_in_group_fields = Model('RecognizerInGroup', {
    'photo_id': fields.String,
    'person_id': fields.String,
    'service_id': fields.Integer,
    'group_ids': fields.List(
        fields.Integer
    )
})

# -----------

science_job_encoder = reqparse.RequestParser()
science_job_encoder.add_argument('user_id', type=int)
science_job_encoder.add_argument('title', type=str)

project_encoder = reqparse.RequestParser()
project_encoder.add_argument('project_id', type=int)
project_encoder.add_argument('title', type=str)

keyword_extractor = reqparse.RequestParser()
keyword_extractor.add_argument('title', type=str)
keyword_extractor.add_argument('length', type=int)

recognizer_by_group_parser = reqparse.RequestParser()
recognizer_by_group_parser.add_argument('photo_id', type=str)
recognizer_by_group_parser.add_argument('person_id', type=str)
recognizer_by_group_parser.add_argument('group_ids', action='append', type=int)
recognizer_by_group_parser.add_argument('service_id', type=int)
