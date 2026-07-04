import asyncio
import httpx
import time

URL = "http://127.0.0.1:8000/posts/async"

async def hit(t, client: httpx.AsyncClient):
    start = time.perf_counter()
    r = await client.get(URL, params={"t": t})
    elapsed = time.perf_counter() - start
    return t, elapsed, r.json()




async def main():

    timeout = httpx.Timeout(20.0)
    limits = httpx.Limits(max_keepalive_connections=12, max_connections=10)
    async with (httpx.AsyncClient(timeout=timeout, limits=limits) as client):
        start = time.perf_counter()
        results = await asyncio.gather(
            hit(3.0, client),
            hit(5.5, client),
            hit(8.3, client),
            hit(9.8, client),
            return_exceptions=True,
        )
        total = time.perf_counter() - start

    print("---Resultados ---")
    for res in results:

        if isinstance(res, Exception):
            print("Error:", repr(res))
        else:
            t, elapsed, body = res
            print(f"sleep={t:<4}  tardo={elapsed:.2f}s   respuesta={body}")
    print(f"Tiempo total de pared: {total:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())