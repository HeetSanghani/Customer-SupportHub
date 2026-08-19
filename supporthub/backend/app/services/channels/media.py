import os
import uuid
import mimetypes
import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

class GenericMediaDownloader:
    """
    A unified utility to securely download media from any external URL and 
    save it to the local SupportHub uploads directory.
    """
    
    @staticmethod
    async def download_url(
        url: str, 
        headers: Optional[dict] = None, 
        expected_mime_type: Optional[str] = None
    ) -> tuple[Optional[str], Optional[str]]:
        """
        Download media from a URL and save it locally.
        
        Args:
            url: The absolute URL to download the file from.
            headers: Optional HTTP headers (e.g. for Bearer token auth).
            expected_mime_type: Fallback mime type if the server doesn't provide one.
            
        Returns:
            Tuple of (local_file_url, local_filename). Returns (None, None) on failure.
        """
        if not url:
            return None, None
            
        try:
            async with httpx.AsyncClient(timeout=15.0) as http_client:
                media_res = await http_client.get(url, headers=headers)
                
                if media_res.status_code != 200:
                    logger.error("Failed to download media binary from %s: %s", url, media_res.status_code)
                    return None, None
                
                # Try to determine mime type from the response, fallback to provided
                content_type = media_res.headers.get("Content-Type", "")
                mime_type = content_type.split(";")[0].strip() if content_type else expected_mime_type
                    
                # Setup uploads directory
                upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads"))
                os.makedirs(upload_dir, exist_ok=True)
                
                # Guess extension
                ext = mimetypes.guess_extension(mime_type) if mime_type else ""
                
                # Fallbacks for common types that mimetypes sometimes struggles with
                if not ext:
                    if mime_type == "image/jpeg": ext = ".jpg"
                    elif mime_type == "image/webp": ext = ".webp"
                    elif mime_type == "audio/ogg; codecs=opus": ext = ".ogg"
                    elif mime_type == "audio/ogg": ext = ".ogg"
                    elif mime_type == "video/mp4": ext = ".mp4"
                    else: ext = ".bin"
                    
                filename = f"{uuid.uuid4().hex}{ext}"
                file_path = os.path.join(upload_dir, filename)
                
                with open(file_path, "wb") as f:
                    f.write(media_res.content)
                    
                from app.config import get_settings as _get_settings
                local_url = f"{_get_settings().backend_url}/static/uploads/{filename}"
                logger.info("Successfully downloaded generic media -> %s", filename)
                return local_url, filename
                
        except Exception as exc:
            logger.error("Error downloading media from %s: %s", url, exc)
            return None, None
