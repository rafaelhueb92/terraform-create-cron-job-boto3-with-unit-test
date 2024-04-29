import boto3
import unittest
from moto import mock_lambda, mock_events

class TestCreateCronJob(unittest.TestCase):

    @mock_lambda
    @mock_events
    def test_create_cron_job(self):
        lambda_client = boto3.client('lambda', region_name='us-east-1')
        event_client = boto3.client('events', region_name='us-east-1')

        # Crie uma função lambda de destino simulada
        lambda_client.create_function(
            FunctionName='TargetLambda',
            Runtime='python3.8',
            Role='arn:aws:iam::123456789012:role/service-role/lambda-role',
            Handler='lambda_function.lambda_handler',
            Code={
                'ZipFile': b'bytes'
            }
        )

        # Crie o cron job
        create_cron_job(lambda_client, event_client, 'cron(0/2 * * * ? *)', 'arn:aws:lambda:us-east-1:123456789012:function:TargetLambda')

        # Verifique se a regra de evento foi criada corretamente
        response = event_client.list_rules(NamePrefix='EvenBridgeCronJob')
        self.assertEqual(len(response['Rules']), 1)
        rule_arn = response['Rules'][0]['Arn']

        # Verifique se o alvo foi atribuído corretamente à regra de evento
        targets = event_client.list_targets_by_rule(Rule=rule_arn)
        self.assertEqual(len(targets['Targets']), 1)
        self.assertEqual(targets['Targets'][0]['Arn'], 'arn:aws:lambda:us-east-1:123456789012:function:TargetLambda')

if __name__ == '__main__':
    unittest.main()