# apache-beam-cicd
Apache beam cicd pipeline for beam summit 2022

Helpful links and videos:
<p>
 - Link to previous youtube video https://www.youtube.com/watch?v=9-jKLjcxJl4&list=PPSV
 </p>
 <p>
 - Link to testing example in Apache beam GitHub https://github.com/apache/beam/blob/master/sdks/python/apache_beam/testing/test_stream_test.py
</p>

This repositiry is an example of how to implement CICD for an Apache Beam pipeline. It covers the below points:
* Testing your pipeline
  * Using the Apache beam ```TestPipeline``` class
    * Unit testing of ```DoFns```
    * Unit testing of Composite Transforms
    * Batch Pipeline Testing
    * Streaming Pipeline Testing using ```TestStream``` class
    * Integration tests of Streming pipeline
* Deploying your pipeline
  * Setting up deployment triggers
    * Environment variables
  * Containerising your pipeline
  * Using Google Cloud Build YAML file
