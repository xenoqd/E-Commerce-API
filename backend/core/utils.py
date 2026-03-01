from fastapi import Request


def get_client_ip(request: Request) -> str:
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        print("X-Forwarded-For:", xff)
        return xff.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        print("X-Real-IP:", real_ip)
        return real_ip.strip()

    client_host = request.client.host
    print("Final client_host:", client_host)
    return client_host or "unknown"
