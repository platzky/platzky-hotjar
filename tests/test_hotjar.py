from typing import Any, Dict


from platzky.platzky import create_app_from_config, Config

from bs4 import BeautifulSoup, Tag

def test_plugin_loader():
    data_with_plugin: Dict[str, Any] = {
        "APP_NAME": "testingApp",
        "SECRET_KEY": "secret",
        "USE_WWW": False,
        "BLOG_PREFIX": "/",
        "TRANSLATION_DIRECTORIES": ["/some/fake/dir"],
        "DB": {
            "TYPE": "json",
            "DATA": {
                "site_content": {"pages": []},
                "plugins": [
                    {"name": "hotjar", "config": {"/page/test": "/page/test2",
                                                  "ID": "super_secret_id"}}
                ],
            },
        },
    }
    config_with_plugin = Config.model_validate(data_with_plugin)
    app_with_plugin = create_app_from_config(config_with_plugin)
    response = app_with_plugin.test_client().get("/")
    soup = BeautifulSoup(response.data, "html.parser")
    print(soup.prettify())
    # assert soup.title is not None
    # assert soup.title.string == "testing App Name"
    # print(response.data.decode())
    if "super_secret_id" in response.data.decode():
        print("\nsuper_secret_id\n")
        print("super_secret_id")
    assert response.status_code == 404
    # assert response.location == "/page/test2"

