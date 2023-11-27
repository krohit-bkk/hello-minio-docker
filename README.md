# hello-minio-docker
Hello world to MinIO Object Store using Docker

#### Create MinIO container
```docker compose up -d minio spark-master spark-worker```

#### Login to MinIO
http://localhost:9090
Create a bucket named `test-bucket-1` and add `sample_data.csv` file in folder `sample_data`

#### Running native python app
```docker rm $(docker ps -a -q --filter "name=minio-etl-run") && docker compose run -it etl python /opt/try_minio_with_python.py```

#### Running pyspark app
```docker compose run -it etl spark-submit --jars aws-java-sdk-bundle-1.12.540.jar,hadoop-aws-3.3.4.jar /opt/try_minio_with_pyspark.py```
Please note that if you run native python app before running pyspark app, ensure that the data file `sample_file/sample_file.csv` is present in the bucket `test-bucket-1`.
The data file `sample_file/sample_file.csv` gets deleted as part of demo, hence if running pyspark app after native python app, you would see error stating file not found.

```
    pyspark.errors.exceptions.captured.AnalysisException: [PATH_NOT_FOUND] Path does not exist: s3a://test-bucket-1/sample_data.
    23/11/27 22:19:52 ERROR TransportRequestHandler: Error sending result StreamResponse[streamId=/jars/aws-java-sdk-bundle-1.12.540.jar,byteCount=339975924,body=FileSegmentManagedBuffer[file=/opt/aws-java-sdk-bundle-1.12.540.jar,offset=0,length=339975924]] to /192.168.0.4:50422; closing connection
    io.netty.channel.StacklessClosedChannelException
        at io.netty.channel.AbstractChannel.close(ChannelPromise)(Unknown Source)
```

