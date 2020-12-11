#!/usr/bin/env python3

from aws_cdk import core

from announcement_app.announcement_app_stack import AnnouncementAppStack


app = core.App()
AnnouncementAppStack(app, "announcement-app")

app.synth()
