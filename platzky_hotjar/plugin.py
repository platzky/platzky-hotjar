"""Platzky Hotjar plugin — injects Hotjar tracking code into page head."""

import inspect
from typing import Any

from platzky.plugin.html_injector import HtmlInjectorPluginBase, PageSection
from pydantic import BaseModel, field_validator


class HotjarConfig(BaseModel):
    """Configuration model for the Hotjar plugin."""

    ID: str

    @field_validator("ID")
    @classmethod
    def validate_id_is_numeric(cls, v: str) -> str:
        """Validate that the Hotjar ID is a numeric string."""
        if not v.isdigit():
            raise ValueError("Hotjar ID must be a numeric string")
        return v


class HotjarPlugin(HtmlInjectorPluginBase):
    """Platzky plugin that injects Hotjar tracking code into the page head."""

    accepted_page_sections: frozenset[PageSection] = frozenset({"head"})

    def __init__(self, config: dict[str, Any]) -> None:
        """Validate the plugin configuration."""
        super().__init__(config)
        self.hotjar_config = HotjarConfig.model_validate(config)

    def get_head_html(self) -> str:
        """Return the Hotjar tracking script to inject into the page head."""
        hj_id = self.hotjar_config.ID

        return inspect.cleandoc(
            f"""
            <!-- Hotjar Tracking Code -->
            <script>
                (function(h,o,t,j,a,r){{
                    h.hj=h.hj||function(){{(h.hj.q=h.hj.q||[]).push(arguments)}};
                    h._hjSettings={{hjid: {hj_id}, hjsv: 6}};
                    a=o.getElementsByTagName('head')[0];
                    r=o.createElement('script');r.async=1;
                    r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
                    a.appendChild(r);
                }})(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
            </script>
            <!-- End Hotjar Tracking Code -->
        """
        )
