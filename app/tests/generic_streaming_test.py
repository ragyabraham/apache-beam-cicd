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

    def test_test_stream_errors(self):
        with self.assertRaises(
                AssertionError, msg=('Watermark must strictly-monotonically advance.')):
            _ = (TestStream().advance_watermark_to(5).advance_watermark_to(4))

        with self.assertRaises(
                AssertionError,
                msg=('Must advance processing time by positive amount.')):
            _ = (TestStream().advance_processing_time(-1))

        with self.assertRaises(
                AssertionError,
                msg=('Element timestamp must be before timestamp.MAX_TIMESTAMP.')):
            _ = (
                TestStream().add_elements(
                    [TimestampedValue('a', timestamp.MAX_TIMESTAMP)]))

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
                    ('a', timestamp.Timestamp(10)),
                    ('b', timestamp.Timestamp(10)),
                    ('c', timestamp.Timestamp(10)),
                    ('d', timestamp.Timestamp(20)),
                    ('e', timestamp.Timestamp(20)),
                    ('late', timestamp.Timestamp(12)),
                    ('last', timestamp.Timestamp(310)),
                ]))

    def test_multiple_outputs(self):
        """Tests that the TestStream supports emitting to multiple PCollections."""
        letters_elements = [
            TimestampedValue('a', 6),
            TimestampedValue('b', 7),
            TimestampedValue('c', 8),
        ]
        numbers_elements = [
            TimestampedValue('1', 11),
            TimestampedValue('2', 12),
            TimestampedValue('3', 13),
        ]
        test_stream = (
            TestStream()
            .advance_watermark_to(5, tag='letters')
            .add_elements(letters_elements, tag='letters')
            .advance_watermark_to(10, tag='numbers')
            .add_elements(numbers_elements, tag='numbers'))  # yapf: disable

        class RecordFn(beam.DoFn):
            def process(
                    self,
                    element=beam.DoFn.ElementParam,
                    timestamp=beam.DoFn.TimestampParam):
                yield (element, timestamp)

        options = StandardOptions(streaming=True)
        p = TestPipeline(options=options)

        main = p | test_stream
        letters = main['letters'] | 'record letters' >> beam.ParDo(RecordFn())
        numbers = main['numbers'] | 'record numbers' >> beam.ParDo(RecordFn())

        assert_that(
            letters,
            equal_to(
                [
                    ('a', timestamp.Timestamp(6)), ('b', timestamp.Timestamp(7)),
                    ('c', timestamp.Timestamp(8))]),
            label='assert letters')

        assert_that(
            numbers,
            equal_to(
                [
                    ('1', timestamp.Timestamp(11)), ('2', timestamp.Timestamp(12)),
                    ('3', timestamp.Timestamp(13))]),
            label='assert numbers')

        p.run()


if __name__ == '__main__':
    unittest.main()
