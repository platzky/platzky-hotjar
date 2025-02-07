from typing import Any, Dict


from platzky.platzky import create_app_from_config, Config

from bs4 import BeautifulSoup, Tag

def test_plugin_loader():

    secret_id_for_testing = "super_secret_id"

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
                                                  "ID": secret_id_for_testing}}
                ],
            },
        },
    }

    hotjar_function ="(function(h,o,t,j,a,r){"

    config_with_plugin = Config.model_validate(data_with_plugin)
    app_with_plugin = create_app_from_config(config_with_plugin)
    response = app_with_plugin.test_client().get("/")
    # soup = BeautifulSoup(response.data, "html.parser")
    # print(soup.prettify())
    decoded_response = response.data.decode()
    assert hotjar_function in decoded_response and secret_id_for_testing in decoded_response
    # if hotjar_function in decoded_response and secret_id_for_testing in decoded_response:
    #     print("\nsuper_secret_id\n")
    #     print("super_secret_id")
    assert response.status_code == 404

