import pika
import logging
import platform
from fineai_test.config import settings
import fineai_task_schema as schema

log = logging.getLogger(__name__)


def connect():
    parameters = pika.URLParameters(settings.rabbitmq_uri)
    parameters.client_properties = {
        "connection_name": platform.node(),
    }
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    queue = channel.queue_declare(queue=settings.rabbitmq_task_queue, durable=True, arguments={
        'x-message-ttl': 60*60*24*1000*7,
        'x-max-priority': 10,
    })

    return connection, channel, queue


def config(connection, channel, queue, tasks_to_ack: list[str], ret: list):
    channel.basic_qos(prefetch_count=queue.method.message_count)
    for topic in settings.rabbitmq_task_topics:
        channel.queue_bind(
            queue=settings.rabbitmq_task_queue,
            exchange=settings.rabbitmq_task_exchange,
            routing_key=topic,
        )
    count = 0

    def callback(ch, method, properties, body):
        nonlocal count
        request = schema.Request.model_validate_json(body)
        log.debug(f'{request.task_no=}, {str(request.task_no) in tasks_to_ack}')
        if str(request.task_no) in tasks_to_ack:
            response_data = '{"what?": "abandoned"}'
            ch.basic_publish("", properties.reply_to, response_data)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ret.append(str(request.task_no))
        count += 1
        # queue.method.message_count is fixed got by queue_declare(), dont update if changed
        if count == queue.method.message_count:
            connection.close()

    channel.basic_consume(queue=settings.rabbitmq_task_queue,
                          on_message_callback=callback,
                          auto_ack=False,
                          consumer_tag=f"{platform.node()}-test-csg",)


def consume(tasks: list[str]):
    log.debug(f'consume: {tasks=}')
    ret = []
    log.debug('Waiting for messages. To exit press CTRL+C')
    try:
        connection, channel, queue = connect()
        log.debug(f'{queue.method.message_count=}')
        if queue.method.message_count == 0:
            # if no message in queue, close connection
            connection.close()
            return ret
        config(connection, channel, queue, tasks, ret)
        channel.start_consuming()
    except (pika.exceptions.ChannelWrongStateError, pika.exceptions.ConnectionClosedByBroker) as e:
        log.debug(f'{e}')
        log.debug("no messages in the queue. Exiting...")
    log.debug(f'consumed: {ret=}')
    return ret
