import numpy as np
import werkzeug
import json
import torch
from flask_restplus import Namespace, Resource, reqparse
from errors import FaceEncodingFail
from api.api_v1.recognizer.models import (
    recognizer_response_fields, recognize_in_group_fields,
    science_job_encoder, project_encoder, recognizer_by_group_parser, keyword_extractor
)
from recognizer.logic import (
    calculate_descriptor_from_phrase,
    extract_keywords_from_doc,
    make_random_sentence,
    extract_keyword,
    get_closest_desriptors_pairs
)
from db.db_create import (
    update_or_create_user_descriptor,
    save_science_job_object_into_db,
    save_project_object_into_db
)

from db.db_select import (
    get_all_science_job_embeddings_by_user_id,
    get_user_mapped_embeddings
)


api = Namespace('descriptors_encoding', description='Расчёт дескрипторов используя BERT модели')

# TODO Define Swagger Docs
api.models[recognizer_response_fields.name] = recognizer_response_fields
api.models[recognize_in_group_fields.name] = recognize_in_group_fields


@api.route('/extract/keywords')
class ExtractKeywords(Resource):
    """

    """
    @api.doc()
    @api.expect(keyword_extractor)
    @api.response(code=200, model=None, description='Success')
    def post(self):
        args = keyword_extractor.parse_args()
        title = args['title']
        length = args['length']
        keywords = extract_keywords_from_doc(doc=title, length=length)
        return {"keywords": keywords}, 200


@api.route('/encode/science_job')
class EncodeScienceJob(Resource):
    """

    """
    @api.doc()
    @api.expect(science_job_encoder)
    @api.response(code=200, model=None, description='Success')
    def post(self):
        args = science_job_encoder.parse_args()
        user_id = args['user_id']
        title = args['title']
        descriptor = calculate_descriptor_from_phrase(title)
        save_science_job_object_into_db(
            descriptor=descriptor,
            user_id=user_id
        )
        users_embeddings = get_all_science_job_embeddings_by_user_id(user_id=user_id).tolist()
        users_embeddings = torch.Tensor(users_embeddings)
        users_embeddings = users_embeddings.reshape(users_embeddings.shape[0], users_embeddings.shape[2])
        mean_user_embedding = torch.mean(users_embeddings, dim=-2)
        user_object = update_or_create_user_descriptor(
            user_id=user_id,
            descriptor=mean_user_embedding
        )
        return {
                   "new_mean_user_descriptor": mean_user_embedding.tolist(),
                   "science_job_descriptor": descriptor.tolist(),
               }, 200


@api.route('/encode/project')
class EncodeProject(Resource):
    """
    """

    @api.doc()
    @api.expect(project_encoder)
    @api.response(code=200, model=recognizer_response_fields, description='Success')
    def post(self):
        args = project_encoder.parse_args()
        project_id = args['project_id']
        title = args['title']
        # phrase = make_random_sentence()
        descriptor = calculate_descriptor_from_phrase(title)
        save_project_object_into_db(
            descriptor=descriptor,
            project_id=project_id
        )
        descriptors_list = get_user_mapped_embeddings()
        recommended_user_ids = get_closest_desriptors_pairs(
            main_tensor=descriptor,
            descriptors_list=descriptors_list,
            tolerance=14,
            capacity=5
        )
        return {
                   "closest_user_ids": recommended_user_ids.tolist()
               }, 200


@api.errorhandler(FaceEncodingFail)
def handle_custom_exception(error):
    """ Return a reason why sample is unprocessable based on error message """
    return {'message': error.message}, 415
