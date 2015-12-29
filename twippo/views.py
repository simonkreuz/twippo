from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import logging
import json
import collections

from twilio.rest import TwilioRestClient 

log = logging.getLogger(__name__)

@require_POST
@csrf_exempt
def track_updated(request):
    log.info("Received new track updated webhook.")
    try:
        log.info(request.body)
        decoded_body = json.loads(request.body)
    except:
        log.warning("Track updated webhook: couldn't decode JSON", extra={
            "webhook_body": request.body })  
        return HttpResponse("", status=400)
    recipient_number_query = request.GET.get("recipient_phone")
    sender_number    = get_sender_number()
    recipient_number = recipient_number_query or get_recipient_number()
    body             = get_body(decoded_body)
    log.info("Found sender '%s', recipient '%s', body '%s'." % \
        (sender_number, recipient_number, body))
    message = send_message(sender_number, recipient_number, body)
    log.info("Twilio response: %s" % message.__dict__)
    log.info("Sent message from '%s' to '%s' with body '%s'" % \
        (sender_number, recipient_number, body))
    return HttpResponse('Powered by Twippo.', status=200)

def get_sender_number():
    return settings.TWILIO_SENDER_NUMBER

def get_recipient_number():
    return "+14157419393"

def get_body(decoded_body):
    log.info(decoded_body)
    if decoded_body["tracking_number"]:
        tracking_number = decoded_body["tracking_number"]
    if decoded_body["tracking_status"] and decoded_body["tracking_status"]["status"]:
        tracking_status = decoded_body["tracking_status"]["status"].title()
    else:
        tracking_status = "Unknown"
    if decoded_body["tracking_history"]:
        #ordered_history = collections.OrderedDict(sorted(decoded_body["tracking_history"].items()))
        ordered_history = sorted(decoded_body["tracking_history"], key=lambda x: x["status_date"], reverse=True)
        last_update = ": %s" % ordered_history[0]["status_details"]
    else:
        last_update = ""
    return "Your shipment with tracking number %s has been updated to %s%s" \
        % (tracking_number, tracking_status, last_update)

def send_message(sender_number, recipient_number, body):
    log.info("%s %s" % (settings.TWILIO_SID, settings.TWILIO_TOKEN) )
    client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_TOKEN) 
    return client.sms.messages.create(
        to=recipient_number, 
        from_=sender_number, 
        body=body,  
    )