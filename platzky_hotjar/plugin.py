"""Platzky Hotjar plugin — injects Hotjar tracking code into page head."""

from typing import cast

from platzky.engine import Engine
from platzky.plugin.plugin import PluginBase, PluginBaseConfig


class HotjarConfig(PluginBaseConfig):
    """Configuration model for the Hotjar plugin."""

    ID: str


class HotjarPlugin(PluginBase[HotjarConfig]):
    """Platzky plugin that injects Hotjar tracking code into the page head."""

    @classmethod
    def get_config_model(cls) -> type[HotjarConfig]:
        """Return the config model class for this plugin."""
        return HotjarConfig

    def process(self, app: Engine) -> Engine:
        """Inject Hotjar tracking script into the app's dynamic head."""
        config = cast(HotjarConfig, self.config)
        hj_id = config.ID

        head_code = (
            """<!-- Hotjar Tracking Code -->
        <script>
            (function(h,o,t,j,a,r){
                h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
                h._hjSettings={hjid: """
            + hj_id
            + """, hjsv: 6};
                a=o.getElementsByTagName('head')[0];
                r=o.createElement('script');r.async=1;
                r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
                a.appendChild(r);
            })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
        </script>
        <!-- End Hotjar Tracking Code -->
    """
        )
        app.add_dynamic_head(head_code)

        return app
