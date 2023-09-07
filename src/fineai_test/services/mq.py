import pika
import logging
import platform
from retrying import retry
from fineai_test.config import settings
import fineai_task_schema as schema

log = logging.getLogger(__name__)

def connect(tasks:list[str], ret:list[str]):
    parameters = pika.URLParameters(settings.rabbitmq_uri)
    parameters.client_properties = {
        "connection_name": platform.node(),
    }
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    queue = channel.queue_declare(queue=settings.rabbitmq_task_queue, durable=True, arguments={
        'x-message-ttl': 60*60*24*1000,
        'x-max-priority': 10,
    })
    # 检查队列中是否还有消息
    log.debug(f'{queue.method.message_count=}')
    if queue.method.message_count == 0:
        # 如果队列中没有消息，断开连接
        connection.close()

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
        log.debug(f'{request.task_no=}, {str(request.task_no) in tasks}')
        if str(request.task_no) in tasks:
            response_data = '{"deprecated": true}'
            channel.basic_publish("", properties.reply_to, response_data)
            channel.basic_ack(delivery_tag=method.delivery_tag)
            ret.append(str(request.task_no))
        count += 1
        if count == queue.method.message_count:
            connection.close()
        # queue = channel.queue_declare(queue=settings.rabbitmq_task_queue, durable=True, arguments={
        #     'x-message-ttl': 60*60*24*1000,
        #     'x-max-priority': 10,
        # })
        # log.debug(f'{queue.method.message_count=}')
        # # 检查队列中是否还有消息
        # if queue.method.message_count == 0:
        #     # 如果队列中没有消息，断开连接
        #     connection.close()

    channel.basic_consume(queue=settings.rabbitmq_task_queue,
        on_message_callback=callback,
        auto_ack=False,
        consumer_tag=f"{platform.node()}-test-csg",)

    return channel


# @retry(stop_max_attempt_number=2)
def consume(tasks:list[str]):
    log.debug(f'consume: {tasks=}')
    ret = []
    
    log.debug('Waiting for messages. To exit press CTRL+C')
    try:
        channel = connect(tasks, ret)
        channel.start_consuming()
    except pika.exceptions.ChannelWrongStateError:
        log.debug("no messages in the queue. Exiting...")
    except pika.exceptions.ConnectionClosedByBroker:
        log.debug("No more messages in the queue. Exiting...")
    log.debug(f'consume: {ret=}')
    return ret
