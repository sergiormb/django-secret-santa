from django.utils import translation
from django.conf import settings


def activate_lang(lang_code):
    lang_mapping = settings.LANGUAGE_MAPPING
    if lang_code in lang_mapping:
        lang_code = lang_mapping[lang_code]
    if lang_code:
        translation.activate(lang_code)


class LocaleMiddleware(object):
    """Middleware to check if we want to change language"""

    def process_request(self, request):
        forced_lang = request.GET.get('set_language', None)
        if forced_lang:
            activate_lang(forced_lang)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        forced_lang = request.GET.get('set_language', None)
        if forced_lang:
            get = request.GET.copy()
            get.pop('set_language')
            request.GET = get
            if translation.check_for_language(forced_lang):
                if hasattr(request, 'session'):
                    request.session[settings.LANGUAGE_COOKIE_NAME] = (
                        forced_lang)
                else:
                    response.set_cookie(
                        settings.LANGUAGE_COOKIE_NAME, forced_lang)
        return response
