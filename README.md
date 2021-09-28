# video-analyzer
This service analyzes videos captured from Ring doorbell / Spotlight camera to detect objects, people, animals and gives a confidence score for its accuracy. The analysis makes use of [Amazon's Rekognition](https://aws.amazon.com/rekognition/) service which performs [label detection](https://docs.aws.amazon.com/rekognition/latest/dg/labels.html) on the video.

Some of the data that can be retreived based on this analysis are - (subject to the confidence score of the analysis and the position of your Ring camera)
* No. of times a person / bird / car is detected on your driveway in a day / month / year
* No. of days it has rained in a month / year (based on "Water" label detected in videos)

The Ring videos are downloaded by the [ring-downloader](https://github.com/sharathgopinath/ring-downloader) and stored into an S3 bucket, from where this video analyzer picks it up for its analysis.

<img src=".img/architecture.png" width="700">

## Data access patterns

The analysis data is stored in a dynamodb table which is designed for the following access patterns - 
* Retrieve all label names for a given year / month / day
* Retrieve properties of specific labels for a given year / month / day 

## Sample analysis data
### Label names
```
{
  "PK": {
    "S": "label:2021"
  },
  "SK": {
    "S": "8:30"
  },
  "label_names": {
    "SS": [
      "Apparel",
      "Architecture",
      "Automobile",
      "Backyard",
      "Balcony"
    ]
  }
}
```

### Label properties
```
{
 "PK": "label:Person:2021",
 "SK": "8:28:front_cam",
 "analysis_response": [
  {
   "name": "Person",
   "instances": [
    {
     "Confidence": 98.52984619140625,
     "BoundingBox": {
      "Height": 0.3622591495513916,
      "Left": 0.36070266366004944,
      "Top": 0.46451959013938904,
      "Width": 0.10082066804170609
     }
    }
   ],
   "confidence": 98.85364532470703,
   "parents": [],
   "timestamp": 3000
  }
}
```

## Run tests
```
docker-compose up -d
python3 -m pytest
```

## References
* https://docs.aws.amazon.com/rekognition/latest/dg/how-it-works.html
* https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python-example_code-rekognition.html
* https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
* https://www.alexdebrie.com/posts/dynamodb-single-table/
