# hello-minio-docker
Hello world to MinIO Object Store using Docker

### !!! README.md file
_**First draft:** Work in progress, detailed documentation to follow. Thank you for your understanding and patience._

### 1. Create MinIO container
```shell
docker compose up -d minio spark-master spark-worker
```

Verify the required containers are up and running:
```text
kumarrohit@Kumars-Mac-mini MinIO % docker ps
CONTAINER ID   IMAGE                        COMMAND                  CREATED          STATUS          PORTS                                            NAMES
a03c6d4d9935   bitnami/spark:3.5.0          "/opt/bitnami/script…"   28 minutes ago   Up 28 minutes                                                    spark-worker
027df1dc7275   bitnami/spark:3.5.0          "/opt/bitnami/script…"   28 minutes ago   Up 28 minutes   0.0.0.0:7077->7077/tcp, 0.0.0.0:9080->9080/tcp   spark-master
465d0d5ef465   quay.io/minio/minio:latest   "/usr/bin/docker-ent…"   5 hours ago      Up 5 hours      0.0.0.0:9000->9000/tcp, 0.0.0.0:9090->9090/tcp   minio-server
```


### 2. Login to MinIO
`http://localhost:9090`

Using the Web-UI, naviage to `Buckets` on left hand side pane to create a bucket named `test-bucket-1` and add file `sample_data.csv` in folder `sample_data`.

**Note:** the final object path would look like this: `test-bucket-1/sample_data/sample_data.csv`


### 3.1. Running simple python (boto3) app
```python
docker compose run -it etl python /opt/try_minio_with_python.py
```


### 3.2. Running pyspark app
```python
docker compose run -it etl spark-submit --jars aws-java-sdk-bundle-1.12.540.jar,hadoop-aws-3.3.4.jar /opt/try_minio_with_pyspark.py
```

**P.S.:** If you run simple python app before pyspark app, ensure that the data file `sample_file/sample_file.csv` is present in the bucket `test-bucket-1`.
The data file `test-bucket-1/sample_file/sample_file.csv` gets deleted as part of demo, hence, file not found. Error message would look something like this:

```text
pyspark.errors.exceptions.captured.AnalysisException: [PATH_NOT_FOUND] Path does not exist: s3a://test-bucket-1/sample_data.
23/11/27 22:19:52 ERROR TransportRequestHandler: Error sending result StreamResponse[streamId=/jars/aws-java-sdk-bundle-1.12.540.jar,byteCount=339975924,body=FileSegmentManagedBuffer[file=/opt/aws-java-sdk-bundle-1.12.540.jar,offset=0,length=339975924]] to /192.168.0.4:50422; closing connection
io.netty.channel.StacklessClosedChannelException
    at io.netty.channel.AbstractChannel.close(ChannelPromise)(Unknown Source)
```

### 4. Successful run
#### Simple python (boto3) app
```text
kumarrohit@Kumars-Mac-mini MinIO % docker compose run -it etl python /opt/try_minio_with_python.py
[+] Creating 3/0
 ✔ Container minio-server  Running                                                                0.0s
 ✔ Container spark-master  Running                                                                0.0s
 ✔ Container spark-worker  Running                                                                0.0s

>>>> Bucket test-bucket-1 already exists

>>>> The file was not found

>>>> Object sample_data/sample_data.csv exists in test-bucket-1

>>>> Bucket test-bucket-2 already exists

>>>> Object test-bucket-1/sample_data/sample_data.csv copied to test-bucket-2/sample_data/sample_data.csv

>>>> File downloaded successfully to local [/opt/sample_data/sample_data1.csv]

>>>> Object sample_data/sample_data.csv deleted from test-bucket-1
```

#### Pyspark app
```text
kumarrohit@Kumars-Mac-mini MinIO % docker compose run -it etl spark-submit --jars aws-java-sdk-bundle-1.12.540.jar,hadoop-aws-3.3.4.jar /opt/try_minio_with_pyspark.py
[+] Creating 3/0
 ✔ Container spark-master  Running                                                               0.0s
 ✔ Container minio-server  Running                                                               0.0s
 ✔ Container spark-worker  Running                                                               0.0s
23/11/27 22:20:41 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
23/11/27 22:20:41 INFO SparkContext: Running Spark version 3.5.0
23/11/27 22:20:41 INFO SparkContext: OS info Linux, 6.3.13-linuxkit, aarch64
23/11/27 22:20:41 INFO SparkContext: Java version 1.8.0_342
23/11/27 22:20:41 INFO ResourceUtils: ==============================================================
23/11/27 22:20:41 INFO ResourceUtils: No custom resources configured for spark.driver.
23/11/27 22:20:41 INFO ResourceUtils: ==============================================================
23/11/27 22:20:41 INFO SparkContext: Submitted application: MinIO PySpark Example
...
...
23/11/27 22:20:42 INFO Utils: Successfully started service 'SparkUI' on port 4040.
23/11/27 22:20:42 INFO SparkContext: Added JAR file:///opt/aws-java-sdk-bundle-1.12.540.jar at spark://1c7062927bda:40149/jars/aws-java-sdk-bundle-1.12.540.jar with timestamp 1701123641753
23/11/27 22:20:42 INFO SparkContext: Added JAR file:///opt/hadoop-aws-3.3.4.jar at spark://1c7062927bda:40149/jars/hadoop-aws-3.3.4.jar with timestamp 1701123641753
23/11/27 22:20:42 INFO StandaloneAppClient$ClientEndpoint: Connecting to master spark://spark-master:7077...
...
...
23/11/27 22:20:42 INFO StandaloneAppClient$ClientEndpoint: Executor updated: app-20231127222042-0003/0 is now RUNNING
23/11/27 22:20:42 INFO StandaloneSchedulerBackend: SchedulerBackend is ready for scheduling beginning after reached minRegisteredResourcesRatio: 0.0

>>>> DEBUG ENV...
>>>> Access key: AWS_ACCESS_KEY_ID not found
>>>> Secret key: AWS_SECRET_ACCESS_KEY not found
>>>> Entrypoint: ENDPOINT not found
23/11/27 22:20:43 WARN MetricsConfig: Cannot locate configuration: tried hadoop-metrics2-s3a-file-system.properties,hadoop-metrics2.properties
+---+----+------+----+
| id|name|salary|Flag|
+---+----+------+----+
|  1|   A|   100| df1|
|  2|   B|   200| df1|
|  3|   C|   300| df1|
+---+----+------+----+

+---+-------+---+----+
| id|   name|age|Flag|
+---+-------+---+----+
|  1|  Alice| 25| df2|
|  2|    Bob| 30| df2|
|  3|Charlie| 22| df2|
+---+-------+---+----+

+---+-------+---+----+
| id|   name|age|Flag|
+---+-------+---+----+
|  2|    Bob| 30| df3|
|  3|Charlie| 22| df3|
|  1|  Alice| 25| df3|
+---+-------+---+----+
```
