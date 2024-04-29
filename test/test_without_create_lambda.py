import boto3
import handler

def test_create_cron_job(self):
        schedule_expression = 'cron(0/2 * * * ? *)'
        target_lambda_arn = 'arn:aws:lambda:us-east-1:123456789012:function:TargetLambda'
        role_arn = 'arn:aws:iam::123456789012:role/TestRole'

        handler.create_cron_job(schedule_expression, target_lambda_arn, role_arn)

        # Verifique se a regra de evento foi criada corretamente
        event_client = boto3.client('events')
        response = event_client.list_rules(NamePrefix='EvenBridgeCronJob')
        self.assertEqual(len(response['Rules']), 1)
        rule_arn = response['Rules'][0]['Arn']
