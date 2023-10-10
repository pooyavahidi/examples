package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
)

// ListBuckets lists up to 'count' buckets using the provided s3Client
func ListBuckets(client *s3.Client, count int) {
	result, err := client.ListBuckets(context.TODO(), &s3.ListBucketsInput{})
	if err != nil {
		fmt.Printf("Couldn't list buckets for your account. Here's why: %v\n", err)
		return
	}

	if len(result.Buckets) == 0 {
		fmt.Println("You don't have any buckets!")
	} else {
		if count > len(result.Buckets) {
			count = len(result.Buckets)
		}
		for _, bucket := range result.Buckets[:count] {
			fmt.Printf("\t%v\n", *bucket.Name)
		}
	}
}

func DownloadObject(s3Client *s3.Client, bucketName string, objectKey string, fileName string) error {
	result, err := s3Client.GetObject(context.TODO(), &s3.GetObjectInput{
		Bucket: aws.String(bucketName),
		Key:    aws.String(objectKey),
	})
	if err != nil {
		log.Printf("Couldn't get object %v:%v. Here's why: %v\n", bucketName, objectKey, err)
		return err
	}
	defer result.Body.Close()
	file, err := os.Create(fileName)
	if err != nil {
		log.Printf("Couldn't create file %v. Here's why: %v\n", fileName, err)
		return err
	}
	defer file.Close()
	body, err := io.ReadAll(result.Body)
	if err != nil {
		log.Printf("Couldn't read object body from %v. Here's why: %v\n", objectKey, err)
	}
	_, err = file.Write(body)
	return err
}

func main() {
	sdkConfig, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		fmt.Println("Couldn't load default configuration. Have you set up your AWS account?")
		fmt.Println(err)
		return
	}

	s3Client := s3.NewFromConfig(sdkConfig)

	// List buckets
	ListBuckets(s3Client, 10)

	// Get object
	bucketName := "jumpstart-cache-prod-us-east-1"
	objectKey := "community_models/huggingface-text2text-flan-t5-small/specs_v1.3.2.json"
	fileName := "specs_v1.3.2.json.downloaded"

	err = DownloadObject(s3Client, bucketName, objectKey, fileName)
	if err != nil {
		log.Printf("Error while downloading object: %v", err)
	} else {
		fmt.Printf("Successfully downloaded %v:%v to %v\n", bucketName, objectKey, fileName)
	}
}
