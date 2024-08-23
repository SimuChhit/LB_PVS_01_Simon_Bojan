package main

import (
    "log"
    "github.com/streadway/amqp"
)

func failOnError(err error, msg string) {
    if err != nil {
        log.Fatalf("%s: %s", msg, err)
    }
}

func main() {
    // Verbindung zu RabbitMQ herstellen
    conn, err := amqp.Dial("amqp://user:user@rabbitmq:5672/")
    failOnError(err, "Failed to connect to RabbitMQ")
    defer conn.Close()

    ch, err := conn.Channel()
    failOnError(err, "Failed to open a channel")
    defer ch.Close()

    // Die Warteschlange definieren
    q, err := ch.QueueDeclare(
        "stock_queue", // Name der Warteschlange
        false,         // haltbar
        false,         // automatisch löschen
        false,         // exklusiv
        false,         // keine Wartezeit
        nil,           // Argumente
    )
    failOnError(err, "Failed to declare a queue")

    body := "Stock Data Packet"
    err = ch.Publish(
        "",     // Exchange
        q.Name, // Routing Key
        false,  // Pflicht
        false,  // Sofort
        amqp.Publishing{
            ContentType: "text/plain",
            Body:        []byte(body),
        })
    failOnError(err, "Failed to publish a message")
    log.Printf(" [x] Sent %s", body)
}