import { Kafka, Producer, RecordMetadata } from 'kafkajs';

export interface ProducerOptions {
    broker: string;
    clientId: string;
}

export class KafkaProducer {
    private kafka: Kafka;
    private producer: Producer;

    constructor(options: ProducerOptions) {
        this.kafka = new Kafka({
            clientId: options.clientId,
            brokers: [options.broker]
        });

        this.producer = this.kafka.producer();
    }

    public async connect(): Promise<void> {
        try {
            await this.producer.connect();
            console.log(`[KafkaProducer] Connected to Kafka broker`);
        } catch (error) {
            console.error('[KafkaProducer] Error connecting to Kafka', error);
            throw error;
        }
    }

    public async disconnect(): Promise<void> {
        try {
            await this.producer.disconnect();
            console.log(`[KafkaProducer] Disconnected from Kafka broker`);
        } catch (error) {
            console.error('[KafkaProducer] Error disconnecting from Kafka', error);
            throw error;
        }
    }

    public async sendMessage(topic: string, message: any): Promise<RecordMetadata[]> {
        try {
            const result = await this.producer.send({
                topic,
                messages: [
                    { value: typeof message === 'string' ? message : JSON.stringify(message) }
                ],
            });
            console.log(`[KafkaProducer] Message sent to topic ${topic}`);
            return result;
        } catch (error) {
            console.error(`[KafkaProducer] Error sending message to topic ${topic}`, error);
            throw error;
        }
    }
}