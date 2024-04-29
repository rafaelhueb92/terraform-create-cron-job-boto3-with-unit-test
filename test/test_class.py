import unittest
from unittest.mock import patch
from moto import mock_events
from lambda_function import create_cron_job

class TestCreateCronJob(unittest.TestCase):

    @mock_events
    @patch('boto3.client')
    def test_create_cron_job(self, mock_boto3_client):
        schedule_expression = 'cron(0/2 * * * ? *)'
        target_lambda_arn = 'arn:aws:lambda:us-east-1:123456789012:function:TargetLambda'
        role_arn = 'arn:aws:iam::123456789012:role/TestRole'

        # Mock boto3.client('events') method
        mock_events_client = mock_boto3_client.return_value
        mock_events_client.put_rule.return_value = {'RuleArn': 'mock_rule_arn'}
        mock_events_client.put_targets.return_value = {}

        create_cron_job(schedule_expression, target_lambda_arn, role_arn)

        # Check if put_rule was called correctly
        mock_events_client.put_rule.assert_called_once_with(
            Name='EvenBridgeCronJob',
            ScheduleExpression=schedule_expression,
            State='ENABLED'
        )

        # Check if put_targets was called correctly
        mock_events_client.put_targets.assert_called_once_with(
            Rule='mock_rule_arn',
            Targets=[
                {
                    'Id': 'TargetLambda',
                    'Arn': target_lambda_arn,
                    'RoleArn': role_arn
                }
            ]
        )

if __name__ == '__main__':
    unittest.main()
