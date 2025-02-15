from collections import OrderedDict
from django.urls import re_path, path
from rest_framework_nested.routers import DefaultRouter, SimpleRouter


class CustomRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        self.custom_root = {}
        super().__init__(*args, **kwargs)
    
    def add_custom_root(self, prefix, view, basename):
        self.custom_root[prefix] = {"name": basename, "view": view}
    
    
    def get_api_root_view(self, api_urls=None):
        """
        Return a basic root view.
        """
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)
        
        if self.custom_root:
            for prefix in self.custom_root:
                api_root_dict[prefix] = self.custom_root[prefix]["name"]

        return self.APIRootView.as_view(api_root_dict=api_root_dict)
    
    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
            for prefix in self.custom_root:
                self._urls.append(path(f'{prefix}/', self.custom_root[prefix]["view"], name=self.custom_root[prefix]["name"]))

        return self._urls
