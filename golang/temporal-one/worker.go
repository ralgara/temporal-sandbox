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

func filter_articles(ctx context.Context, input []map[string]interface{}) ([]map[string]interface{}, error) {
	// metapages = [
	// 	""
	// ]
	fmt.Println(fmt.Sprintf("%v", input))
	for index, element := range input {
		fmt.Println(fmt.Sprintf("%v, %v", index, element))
		element["foo"] = "bar"
	}
	// if err != nil {
	// 	log.Fatalln("Could not unmarshal")
	// }
	// var output []string
	// for _, article := range articles {
	// 	articles = append(output, article+"@foo")
	// }
	return input, nil
}
