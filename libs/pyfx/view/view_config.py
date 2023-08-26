from dataclasses import dataclass

from rp.libs.pyfx.view.keymapper.keymapper_config import KeyMapperConfiguration
from rp.libs.pyfx.view.theme.theme_config import ThemeConfiguration


@dataclass(frozen=True)
class ViewConfiguration:
    appearance: ThemeConfiguration = ThemeConfiguration()
    keymap: KeyMapperConfiguration = KeyMapperConfiguration()
