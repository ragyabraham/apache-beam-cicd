import argparse
import logging

import apache_beam as beam
from apache_beam.dataframe.convert import to_dataframe
from apache_beam.dataframe.convert import to_pcollection
from apache_beam.io import ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions


def run(argv=None):
    """Main entry point; defines and runs the wordcount pipeline."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--input',
        dest='input',
        default='gs://dataflow-samples/shakespeare/kinglear.txt',
        help='Input file to process.')
    parser.add_argument(
        '--output',
        dest='output',
        required=True,
        help='Output file to write results to.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    # Import this here to avoid pickling the main session.
    import re

    # The pipeline will be run on exiting the with block.
    with beam.Pipeline(options=PipelineOptions(pipeline_args)) as p:

        # [START DataFrame_wordcount]

        # Read the text file[pattern] into a PCollection.
        lines = p | 'Read' >> ReadFromText(known_args.input)

        words = (
            lines
            | 'Split' >> beam.FlatMap(
                lambda line: re.findall(r'[\w]+', line)).with_output_types(str)
            # Map to Row objects to generate a schema suitable for conversion
            # to a dataframe.
            | 'ToRows' >> beam.Map(lambda word: beam.Row(word=word)))

        df = to_dataframe(words)
        df['count'] = 1
        counted = df.groupby('word').sum()
        counted.to_csv(known_args.output)

        # Deferred DataFrames can also be converted back to schema'd PCollections
        counted_pc = to_pcollection(counted, include_indexes=True)

        # [END DataFrame_wordcount]

        # Print out every word that occurred >50 times
        _ = (
            counted_pc
            | beam.Filter(lambda row: row.count > 50)
            | beam.Map(lambda row: f'{row.word}: {row.count}')
            | beam.Map(print))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
