package main

import (
	"context"
	// "encoding/json"
	"log"
	// "net/http"
	// "time"
	// "fmt"
	"go.temporal.io/sdk/client"
	// "go.temporal.io/sdk/temporal"
	"go.temporal.io/sdk/activity"
	"go.temporal.io/sdk/worker"
)

func main() {
	temporalClient, err := client.Dial(client.Options{
		HostPort:  client.DefaultHostPort,
		Namespace: "default",
	})
	if err != nil {
		log.Fatalln("Unable to create Temporal Client", err)
	}
	defer temporalClient.Close()
	w := worker.New(temporalClient, "wikipedia-pageviews-queue",
		worker.Options{
			DisableWorkflowWorker: true,
		},
	)

	opt := activity.RegisterOptions{
		Name: "filter_articles",
	}
	w.RegisterActivityWithOptions(
		filter_articles,
		opt,
	)
	//w.RegisterWorkflow(WikipediaPageviews)
	err = w.Run(worker.InterruptCh())
	if err != nil {
		log.Fatalln("Unable to start Worker", err)
	}
}

func filter_articles(ctx context.Context, articles []string) ([]string, error) {
	var output []string
	for _, article := range articles {
		articles = append(output, article+"@foo")
	}
	return articles, nil
}
