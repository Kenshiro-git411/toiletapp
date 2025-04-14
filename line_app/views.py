from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

# LINE Bot configuration
print("LINE_CHANNEL_ACCESS_TOKEN: ",settings.LINE_CHANNEL_ACCESS_TOKEN)
print("LINE_CHANNEL_SECRET: ",settings.LINE_CHANNEL_SECRET)
configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        print("request: ", request)
        print("request.headers: ", request.headers)

        # get X-Line-Signature header value
        signature = request.headers.get('X-Line-Signature', '')

        # get request body as text
        body = request.body.decode('utf-8')

        print("===== LINE Webhook Request =====")
        print("Signature:", signature)
        print("Body:", body)

        try:
            request_json = json.loads(body)
            print("request_json", request_json)
        except json.JSONDecodeError:
            print("JSONデコードエラー")
            return HttpResponseBadRequest()

        if not request_json["events"]:
            # print("request_json", request_json)
            print("空のイベントを無視")
            return HttpResponse('OK')

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("こっちにきている")
            return HttpResponseBadRequest()

        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest()


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # print("handle_message処理内: ", handle_message)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        print("line_bot_api: ", line_bot_api)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="こんにちは")]
            )
        )

        # https://liff.line.me/2006987823-rbyRdp3p