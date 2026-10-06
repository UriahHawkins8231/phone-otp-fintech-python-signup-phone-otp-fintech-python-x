from src.signup_service import PaymentEvent, SignupService


class FakeClient:
    def request(self, method, path, body=None, query=None):
        return {"user_id": "u-1"}


def test_untrusted_large_payment_requires_review():
    service = SignupService(FakeClient())
    event = PaymentEvent("u-1", 125000, "USD", False)
    assert service.decide_payment(event) == "review"


def test_trusted_small_payment_is_approved():
    service = SignupService(FakeClient())
    event = PaymentEvent("u-1", 2500, "USD", True)
    assert service.decide_payment(event) == "approve"
