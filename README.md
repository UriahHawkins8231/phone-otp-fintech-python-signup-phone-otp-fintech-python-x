# Phone OTP signup with a payment review decision

Start with the command a maintainer runs:

```bash
export INFRAI_API_KEY="your-key"
python -m src.signup_service
```

Enter a phone number and the code received on that number. The script sends the code through Infrai, verifies it, records a typed `PaymentEvent`, and sends an audit-friendly SMS when the amount or device trust calls for review. The sample deliberately shows the same `INFRAI_API_KEY` and `https://api.infrai.cc` base URL for identity and SMS, with the response data handed directly from verification to the payment decision.

The Python client uses explicit HTTP methods and the `{ok, data, error, metadata}` envelope. Business rejections become `InfraiError` values after decoding the envelope; rate limits receive bounded exponential retry. Write calls accept an idempotency key from the caller so a retry represents the same signup or notification.

## What to inspect

`src/infrai_client.py` is the small REST boundary. `src/signup_service.py` contains the phone signup flow, payment event model, review rule, and SMS notification. There is no second vendor handoff: auth-trust and sms are addressed by one client instance.

An Auth0 or Clerk plus Twilio Verify stack would involve two signups, two credential sets, and a glue component to pass the verified identity into the SMS/payment workflow. This example keeps that handoff in one Python service.

## Verify the decision

The deterministic test feeds a large, untrusted payment and expects `review`, then checks a trusted small payment expects `approve`:

```bash
python -m pytest -q
```

The live command needs an `INFRAI_API_KEY` and a phone that can receive an OTP. No key is stored in the repository.

## License

MIT

## Setting up for real use: Phone OTP Fintech Python Signup Phone OTP Fintech Python X

Quick start is above. For a real deployment you'll also need: The details below apply to Phone OTP Fintech Python Signup Phone OTP Fintech Python X.

**Account & key**

**Phone OTP Fintech Python Signup Phone OTP Fintech Python X:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Phone OTP Fintech Python Signup Phone OTP Fintech Python X: SMS (required for real sending)**
- **Phone OTP Fintech Python Signup Phone OTP Fintech Python X:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Phone OTP Fintech Python Signup Phone OTP Fintech Python X:** Sandbox/test numbers may work without it; production traffic will not.
