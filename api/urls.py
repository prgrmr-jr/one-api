from django.urls import path

from . import views

urlpatterns = [
    path('dev-rex/api-key=<str:api_key>/chat=<str:prompt>', views.dev_rex_ai, name='dev_rex_ai'),
    path('perp/api-key=<str:api_key>/chat=<str:prompt>', views.perp_ai, name='perp_ai'),
    path('bert/api-key=<str:api_key>/chat=<str:prompt>', views.bert_ai, name='bert_ai'),
    path('gemini/api-key=<str:api_key>/chat=<str:prompt>', views.gemini_ai, name="gemini_ai"),
    path(
        'mp3/yt-key=<str:yt_key>/cloud-name=<str:cloud_name>/cloud-key=<str:cloud_key>/secret-key=<str:secret_key>/search=<str:search_prompt>',
        views.youtube_music_downloader, name="youtube_mp3")
]
