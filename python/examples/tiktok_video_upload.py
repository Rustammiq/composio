import requests
import base64
from pydantic import BaseModel, Field
from typing import Optional
import os

from composio import Composio
from composio.types import ExecuteRequestFn

composio = Composio()


class TikTokVideoUploadInput(BaseModel):
    video_file_path: str = Field(
        ...,
        description="Path to the video file to upload to TikTok"
    )
    caption: Optional[str] = Field(
        None,
        description="Caption for the TikTok video"
    )
    privacy_level: str = Field(
        "PUBLIC_TO_EVERYONE",
        description="Privacy level: PUBLIC_TO_EVERYONE, MUTUAL_FOLLOW_FRIEND, SELF_ONLY"
    )
    allow_duet: bool = Field(
        True,
        description="Allow others to duet with this video"
    )
    allow_stitch: bool = Field(
        True,
        description="Allow others to stitch with this video"
    )
    allow_comment: bool = Field(
        True,
        description="Allow comments on this video"
    )


@composio.tools.custom_tool(toolkit="tiktok")
def upload_video_to_tiktok(
    request: TikTokVideoUploadInput,
    execute_request: ExecuteRequestFn,
    auth_credentials: dict,
) -> dict:
    """
    Upload a video to TikTok using the TikTok API.
    
    This tool allows you to upload videos to TikTok with various privacy settings
    and content controls.
    """
    try:
        # Check if video file exists
        if not os.path.exists(request.video_file_path):
            raise FileNotFoundError(f"Video file not found: {request.video_file_path}")
        
        # Read and encode video file
        with open(request.video_file_path, 'rb') as video_file:
            video_data = video_file.read()
            video_base64 = base64.b64encode(video_data).decode('utf-8')
        
        # Prepare the request payload
        payload = {
            "video": {
                "video_data": video_base64
            },
            "post_info": {
                "title": request.caption or "Uploaded via Composio",
                "privacy_level": request.privacy_level,
                "disable_duet": not request.allow_duet,
                "disable_comment": not request.allow_comment,
                "disable_stitch": not request.allow_stitch,
                "video_cover_timestamp_ms": 1000
            }
        }
        
        # Make the API request to TikTok
        response = execute_request(
            endpoint="/v2/post/publish/video/init/",
            method="POST",
            parameters=[
                {
                    "name": "Authorization",
                    "value": f"Bearer {auth_credentials.get('access_token', '')}",
                    "type": "header",
                },
                {
                    "name": "Content-Type",
                    "value": "application/json",
                    "type": "header",
                },
            ],
            data=payload
        )
        
        return {
            "success": True,
            "message": "Video uploaded successfully to TikTok",
            "data": response.data,
            "video_info": {
                "file_path": request.video_file_path,
                "caption": request.caption,
                "privacy_level": request.privacy_level
            }
        }
        
    except FileNotFoundError as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Video file not found"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to upload video to TikTok"
        }


class TikTokVideoInfoInput(BaseModel):
    video_id: str = Field(
        ...,
        description="The ID of the TikTok video to get information about"
    )


@composio.tools.custom_tool(toolkit="tiktok")
def get_tiktok_video_info(
    request: TikTokVideoInfoInput,
    execute_request: ExecuteRequestFn,
    auth_credentials: dict,
) -> dict:
    """
    Get information about a TikTok video.
    """
    try:
        response = execute_request(
            endpoint=f"/v2/video/info/",
            method="GET",
            parameters=[
                {
                    "name": "Authorization",
                    "value": f"Bearer {auth_credentials.get('access_token', '')}",
                    "type": "header",
                },
                {
                    "name": "video_id",
                    "value": request.video_id,
                    "type": "query",
                },
            ]
        )
        
        return {
            "success": True,
            "data": response.data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get video information"
        }


# Example usage
if __name__ == "__main__":
    # Example: Upload a video
    response = composio.tools.execute(
        user_id="default",
        slug=upload_video_to_tiktok.slug,
        arguments={
            "video_file_path": "/path/to/your/video.mp4",
            "caption": "Check out this amazing video! #composio #ai",
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "allow_duet": True,
            "allow_comment": True
        },
    )
    
    print("Upload Response:", response)
