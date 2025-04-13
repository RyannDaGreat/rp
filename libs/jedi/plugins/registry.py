"""
This is not a plugin, this is just the place were plugins are registered.
"""

from rp.libs.jedi.plugins import stdlib
from rp.libs.jedi.plugins import flask
from rp.libs.jedi.plugins import plugin_manager


plugin_manager.register(stdlib, flask)
