# api.py
import aiohttp
import asyncio

BASE_URL = "https://api.harvardartmuseums.org/object"

async def fetch_harvard(api_key, classification, size=100):
    """
    Fetch artifacts from Harvard API, including metadata, media, and colors.
    Returns: meta, media, colors lists ready for DB insertion.
    """
    params = {
        "apikey": api_key,
        "classification": classification,
        "size": size,
        "page": 1
    }

    metadata = []
    media = []
    colors = []

    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(BASE_URL, params=params) as response:
                data = await response.json()

            records = data.get("records", [])
            if not records:
                break

            for item in records:
                artifact_id = str(item.get("id"))

                # Metadata
                metadata.append({
                    "id": artifact_id,
                    "classification": item.get("classification"),
                    "title": item.get("title"),
                    "culture": item.get("culture"),
                    "period": item.get("period"),
                    "century": item.get("century")
                })

                # Media
                images = item.get("images") or []
                for img in images:
                    media.append({
                        "id": str(img.get("id")),
                        "artifact_id": artifact_id,
                        "type": img.get("technique"),
                        "url": img.get("baseimageurl")
                    })

                # Colors
                item_colors = item.get("colors") or []
                for c in item_colors:
                    colors.append({
                        "id": artifact_id + "_" + c.get("color"),
                        "artifact_id": artifact_id,
                        "color": c.get("color")
                    })

            # Pagination
            if "info" in data and data["info"].get("next"):
                params["page"] += 1
            else:
                break

    return metadata, media, colors
