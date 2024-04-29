import boto3
import unittest
from moto import mock_lambda, mock_events

# Função para criar um cron job que chama outra função lambda
def create_cron_job(lambda_client, event_client, schedule_expression, target_lambda_arn):
    rule_name = 'EvenBridgeCronJob'
    target_id = 'TargetLambda'

    response = event_client.put_rule(
        Name=rule_name,
        ScheduleExpression=schedule_expression,
        State='ENABLED'
    )

    event_client.put_targets(
        Rule=response['RuleArn'],
        Targets=[
            {
                'Id': target_id,
                'Arn': target_lambda_arn,
            }
        ]
    )