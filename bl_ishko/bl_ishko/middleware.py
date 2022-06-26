from django.shortcuts import render
from loguru import logger


class ErrorLogMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f'Error middleware: {exception}')
        return render(request, 'shop/404.html')
