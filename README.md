# hello-minio-docker
Hello world to MinIO Object Store using Docker

### !!! README.md file
_**First draft:** Work in progress, detailed documentation to follow. Thank you for your understanding and patience._

### 1. Create MinIO container

`cd` into your project directory and clone the repository. Ensure that all the files are present in your project directory.
```shell
kumarrohit@Kumars-Mac-mini MinIO % git clone https://github.com/krohit-bkk/hello-minio-docker.git
kumarrohit@Kumars-Mac-mini MinIO % pwd && tree .
```

Folder structure should look like this:
```text
/Users/kumarrohit/Learning/Docker_Projects/MinIO
.
├── Dockerfile.etl
├── README.md
├── docker-compose.yml
├── .gitignore
├── minio_data
│   ├── .gitkeep
├── pyproject.toml
├── sample_data.csv
├── try_minio_with_pyspark.py
└── try_minio_with_python.py
```

Start the containers for MinIO and Spark
```shell
docker compose up -d minio spark-master spark-worker
```

Verify that all three required containers are up and running:
```text
kumarrohit@Kumars-Mac-mini MinIO % docker ps
CONTAINER ID   IMAGE                        COMMAND                  CREATED          STATUS          PORTS                                            NAMES
a03c6d4d9935   bitnami/spark:3.5.0          "/opt/bitnami/script…"   28 minutes ago   Up 28 minutes                                                    spark-worker
027df1dc7275   bitnami/spark:3.5.0          "/opt/bitnami/script…"   28 minutes ago   Up 28 minutes   0.0.0.0:7077->7077/tcp, 0.0.0.0:9080->9080/tcp   spark-master
465d0d5ef465   quay.io/minio/minio:latest   "/usr/bin/docker-ent…"   5 hours ago      Up 5 hours      0.0.0.0:9000->9000/tcp, 0.0.0.0:9090->9090/tcp   minio-server
```


### 2. Quick MinIO setup and the basic know how
1. http://localhost:9090

![image](https://github.com/krohit-bkk/hello-minio-docker/assets/137164694/218df151-0a29-4822-a1b9-70bf18044c0d)

2. Using the Web-UI, naviage to `Buckets` on left hand side pane to create a bucket named `test-bucket-1`. 

![image](https://github.com/krohit-bkk/hello-minio-docker/assets/137164694/f0728d4f-3910-4c51-8013-25052fe35c4b)

![image](https://github.com/krohit-bkk/hello-minio-docker/assets/137164694/4c29e30b-c8da-4c04-be14-5cadcc7c0555)

3. Once bucket is created, navigate to `Object Browser` select the bucket and click on `create new path` and create a new folder and name it `sample_data`

![image](https://github.com/krohit-bkk/hello-minio-docker/assets/137164694/c283cd7c-f1c0-4d39-8e9b-493282ad564f)

![image](https://github.com/krohit-bkk/hello-minio-docker/assets/137164694/101b2cd9-a5d2-43e0-85fa-2fe713e79c38)

4. Browse and add the file `sample_data.csv` in folder `sample_data`.

![image](https://github.com/krohit-bkk/hello-minio-docker/assets/137164694/4f2f2105-8a35-4281-9067-d42506b060ac)

**Note:** the final object path would look like this: `test-bucket-1/sample_data/sample_data.csv`


### 3. Running the apps
The `etl` container has `sample_data.csv` located in `/opt/` which is our data file for demo. 

#### 3.1. Simple python (boto3) app
The `etl` container has `try_minio_with_python.py`, which is the main app, located in `/opt/`.

This app does these things in the given sequence:
1. Create MinIO (S3) bucket
2. Upload to MinIO (S3) from local storage (of container `etl`)
3. Check if an object exists (on `test-bucket-1`)
4. Copy object from one bucket `test-bucket-1` to another `test-bucket-2`
5. Download object from MinIO (S3) to local storage (of container `etl` at `/opt/sample_data/sample_data1.csv`)
6. Delete object from MinIO (S3) bucket (`test-bucket-1/sample_data/sample_data.csv`)

```shell
docker compose run -it etl python /opt/try_minio_with_python.py
```

Console output:
```text
kumarrohit@Kumars-Mac-mini MinIO % docker compose run -it etl python /opt/try_minio_with_python.py
[+] Creating 3/0
 ✔ Container minio-server  Running                                                                0.0s
 ✔ Container spark-master  Running                                                                0.0s
 ✔ Container spark-worker  Running                                                                0.0s

>>>> Bucket test-bucket-1 already exists

>>>> File uploaded successfully to test-bucket-1/sample_data/sample_data.csv

>>>> Object sample_data/sample_data.csv exists in test-bucket-1

>>>> Bucket test-bucket-2 already exists

>>>> Object test-bucket-1/sample_data/sample_data.csv copied to test-bucket-2/sample_data/sample_data.csv

>>>> File downloaded successfully to local [/opt/sample_data/sample_data1.csv]

>>>> Object sample_data/sample_data.csv deleted from test-bucket-1
```

#### 3.2. Running pyspark app
The `etl` container has `try_minio_with_pyspark.py`, which is the main app, located in `/opt/`.

The app does these things in the given sequence:
1. Read data from MinIO (S3) as spark dataframe located at `test-bucket-1/sample_data/sample_data.csv`
2. Write another sample data to another location in MinIO (S3) bucket in parquet format at `test-bucket-1/sample_data1/`
3. Read the parquet file (again) as spark dataframe to verify the writes

Everytime, we print data from spark dataframe we are adding a column `Flag` to indicate the dataframe from which the data getting printed.

```shell
docker compose run -it etl spark-submit --jars aws-java-sdk-bundle-1.12.540.jar,hadoop-aws-3.3.4.jar /opt/try_minio_with_pyspark.py
```

Console output:
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

### 4. Any trouble?

**__P.S.__:** If you run **simple python (boto3) app** before **pyspark app**, ensure that the data file `sample_file/sample_file.csv` is present in the bucket `test-bucket-1`.
The data file `test-bucket-1/sample_file/sample_file.csv` gets deleted as part of **simple python app**, hence, you would get a `FileNotFoundException` or `PATH_NOT_FOUND`. Error message would look something like this:

```text
pyspark.errors.exceptions.captured.AnalysisException: [PATH_NOT_FOUND] Path does not exist: s3a://test-bucket-1/sample_data.
23/11/27 22:19:52 ERROR TransportRequestHandler: Error sending result StreamResponse[streamId=/jars/aws-java-sdk-bundle-1.12.540.jar,byteCount=339975924,body=FileSegmentManagedBuffer[file=/opt/aws-java-sdk-bundle-1.12.540.jar,offset=0,length=339975924]] to /192.168.0.4:50422; closing connection
io.netty.channel.StacklessClosedChannelException
    at io.netty.channel.AbstractChannel.close(ChannelPromise)(Unknown Source)
```
To mitigate this issue, please follow the MinIO Web-UI guide (explained above) to upload the `sample_data.csv` file again, and then proceed with the pyspark app.