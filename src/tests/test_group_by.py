import sys
import os
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
import logging
import unittest
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


@beam.ptransform_fn
def GroupBy(pcoll):
    return (
        pcoll
        | 'Pair with One' >> beam.Map(lambda x: (x, 1))
        | "Set Window" >> beam.WindowInto(beam.window.Sessions(1.0))
        | "Group By Key" >> beam.GroupByKey()
        | "Extract Message" >> beam.Map(lambda x: (x[0]))
    )


class GroupByKeyTest(unittest.TestCase):
    def test_group_by(self):
        options = PipelineOptions()
        options.view_as(StandardOptions).streaming = True
        with TestPipeline(options=options) as p:
            data = p | beam.Create([json.dumps({"key": "value"})])
            output = data | GroupBy()
            assert_that(
                output,
                equal_to([json.dumps({"key": "value"})])
            )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()
