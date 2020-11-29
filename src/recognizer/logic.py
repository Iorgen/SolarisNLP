import cv2
import pandas as pd
from errors import FaceEncodingFail
from typing import Union
from keybert import KeyBERT
import torch
import numpy as np
from torch import nn
import db.db_select
import db.db_create
import logging
import torch

logger = logging.getLogger(__name__)

model = KeyBERT('distilbert-base-nli-mean-tokens')
# TODO implement all logic

import random


def make_random_sentence():
  nouns = ["puppy", "car", "rabbit", "girl", "monkey"]
  verbs = ["runs", "hits", "jumps", "drives", "barfs"]
  adv = ["crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally."]
  adj = ["adorable", "clueless", "dirty", "odd", "stupid"]

  random_entry = lambda x: x[random.randrange(len(x))]
  return " ".join([random_entry(nouns), random_entry(verbs), random_entry(adv), random_entry(adj)])


def extract_keywords_from_doc(doc: str, length: int):
    keywords = model.extract_keywords(doc, keyphrase_length=length)
    return keywords


def calculate_descriptor_from_phrase(phrase: str):
    pytens_descriptor = model.extract_query_tensor_embedding(
        phrase
    )
    return pytens_descriptor.reshape(1, pytens_descriptor.shape[0])


def get_closest_desriptors_pairs(
        main_tensor: torch.Tensor,
        descriptors_list: pd.DataFrame,
        tolerance: int = 14,
        capacity: int = 10
):
    logger.info('start finding closest employees')
    banners_descriptor = None
    banner_distance = None
    # TODO should check if all of that is working
    base_entity_descriptors = torch.Tensor([np.array(i) for i in descriptors_list.embedding.values])
    # Comment
    banner_distance = torch.pairwise_distance(main_tensor, base_entity_descriptors).cpu().numpy()
    # Comment
    distance = list(banner_distance)
    # TODO if length < capacity take length
    founded_distances = []
    most_similar_base_banner_indexes = []
    for _cap in range(capacity):
        founded_distances.append(sorted(distance)[_cap])
        most_similar_base_banner_indexes.append(distance.index(sorted(distance)[_cap]))
    target_class_ids = descriptors_list['user_id'][most_similar_base_banner_indexes]
    return target_class_ids


def extract_keyword(title: str, length: int):
    return model.extract_keywords(title, keyphrase_length=length)


# TODO For calculation between author articles torch.mean(a, dim=-2) or  torch.mean(a, dim=0)
# How to fill citation matrix

# I will get phrase
# select all encoded tensors from database to get all of them with id
# Find 10 closest

# TODO База авторов
# Прикрепленны научные статьи этого автора
# класссификация и название научной статьи
# У каждой есть список цитирований - цитирование идет на другие

# TODO co-citation network
# TODO algorithm
# статья - (10 статей)
# класссификация и название научной статьи
# + ---- =
#
# Статья 1 - векторное представление названия
# Статья 2 - векторное представление названия
#
# Статьи соавторов - векторное представление название
# + Векторное представление
#
# цитируемой статьи 1 - векторное представление названия
# цитируемой статьи 2 - векторное представление названия
# цитируемой статьи 3 - векторное представление названия
# цитируемой статьи 4 - векторное представление названия

# Also i need to use this when search
# banners_distance[banner_id] = torch.pairwise_distance(banners_descriptors[i],
#                                                               base_banners_de