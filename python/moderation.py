import json
import base64
from os import environ
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    """
    Lambda handler function
    Uses Amazon Rekognition Moderation Labels to accept or reject an image.
    """

    try:
        # Determine image source
        if 'image' in event:
            image_bytes = event['image'].encode('utf-8')
            img_b64decoded = base64.b64decode(image_bytes)
            image = {'Bytes': img_b64decoded}
        else:
            raise ValueError(
                'Invalid source. Only image base64 encoded bytes are supported.')

        # Detect Moderation Labels
        moderation_response = rekognition.detect_moderation_labels(
            Image=image,
            MinConfidence=75   # you can adjust if you want to be more strict
        )

        labels = moderation_response.get("ModerationLabels", [])

        # Criteria for rejection
        REJECT_CATEGORIES = [
            "Explicit Nudity",
            "Explicit Sexual Activity",
            "Non-Explicit Nudity",
            "Obstructed Intimate Parts",
            "Sex Toys",
            "Nudity",
            "Violence",
            "Hate Symbols",
            "Alcohol Use",
            "Middle Finger",
            "Drugs",
            "Alcohol",
            "Tobacco",
            "Graphic Violence",
        ]

        rejected = False
        matched_labels = []

        for lbl in labels:
            if lbl["ParentName"] in REJECT_CATEGORIES or lbl["Name"] in REJECT_CATEGORIES:
                rejected = True
                matched_labels.append({
                    "Name": lbl["Name"],
                    "Parent": lbl["ParentName"],
                    "Confidence": lbl["Confidence"]
                })

        # Prepare response
        if rejected:
            result = {
                "decision": "REJECTED",
                "reason": "Image contains inappropriate/unallowed content",
                "labels": matched_labels
            }
        else:
            result = {
                "decision": "ACCEPTED",
                "labels_detected": labels
            }

        lambda_response = {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    # Handle exceptions
    except ClientError as err:
        error_message = (
            f"Couldn't analyze image. {err.response['Error']['Message']}"
        )
        lambda_response = {
            'statusCode': 400,
            'body': {
                "Error": err.response['Error']['Code'],
                "ErrorMessage": error_message
            }
        }
        logger.error("Error function %s: %s",
                     context.invoked_function_arn, error_message)

    except ValueError as val_error:
        lambda_response = {
            'statusCode': 400,
            'body': {
                "Error": "ValueError",
                "ErrorMessage": str(val_error)
            }
        }
        logger.error("Error function %s: %s",
                     context.invoked_function_arn, str(val_error))

    return lambda_response