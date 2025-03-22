from rte import (
    Addon,
    register_addon_as_extension,
    RteEnv,
)
from .extension import EXTENSION_NAME
from .log import logger
from .audio_denoise_extension import AudioDenoiseExtension


@register_addon_as_extension(EXTENSION_NAME)
class AudioDenoiseExtensionAddon(Addon):
    def on_create_instance(self, rte: RteEnv, addon_name: str, context) -> None:
        logger.info("on_create_instance")
        rte.on_create_instance_done(AudioDenoiseExtension(addon_name), context)
