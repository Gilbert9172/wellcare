from pyfcm import FCMNotification
import app

def push(token, title, body, type, data, device='A'):
    API_KEY = app.app.config['FCM_API_KEY']
    push_service = FCMNotification(api_key=API_KEY)

    result = None
    if device == 'A':
        data_message = {
            "title": title,
            "body": body,
            "type": type,
            "data": data
        }

        result = push_service.single_device_data_message(
            registration_id=token,
            data_message=data_message
        )
    else:
        result = push_service.notify_single_device(
            registration_id=token,
            message_title=title,
            message_body=body,
            data_message=data
        )


    # result = push_service.notify_single_device(
    #     registration_id=token,
    #     message_title=title,
    #     message_body=body,
    #     data_message=data_message
    # )
    return result

def pushs(atokens, itokens, title, body, type, data):
    API_KEY = app.app.config['FCM_API_KEY']
    push_service = FCMNotification(api_key=API_KEY)

    data_message = {
        "title": title,
        "body": body,
        "type": type,
        "data": data
    }

    result = push_service.multiple_devices_data_message(
        registration_ids=atokens,
        data_message=data_message
    )

    result = push_service.notify_multiple_devices(
        registration_ids=itokens,
        message_title=title,
        message_body=body,
        data_message=data
    )
    return result