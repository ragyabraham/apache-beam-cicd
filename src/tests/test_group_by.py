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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


def test_group_by():
    options = PipelineOptions()
    options.view_as(StandardOptions).streaming = True
    with TestPipeline(options=options) as p:
        output = (
            p
            |
        )

        assert_that(
            output,
            equal_to([])
        )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()
