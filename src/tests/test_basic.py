from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
import logging
import unittest
import apache_beam as beam


class CountTest(unittest.TestCase):

    def test_count(self):
        # Our static input data, which will make up the initial PCollection.
        WORDS = [
            "hi", "there", "hi", "hi", "sue", "bob",
            "hi", "sue", "", "", "ZOW", "bob", ""
        ]
        # Create a test pipeline.
        with TestPipeline() as p:

            # Create an input PCollection.
            input = p | beam.Create(WORDS)

            # Apply the Count transform under test.
            output = input | beam.combiners.Count.PerElement()

            # Assert on the results.
            assert_that(
                output,
                equal_to([
                    ("hi", 4),
                    ("there", 1),
                    ("sue", 2),
                    ("bob", 2),
                    ("", 3),
                    ("ZOW", 1)]))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()
