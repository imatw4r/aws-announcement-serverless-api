from aws_cdk import core

from deployment.stacks.app import AnnouncementAppProdStack, AnnouncementAppDevStack
from deployment.settings.base import AWS_ACCOUNT, AWS_REGION


def create_stack(app, is_prod=False):
    if is_prod:
        return AnnouncementAppProdStack(
            app,
            "prod-announcement-app",
            env={"account": AWS_ACCOUNT, "region": AWS_REGION},
        )
    return AnnouncementAppDevStack(
        app, "dev-announcement-app", env={"account": AWS_ACCOUNT, "region": AWS_REGION}
    )


if __name__ == "__main__":
    app = core.App()
    create_stack(app, is_prod=False)
    app.synth()
