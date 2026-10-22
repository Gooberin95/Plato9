import reflex as rx

config = rx.Config(
    app_name="halcyon",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="dark",
                accent_color="gold",
                gray_color="sand",
                radius="large",
                has_background=False,
                panel_background="translucent",
            )
        ),
    ],
)