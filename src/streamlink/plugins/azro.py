import logging
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate, useragents
from streamlink.stream.hls import HLSStream
from functools import partial

log = logging.getLogger(__name__)

@pluginmatcher(re.compile(r"""
    http://azrotv.com/m3u8/m/?
""", re.VERBOSE))

class AzroTV(Plugin):
        _re_hls = re.compile(r"""file\s*:\s*(["'])(?P<hls_url>https?://.*?\.m3u8.*?)\1""")
        def _get_streams(self):
            hls_url = self.session.http.get(self.url, schema=validate.Schema(
                validate.transform(self._re_hls.search),
                validate.any(None, validate.get("hls_url"))
            ))
            if not hls_url:
                log.error("Not a correct 'jwplayer/azro' iframe")
                return

            return {"live": HLSStream(self.session, hls_url)}


__plugin__ = AzroTV