from aws_cdk import core

from deployment.stacks.app import AnnouncementAppStack


if __name__ == "__main__":
    app = core.App()
    AnnouncementAppStack(app, "announcement-app")

    app.synth()
