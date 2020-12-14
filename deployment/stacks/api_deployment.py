from aws_cdk import core
from aws_cdk import aws_apigateway


class APIDeploymentStack(core.NestedStack):
    def __init__(
        self,
        scope,
        *,
        rest_api_id,
        root_resource_id,
        methods=None,
        parameters=None,
        timeout=None
    ):
        super().__init__(
            scope,
            "DeployStack",
            parameters=parameters,
            timeout=timeout,
        )

        deployment = aws_apigateway.Deployment(
            self,
            "Deployment",
            api=aws_apigateway.LambdaRestApi.from_rest_api_attributes(
                self,
                "RestAPI",
                rest_api_id=rest_api_id,
                root_resource_id=root_resource_id,
            ),
        )

        if methods is not None:
            for method in methods:
                deployment.node.add_dependency(method)

        self.deploy(deployment)


class APIProdDeploymentStack(APIDeploymentStack):
    def deploy(self, deployment: aws_apigateway.Deployment) -> aws_apigateway.Stage:
        return aws_apigateway.Stage(
            self,
            "ProdStage",
            deployment=deployment,
            stage_name="prod",
            tracing_enabled=True,
            metrics_enabled=True,
        )


class APIDevDeploymentStack(APIDeploymentStack):
    def deploy(self, deployment: aws_apigateway.Deployment) -> aws_apigateway.Stage:
        return aws_apigateway.Stage(
            self,
            "DevStage",
            deployment=deployment,
            stage_name="dev",
            tracing_enabled=False,
            metrics_enabled=False,
        )