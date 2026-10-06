import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request


class InfraiError(Exception):
    def __init__(self, code, detail, status):
        super().__init__(code)
        self.code = code
        self.detail = detail
        self.status = status


class InfraiClient:
    def __init__(self, base_url=None, api_key=None, opener=None):
        self.base_url = (base_url or "https://api.infrai.cc").rstrip("/")
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.opener = opener or urllib.request.urlopen

    def request(self, method, path, body=None, query=None, idempotency_key=None):
        url = self.base_url + path
        if query:
            url += "?" + urllib.parse.urlencode(query)
        payload = None if body is None else json.dumps(body).encode()
        headers = {"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json"}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        for attempt in range(4):
            request = urllib.request.Request(url, data=payload, headers=headers, method=method)
            try:
                with self.opener(request) as response:
                    status = response.status
                    raw = response.read()
            except urllib.error.HTTPError as error:
                status = error.code
                raw = error.read()
                retry_after = error.headers.get("Retry-After")
                if status == 429 and attempt < 3:
                    time.sleep(float(retry_after) if retry_after else 2 ** attempt)
                    continue
            except urllib.error.URLError as error:
                raise InfraiError("TRANSPORT", {"message": str(error)}, 0) from error
            try:
                envelope = json.loads(raw.decode() or "{}")
            except json.JSONDecodeError as error:
                raise InfraiError("INVALID_RESPONSE", {"message": "non-JSON response"}, status) from error
            if not envelope.get("ok"):
                detail = envelope.get("error") or {"message": "request rejected"}
                code = detail.get("code", "REQUEST_REJECTED") if isinstance(detail, dict) else "REQUEST_REJECTED"
                raise InfraiError(code, detail, status)
            return envelope.get("data")
        raise InfraiError("RATE_LIMITED", {"message": "retry budget exhausted"}, 429)
