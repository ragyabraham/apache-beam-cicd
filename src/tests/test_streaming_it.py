# import logging
# import unittest
# import os

# import pytest
# from hamcrest.core.core.allof import all_of

# from app import streaming_wordcount
# from apache_beam.io.gcp.tests.pubsub_matcher import PubSubMessageMatcher
# from apache_beam.runners.runner import PipelineState
# from apache_beam.testing.pipeline_verifiers import PipelineStateMatcher
# from apache_beam.testing.test_pipeline import TestPipeline


# INPUT_TOPIC = 'wc_topic_input'
# OUTPUT_TOPIC = 'wc_topic_output'
# INPUT_SUB = 'wc_subscription_input'
# OUTPUT_SUB = 'wc_subscription_output'

# DEFAULT_INPUT_NUMBERS = 5

# message = {
#     "eventType": "ruleCompleted",
#     "rule_name": "Pixels_monita",
#     "rule_id": "RLbd0b50167abd4de68f75040df959fdca",
#     "eventTimestamp": 1626413698,
#     "status": "ruleCompleted",
#     "action_modulePath": "facebook_pixel/src/lib/actions/sendCustomEvent.js",
#     "action_modulePath_sum": "facebook_pixel/sendCustomEvent",
#     "condition_modulePath": "",
#     "condition_modulePath_sum": "",
#     "event_modulePath": "core/src/lib/events/pageBottom.js",
#     "event_modulePath_sum": "core/pageBottom",
#     "event_ruleOrder": "1",
#     "buildInfo_buildDate": 1626413679,
#     "buildInfo_environment": "production",
#     "buildInfo_minified": "false",
#     "buildInfo_turbineBuildDate": 1619456068,
#     "buildInfo_turbineVersion": "27.1.3",
#     "company_orgId": "36DE0D2C5C867DCE0A495CC9@AdobeOrg",
#     "property_name": "Monita",
#     "session_id": "",
#     "user_id": "ragyabraham",
#     "segment_id": "",
#     "ip_address": "",
#     "url": "https://www.getmonita.io/"
# }


# class StreamingWordCountIT(unittest.TestCase):
#     def setUp(self):
#         os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./app/keys/k8s_owner_key.json"
#         self.test_pipeline = TestPipeline()
#         self.topic = 'beam-summit-testing'

#     def _publish_message(self, message, user_agent):
#         from google.cloud import pubsub
#         import google.auth
#         import json
#         self.credentials, self.project = google.auth.default(
#             scopes=["https://www.googleapis.com/auth/cloud-platform"]
#         )
#         message['user_agent'] = user_agent
#         publisher = pubsub.PublisherClient()
#         topic_path = publisher.topic_path(self.project, self.topic)
#         data = json.dumps(message).encode('utf-8')
#         future = publisher.publish(
#             topic_path, data)
#         if future._exception is None:
#             print(f"Published messages to '{topic_path}' topic")
#             return True
#         else:
#             raise Exception(future._exception)

#     @pytest.mark.it_postcommit
#     def test_streaming_wordcount_it(self):
#         # TODO: Need to Build expected row from BQ
#         expected_msg = []

#         # Set extra options to the pipeline for test purpose
#         state_verifier = PipelineStateMatcher(PipelineState.RUNNING)
#         pubsub_msg_verifier = PubSubMessageMatcher(
#             self.project, self.output_sub.name, expected_msg, timeout=400)
#         extra_opts = {
#             'input_subscription': self.input_sub.name,
#             'output_topic': self.output_topic.name,
#             'on_success_matcher': all_of(state_verifier, pubsub_msg_verifier)
#         }

#         # Generate input data and inject to PubSub.
#         self._inject_numbers(self.input_topic, DEFAULT_INPUT_NUMBERS)

#         # Get pipeline options from command argument: --test-pipeline-options,
#         # and start pipeline job by calling pipeline main function.
#         streaming_wordcount.run(
#             self.test_pipeline.get_full_options_as_args(**extra_opts),
#             save_main_session=False)


# if __name__ == '__main__':
#     logging.getLogger().setLevel(logging.DEBUG)
#     unittest.main()
