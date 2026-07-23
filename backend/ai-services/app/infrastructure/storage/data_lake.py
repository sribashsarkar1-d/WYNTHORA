import os
import json
import asyncio
from datetime import datetime
from typing import Union

STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../storage"))

class DataLakeManager:
    """
    Manages saving and loading of raw API payloads to the local Data Lake.
    Enforces the 'Store every original payload, never overwrite' principle.
    """
    
    @staticmethod
    def _write_sync(filepath: str, payload: Union[dict, list, str]):
        with open(filepath, "w", encoding="utf-8") as f:
            if isinstance(payload, (dict, list)):
                json.dump(payload, f, indent=2, ensure_ascii=False)
            else:
                f.write(str(payload))

    @staticmethod
    async def save_raw_payload(source_name: str, payload: Union[dict, list, str]) -> str:
        """
        Saves a raw payload to storage/raw/<source_name>/<timestamp>.json
        Returns the saved absolute file path.
        """
        raw_dir = os.path.join(STORAGE_DIR, "raw", source_name.lower())
        os.makedirs(raw_dir, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        filepath = os.path.join(raw_dir, f"{timestamp}.json")
        
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                pass # Fallback to save as string

        # Offload file IO to a thread to prevent blocking the async event loop
        await asyncio.to_thread(DataLakeManager._write_sync, filepath, payload)
                
        return filepath
