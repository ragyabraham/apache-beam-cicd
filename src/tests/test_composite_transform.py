import apache_beam as beam
import unittest
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
import re
import logging


@beam.ptransform_fn
def CountWords(pcoll):
    return (
        pcoll
        | 'ExtractWords' >> beam.FlatMap(lambda x: re.findall(r'[A-Za-z\']+', x))
        | beam.combiners.Count.PerElement()
    )


class WordCountTest(unittest.TestCase):

    def test_count_words(self):
        # Our input data, which will make up the initial PCollection.
        WORDS = [
            "hi", "there", "hi", "hi", "sue", "bob",
            "hi", "sue", "", "", "ZOW", "bob", ""
        ]
        # Our output data, which is the expected data that the final PCollection must match.
        EXPECTED_COUNTS = [
            ('hi', 4), ('there', 1),
            ('sue', 2), ('bob', 2), ('ZOW', 1)]
        with TestPipeline() as p:
            input = p | beam.Create(WORDS)
            output = input | CountWords()
            assert_that(output, equal_to(EXPECTED_COUNTS), label='CheckOutput')

    # The pipeline will run and verify the results.


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()
