def process(app, plugin_config):
    hj_id = plugin_config["ID"]

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
