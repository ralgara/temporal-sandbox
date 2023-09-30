package main

import (
	"context"
	"fmt"
	"log"

	"go.temporal.io/sdk/activity"
	"go.temporal.io/sdk/client"
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
	w := worker.New(temporalClient, "wikipedia-filter",
		worker.Options{
			DisableWorkflowWorker: true,
		},
	)

	w.RegisterActivityWithOptions(
		filter_articles,
		activity.RegisterOptions{
			Name: "filter_articles",
		},
	)

	err = w.Run(worker.InterruptCh())
	if err != nil {
		log.Fatalln("Unable to start Worker", err)
	}
}

type ArticleMetadata struct {
	Type  string
	Flags string
}

func filter_articles(ctx context.Context, input []map[string]interface{}) ([]map[string]interface{}, error) {
	article_metadata := map[string]string{
		"Main_Page":      "meta",
		"Special:Search": "meta",
	}
	var output []map[string]interface{}
	arank := 1 // adjusted rank: rank of an article ignoring meta pages
	for _, article := range input {
		_, is_meta := article_metadata[article["article"].(string)]
		if is_meta {
			fmt.Printf("Drop [%v]\n", article["article"])
			continue
		} else {
			article["arank"] = arank
			fmt.Printf("Add [%v]\n", article["article"])
			arank++
			output = append(output, article)
		}
	}
	return output, nil
}
