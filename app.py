from aws_cdk import core

from deployment.stacks.app import AnnouncementAppProdStack, AnnouncementAppDevStack
from deployment.settings.base import IS_PROD
import deployment.settings.prod as prod_settings
import deployment.settings.dev as dev_settings


def create_stack(app, is_prod=False):
    if is_prod:
        return AnnouncementAppProdStack(
            app,
            "prod-announcement-app",
            settings=prod_settings,
            env={
                "account": prod_settings.AWS_ACCOUNT,
                "region": prod_settings.AWS_REGION,
            },
        )
    return AnnouncementAppDevStack(
        app,
        "dev-announcement-app",
        settings=dev_settings,
        env={"account": dev_settings.AWS_ACCOUNT, "region": dev_settings.AWS_REGION},
    )


if __name__ == "__main__":
    app = core.App()
    create_stack(app, is_prod=IS_PROD)
    app.synth()
