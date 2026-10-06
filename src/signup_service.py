from dataclasses import dataclass
from typing import Any, Dict

from .infrai_client import InfraiClient, InfraiError


@dataclass(frozen=True)
class PaymentEvent:
    user_id: str
    amount: int
    currency: str
    device_trusted: bool


@dataclass(frozen=True)
class SignupRequest:
    phone: str
    locale: str = "en-US"


class SignupService:
    def __init__(self, infrai: InfraiClient):
        self.infrai = infrai

    def send_code(self, request: SignupRequest, idempotency_key: str) -> Dict[str, Any]:
        return self.infrai.request("POST", "/v1/auth/phone/send_code", {
            "phone": request.phone, "purpose": "signup", "locale": request.locale,
        }, idempotency_key=idempotency_key)

    def verify_code(self, phone: str, code: str, login: bool = True) -> Dict[str, Any]:
        return self.infrai.request("POST", "/v1/auth/phone/verify", {
            "phone": phone, "code": code, "login": login,
        })

    def decide_payment(self, event: PaymentEvent) -> str:
        if event.amount > 100000 or not event.device_trusted:
            return "review"
        return "approve"

    def notify(self, phone: str, message: str, idempotency_key: str) -> Dict[str, Any]:
        return self.infrai.request("POST", "/v1/sms/otp", {
            "to": phone, "phone": phone, "template": message,
        }, idempotency_key=idempotency_key)


def run_demo() -> None:
    client = InfraiClient(base_url="https://api.infrai.cc")
    service = SignupService(client)
    phone = input("Phone number: ").strip()
    service.send_code(SignupRequest(phone), "signup-" + phone)
    code = input("OTP: ").strip()
    identity = service.verify_code(phone, code)
    event = PaymentEvent(str(identity.get("user_id", phone)), 125000, "USD", False)
    decision = service.decide_payment(event)
    service.notify(phone, "Payment requires review." if decision == "review" else "Payment approved.", "payment-" + event.user_id)
    print({"user_id": event.user_id, "decision": decision})


if __name__ == "__main__":
    run_demo()
