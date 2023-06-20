"""
Theme
"""

from . import pywal_util


class Theme:
    """Theme"""

    def __init__(self):
        """Initialize theme"""
        self.list = pywal_util.get_theme_list()

    def get(self):
        """Get list themes"""
        return self.list

    def get_color(self, category, name):
        """Get theme's colors by category and name"""
        return pywal_util.get_theme(category, name)["colors"]
