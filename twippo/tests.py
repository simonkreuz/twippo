from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy

import json

class TrackUpdatedTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.url = reverse_lazy('track_updated')

    def test_track_updated_get_invalid(self):
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_track_updated_post_body_empty(self):
        response = self.c.post(self.url)
        self.assertEqual(response.status_code, 400)

    def test_track_updated_post(self):
        payload = SAMPLE_TRANSACTIOM
        response = self.c.post(self.url, payload, content_type="application/json",)
        self.assertEqual(response.status_code, 200)


SAMPLE_TRANSACTIOM = '{"object_state":"VALID","object_status":"SUCCESS","object_created":"2014-11-29T16:31:19.512Z","object_updated":"2014-11-29T16:31:19.512Z","object_id":"5695ae3a5eda41ba9abdbf347fd545f3","object_owner":"simon+epostage1@goshippo.com","was_test":true,"rate":"fabbb33d03c14b4eb7c4366f2df2a7b3","pickup_date":null,"notification_email_from":false,"notification_email_to":false,"notification_email_other":"","tracking_number":"9102969010383081813033","tracking_status":{  "object_created":"2014-11-29T16:31:19.511Z","status":"DELIVERED","status_details":"Your shipment has been delivered.","status_date":"2012-03-08T09:58:00Z","location":{  "city":"Beverly Hills","state":"CA","zip":"90210","country":"US"}},"tracking_history":[  {  "object_created":"2014-11-29T12:31:19.573Z","status":"UNKNOWN","status_details":null,"status_date":null,"location":null},{  "object_created":"2014-11-29T16:31:19.573Z","status":"UNKNOWN","status_details":"The electronic shipping data has been received.","status_date":"2012-03-06T00:00:00Z","location":null},{  "object_created":"2014-11-29T16:31:19.568Z","status":"TRANSIT","status_details":"Your shipment has been accepted.","status_date":"2012-03-06T15:28:00Z","location":{  "city":"Las Vegas","state":"NV","zip":"89121","country":"US"}},{  "object_created":"2014-11-29T16:31:19.544Z","status":"TRANSIT","status_details":"Your shipment has departed the USPS Sort Facility.","status_date":"2012-03-07T00:00:00Z","location":{  "city":"Bell Gardens","state":"CA","zip":"90201","country":"US"}},{  "object_created":"2014-11-29T16:31:19.539Z","status":"TRANSIT","status_details":"Your shipment has arrived at the Post Office.","status_date":"2012-03-08T04:47:00Z","location":{  "city":"Beverly Hills","state":"CA","zip":"90210","country":"US"}},{  "object_created":"2014-11-29T16:31:19.524Z","status":"DELIVERED","status_details":"Your shipment has been delivered.","status_date":"2012-03-08T09:58:00Z","location":{  "city":"Beverly Hills","state":"CA","zip":"90210","country":"US"}}],"tracking_url_provider":"","label_url":"https://s3.amazonashippo.com/hippolabel.pdf","messages":[],"customs_note":"","submission_note":"","metadata":""}'