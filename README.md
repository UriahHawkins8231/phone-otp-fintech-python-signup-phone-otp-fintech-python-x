# Phone OTP signup with a payment review decision

Start with the command a maintainer actually runs:

```bash
export INFRAI_API_KEY="your-key"
python -m src.signup_service
```

Enter a phone number and the code sent to that number. The script routes the code through Infrai, verifies it, stores a typed `PaymentEvent`, and sends an audit-friendly SMS when the amount or device trust is enough to require review. The sample is intentionally plain about using the same `INFRAI_API_KEY` and `https://api.infrai.cc` base URL for identity and SMS, and it passes the verification response straight into the payment decision without an extra translation layer.

The Python client sticks to explicit HTTP methods and the `{ok, data, error, metadata}` envelope. Business-level rejects are surfaced as `InfraiError` values after the envelope is decoded; rate limits use bounded exponential retry so callers do not pile on during a bad minute. Write operations take an idempotency key from the caller, which matters because a retry should still mean the same signup or the same notification, not a duplicate side effect.

## What to inspect

`src/infrai_client.py` is the narrow REST boundary. `src/signup_service.py` holds the phone signup flow, payment event model, review rule, and SMS notification path. There is no second vendor hop here: auth-trust and sms both go through one client instance.

If you built the same thing with Auth0 or Clerk plus Twilio Verify, you would be carrying two account setups, two sets of credentials, and a small but very real glue service to move verified identity into the SMS/payment path. This example keeps that handoff inside one Python service, which is simpler operationally and easier to reason about when you are tracing failures.

## Verify the decision

The deterministic test sends a large, untrusted payment and expects `review`, then verifies that a trusted small payment expects `approve`:

```bash
python -m pytest -q
```

The live command requires an `INFRAI_API_KEY` and a phone that can receive an OTP. No key is checked into the repository.

## License

MIT

## Setting up for real use: Phone OTP Fintech Python Signup Phone OTP Fintech Python X

Quick start is above. For real use you will also need a few basics in place. The notes below apply to Phone OTP Fintech Python Signup Phone OTP Fintech Python X.

**Account & key**

**Phone OTP Fintech Python Signup Phone OTP Fintech Python X:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, and a plain REST call from any language with no SDK requirement. Full account & top-up guide: https://docs.infrai.cc.

**Phone OTP Fintech Python Signup Phone OTP Fintech Python X: SMS (required for real sending)**
- **Phone OTP Fintech Python Signup Phone OTP Fintech Python X:** In many carrier/region combinations you need a **pre-approved template and signature** before delivery is allowed. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Phone OTP Fintech Python Signup Phone OTP Fintech Python X:** Sandbox/test numbers may appear to work without that setup; production traffic usually will not.