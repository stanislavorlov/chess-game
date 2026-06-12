package kafka

import (
	"log"

	ckafka "github.com/confluentinc/confluent-kafka-go/v2/kafka"
)

type Producer struct {
	client *ckafka.Producer
}

func NewProducer(bootstrapServers string) (*Producer, error) {
	p, err := ckafka.NewProducer(&ckafka.ConfigMap{"bootstrap.servers": bootstrapServers})
	if err != nil {
		return nil, err
	}

	go func() {
		for e := range p.Events() {
			switch ev := e.(type) {
			case *ckafka.Message:
				if ev.TopicPartition.Error != nil {
					log.Printf("Delivery failed: %v\n", ev.TopicPartition)
				} else {
					log.Printf("Delivered message to %v\n", ev.TopicPartition)
				}
			}
		}
	}()

	return &Producer{client: p}, nil
}

func (p *Producer) Produce(topic string, key, value []byte) error {
	return p.client.Produce(&ckafka.Message{
		TopicPartition: ckafka.TopicPartition{Topic: &topic, Partition: ckafka.PartitionAny},
		Key:            key,
		Value:          value,
	}, nil)
}

func (p *Producer) Close() {
	p.client.Flush(15 * 1000)
	p.client.Close()
}
