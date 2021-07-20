from __future__ import unicode_literals

from rp.prompt_toolkit.filters import Filter

__all__ = (
    'HasSignature',
    'ShowSidebar',
    'ShowDocstring',
)


class PythonInputFilter(Filter):
    def __init__(self, python_input):
        self.python_input = python_input

    def __call__(self, cli):
        raise NotImplementedError


class HasSignature(PythonInputFilter):
    def __call__(self, cli):
        return bool(self.python_input.signatures)


class ShowSidebar(PythonInputFilter):
    def __call__(self, cli):
        return self.python_input.show_sidebar

class ShowSignature(PythonInputFilter):
    def __call__(self, cli):
        return self.python_input.show_signature


class ShowDocstring(PythonInputFilter):
    def __call__(self, cli):
        return self.python_input.show_docstring
class ShowRealtimeInput(PythonInputFilter):
    def __call__(self, cli):
        return self.python_input.show_realtime_input
class ShowVarSpace(PythonInputFilter):
    def __call__(self, cli):
        return self.python_input.show_vars
class ShowVarSpaceOrShowRealtimeInput(PythonInputFilter):
    def __call__(self, cli):
        return self.python_input.show_vars or self.python_input.show_realtime_input
class ShowVarSpaceAndShowRealtimeInput(PythonInputFilter):
    def __call__(self, cli):
        return self.python_input.show_vars and self.python_input.show_realtime_input
class ShowParenthesisAutomator(PythonInputFilter):
    def __call__(self, cli):
        return self.python_input.show_parenthesis_automator and self.python_input.show_parenthesis_automator
class ShowLastAssignable(PythonInputFilter):
    def __call__(self, cli):
        return hasattr(self.python_input,'show_last_assignable') and self.python_input.show_last_assignable 
class ShowBatteryLife(PythonInputFilter):
    def __call__(self, cli):
        return hasattr(self.python_input,'show_battery_life') and self.python_input.show_battery_life 
