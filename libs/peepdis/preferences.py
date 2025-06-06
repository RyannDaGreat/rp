class _PreferencesMixin:
    _color_scheme = {
        "error": "red",
        "callable_": "cyan",
        "attr": "magenta",
        "message": "white",
        "null": "grey",
        "forged": "yellow",
        "specified": "orange",
        "default": "grey",
        "None": "grey",
        "builtin": "grey",
    }
    _display_type_annotations = True

    @classmethod
    def _load_preferences(cls):
        pass

    @classmethod
    def _update_color_scheme(cls, key, value):
        cls._color_scheme[key] = value
