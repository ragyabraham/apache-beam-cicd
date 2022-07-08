import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.test_stream import TestStream
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
from apache_beam.transforms.window import TimestampedValue
from apache_beam.utils import timestamp
import unittest


def test_basic_execution(self):
    test_stream = (
        TestStream()
        .advance_watermark_to(10)
        .add_elements(['a', 'b', 'c'])
        .advance_watermark_to(20)
        .add_elements(['d'])
        .add_elements(['e'])
        .advance_processing_time(10)
        .advance_watermark_to(300)
        .add_elements([TimestampedValue('late', 12)])
        .add_elements([TimestampedValue('last', 310)])
        .advance_watermark_to_infinity()
    )  # yapf: disable

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
                ('a', timestamp.Timestamp(10)),
                ('b', timestamp.Timestamp(10)),
                ('c', timestamp.Timestamp(10)),
                ('d', timestamp.Timestamp(20)),
                ('e', timestamp.Timestamp(20)),
                ('late', timestamp.Timestamp(12)),
                ('last', timestamp.Timestamp(310)),
            ]))


if __name__ == '__main__':
    unittest.main()
