from django.contrib.staticfiles.finders import AppDirectoriesFinder


class MustacheTemplateFinder(AppDirectoriesFinder):
    """
    Static files finder to locate mustache template files.
    """
    source_dir = 'mustachetemplates'
