import time
import json
import pika
import logging
import platform
from pika.adapters.blocking_connection import BlockingChannel
from fineai_test.config import settings
import fineai_task_schema as schema

log = logging.getLogger(__name__)


def connect(queue_name):
    parameters = pika.URLParameters(settings.rabbitmq_uri)
    parameters.client_properties = {
        "connection_name": platform.node(),
    }
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    method = channel.queue_declare(queue=queue_name, durable=True, arguments={
        'x-message-ttl': 60*60*24*1000*7,
        'x-max-priority': 10,
    })
    
    return connection, channel, method


def config(queue_name:str, connection:pika.BlockingConnection, channel:BlockingChannel, mthd:pika.frame.Method, tasks_to_ack: list[str], ret: list, response_type: str | None = None):
    # train
    channel.basic_qos(prefetch_count=mthd.method.message_count)
    # for topic in settings.rabbitmq_task_topics:
    #     channel.queue_bind(
    #         queue=settings.rabbitmq_task_queue,
    #         exchange=settings.rabbitmq_task_exchange,
    #         routing_key=topic,
    #     )
    count = 0

    def callback(ch:BlockingChannel, method, properties, body):
        nonlocal count
        request = schema.Request.model_validate_json(body)
        log.debug(f'{request.task_no=}, {str(request.task_no) in tasks_to_ack}')
        if str(request.task_no) in tasks_to_ack:
            if response_type == 'fail':
                response_data = schema.Response(**request.model_dump(), success=False, message='manually fail').model_dump_json(exclude_unset=True)
                log.debug(response_data)
            else:
                response_data = '{"what?": "abandoned"}'
            log.debug(f'{properties.reply_to=}')
            ch.basic_publish("", properties.reply_to, response_data)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ret.append(str(request.task_no))
        count += 1
        # queue.method.message_count is fixed got by queue_declare(), dont update if changed
        if count == mthd.method.message_count:
            connection.close()

    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback,
                          auto_ack=False,
                          consumer_tag=f"{platform.node()}-test-csg",)


def consume(jobs: list[str], type: str | None = None):
    log.debug(f'consume: {jobs=}')
    ret = []
    log.debug('Waiting for messages. To exit press CTRL+C')
    lora_train_jobs = [job['job_id'] for job in jobs if job['job_kind'] == 'lora_train']
    img2img_jobs = [job['job_id'] for job in jobs if job['job_kind'] == 'img2img']
    if lora_train_jobs:
        try:
            connection, channel, method = connect(settings.rabbitmq_task_queue)
            log.debug(f'{method.method.message_count=}')
            if method.method.message_count != 0:
                config(settings.rabbitmq_task_queue, connection, channel, method, lora_train_jobs, ret, response_type=type)
                channel.start_consuming()
            else:
                connection.close()
        except (pika.exceptions.ChannelWrongStateError, pika.exceptions.ConnectionClosedByBroker) as e:
            log.debug(f'{e}')
            log.debug("no messages in the lora train queue. Exiting...")
    if img2img_jobs:
        try:
            connection, channel, method = connect(settings.rabbitmq_sd_queue)
            log.debug(f'{method.method.message_count=}')
            if method.method.message_count != 0:
                config(settings.rabbitmq_sd_queue, connection, channel, method, img2img_jobs, ret, response_type=type)
                channel.start_consuming()
            else:
                connection.close()
        except (pika.exceptions.ChannelWrongStateError, pika.exceptions.ConnectionClosedByBroker) as e:
            log.debug(f'{e}')
            log.debug("no messages in the sd queue. Exiting...")
    log.debug(f'consumed: {ret=}')
    return ret

def fail(jobs: list[str], type: str | None = None):
    log.debug(f'consume: {jobs=}')
    log.debug('Waiting for messages. To exit press CTRL+C')
    lora_train_jobs = [job['job_id'] for job in jobs if job['job_kind'] == 'lora_train']
    img2img_jobs = [job['job_id'] for job in jobs if job['job_kind'] == 'img2img']
    
    if lora_train_jobs:
        
        connection, channel, _ = connect(settings.rabbitmq_task_queue) 
        for task_no in lora_train_jobs:
            if type == 'suspend':
                resp = schema.Response(
                task_no=task_no,
                kind=schema.Kind.progress,
                success=True,
                payload=schema.Progress(
                    progress=0.2,
                    eta_relative=100,
                ),
                message="forcefully suspend a job"
            )
            else:    
                resp = schema.Response(
                    task_no=task_no,
                    kind=schema.Kind.lora_train,
                    success=False,
                    message="forcefully fail a job"
                ) 
            channel.basic_publish("", settings.rabbitmq_reply_queue, resp.model_dump_json(exclude_unset=True))
        connection.close()
    
    if img2img_jobs:
        connection, channel, _ = connect(settings.rabbitmq_sd_queue)
        for task_no in img2img_jobs:
            if type == 'suspend':
                resp = schema.Response(
                    task_no=task_no,
                    kind=schema.Kind.progress,
                    success=True,
                    payload=schema.Progress(
                        progress=0.2,
                        eta_relative=100,
                    ),
                    message="forcefully suspend a job"
                )
            else:
                resp = schema.Response(
                    task_no=task_no,
                    kind=schema.Kind.img2img,
                    success=False,
                    message="forcefully fail job"
                ) 
            channel.basic_publish("", settings.rabbitmq_reply_queue, resp.model_dump_json(exclude_unset=True))
            
        connection.close()
