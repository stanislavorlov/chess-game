package kafka

import (
	"context"
	"log"

	ckafka "github.com/confluentinc/confluent-kafka-go/v2/kafka"
)

type Consumer struct {
	client *ckafka.Consumer
}

// StartConsumer creates and starts a continuous Kafka polling loop in a goroutine
func StartConsumer(ctx context.Context, bootstrapServers, groupID, topic string, handler func([]byte)) (*Consumer, error) {
	config := &ckafka.ConfigMap{
		"bootstrap.servers": bootstrapServers,
		"group.id":          groupID,
		"auto.offset.reset": "earliest",
	}

	consumer, err := ckafka.NewConsumer(config)
	if err != nil {
		return nil, err
	}

	err = consumer.SubscribeTopics([]string{topic}, nil)
	if err != nil {
		return nil, err
	}

	c := &Consumer{client: consumer}
	log.Printf("Started Kafka consumer on topic %s", topic)

	go c.pollLoop(ctx, handler)

	return c, nil
}

func (c *Consumer) pollLoop(ctx context.Context, handler func([]byte)) {
	for {
		select {
		case <-ctx.Done():
			log.Println("Stopping Kafka consumer loop...")
			c.Close()
			return
		default:
			// Poll block for 100ms
			msg, err := c.client.ReadMessage(100)
			if err != nil {
				// Errors are expected when polling times out
				if err.(ckafka.Error).Code() != ckafka.ErrTimedOut {
					log.Printf("Kafka consumer error: %v", err)
				}
				continue
			}

			// Pass the message value to the handler
			handler(msg.Value)
		}
	}
}

func (c *Consumer) Close() {
	if c.client != nil {
		err := c.client.Close()
		if err != nil {
			log.Printf("Error closing Kafka consumer: %v", err)
		} else {
			log.Println("Kafka consumer closed successfully.")
		}
	}
}
