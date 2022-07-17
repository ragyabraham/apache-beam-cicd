import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.test_stream import TestStream
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
from apache_beam.transforms.window import TimestampedValue, WindowedValue
from apache_beam.testing.test_stream import ProcessingTimeEvent, ElementEvent, WatermarkEvent
from apache_beam.utils import timestamp
import unittest

"""Notes:
    advancing to watermark to infinity closes the stream
    This will advance the stream to "end of time"
"""


class TestStreamTest(unittest.TestCase):
    def test_basic_test_stream(self):
        test_stream = (
            TestStream()
            .advance_watermark_to(0)
            .add_elements([
                'a',
                WindowedValue('b', 3, []),
                TimestampedValue('c', 6)])
            .advance_processing_time(10)
            .advance_watermark_to(8)
            .add_elements(['d'])
            .advance_watermark_to_infinity())  # yapf: disable
        self.assertEqual(
            test_stream._events,
            [
                WatermarkEvent(0),
                ElementEvent([
                    TimestampedValue('a', 0),
                    TimestampedValue('b', 3),
                    TimestampedValue('c', 6),
                ]),
                ProcessingTimeEvent(10),
                WatermarkEvent(8),
                ElementEvent([
                    TimestampedValue('d', 8),
                ]),
                WatermarkEvent(timestamp.MAX_TIMESTAMP),
            ])

    def test_basic_execution(self):
        test_stream = (
            TestStream()
            .advance_watermark_to(10)
            .add_elements([{"rule_id": "RLbd0b50167abd4de68f75040df959fdca"}, {"eventTimestamp": 1626413698}])
            .advance_watermark_to(20)
            .add_elements([{"status": "ruleCompleted"}])
            .add_elements([{"user_id": "ragyabraham"}])
            .advance_processing_time(10)
            .advance_watermark_to(300)
            .add_elements([TimestampedValue('late_data_1', 12)])
            .add_elements([TimestampedValue('last_data_2', 310)])
            .advance_watermark_to_infinity())  # yapf: disable

        class RecordFn(beam.DoFn):
            def process(
                    self,
                    element=beam.DoFn.ElementParam,
                    timestamp=beam.DoFn.TimestampParam):
                yield (element, timestamp)

        options = PipelineOptions()
        options.view_as(StandardOptions).streaming = True
        with TestPipeline(options=options) as p:
            my_record_fn = RecordFn()
            records = p | test_stream | beam.ParDo(my_record_fn)

            assert_that(
                records,
                equal_to([
                    ({'rule_id': 'RLbd0b50167abd4de68f75040df959fdca'},
                     timestamp.Timestamp(10)),
                    ({'eventTimestamp': 1626413698}, timestamp.Timestamp(10)),
                    ({'status': 'ruleCompleted'}, timestamp.Timestamp(20)),
                    ({'user_id': 'ragyabraham'}, timestamp.Timestamp(20)),
                    ('late_data_1', timestamp.Timestamp(12)),
                    ('last_data_2', timestamp.Timestamp(310)),
                ]))
        p.run()
