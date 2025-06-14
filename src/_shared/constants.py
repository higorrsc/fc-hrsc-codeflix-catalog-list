import os

DEFAULT_PAGINATION_SIZE = 5

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
ELASTICSEARCH_HOST_TEST = os.getenv("ELASTICSEARCH_TEST_HOST", "http://localhost:9201")
ELASTICSEARCH_CATEGORY_INDEX = "catalog-db.codeflix.categories"
ELASTICSEARCH_CAST_MEMBER_INDEX = "catalog-db.codeflix.cast_members"
ELASTICSEARCH_GENRE_INDEX = "catalog-db.codeflix.genres"
ELASTICSEARCH_GENRE_CATEGORIES_INDEX = "catalog-db.codeflix.genre_categories"
ELASTICSEARCH_VIDEO_INDEX = "catalog-db.codeflix.videos"
