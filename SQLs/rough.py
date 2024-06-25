I wanted to get your advice on Snowpipe. I don't think we have a Kafka (streaming) use case in Speciality, but we can explore it if you advise.

On the other hand, we have completed 80% of the development and testing for the GCP Snowflake decommissioning and expect a parallel run of both pipelines (the pipeline with GCP SF and the pipeline without GCP SF) by early next week in PROD to facilitate regression testing.

We have taken the following measures to reduce costs while developing for the GCP Snowflake decommissioning:

Transient Tables: As we can always pull the latest data from BigQuery, we are not dependent on the fail-safe feature of Snowflake permanent (normal/default) tables. Therefore, we are opting for transient tables, which can save significant storage costs.
Travel Feature: Since we do not have a use case for the travel feature, we are switching off that feature for our transient tables, further reducing storage costs.
Processing Logic Optimization: Tested and found the removal of these processing logics has improved performance by 40%, saving us compute costs.
