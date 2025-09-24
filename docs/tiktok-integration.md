# TikTok Video Upload Integration

This integration allows you to upload videos to TikTok and retrieve video information using the TikTok API through Composio.

## Features

- **Video Upload**: Upload videos to TikTok with customizable privacy settings
- **Video Information**: Retrieve information about uploaded videos
- **Privacy Controls**: Set privacy levels, duet permissions, comment settings, and stitch permissions
- **Error Handling**: Comprehensive error handling for file operations and API calls

## Setup

### 1. TikTok API Access

To use this integration, you need:

1. A TikTok Developer Account
2. TikTok API credentials (Access Token)
3. Proper permissions for video upload

### 2. Authentication

Set up your TikTok API credentials in your Composio configuration:

```python
from composio import Composio

composio = Composio(
    api_key="your_composio_api_key"
)

# Configure TikTok authentication
composio.toolkits.configure(
    toolkit="tiktok",
    auth_credentials={
        "access_token": "your_tiktok_access_token"
    }
)
```

## Usage

### Python SDK

#### Upload a Video

```python
from composio import Composio
from examples.tiktok_video_upload import upload_video_to_tiktok

composio = Composio()

# Upload a video
response = composio.tools.execute(
    user_id="default",
    slug=upload_video_to_tiktok.slug,
    arguments={
        "video_file_path": "/path/to/your/video.mp4",
        "caption": "Check out this amazing video! #composio #ai",
        "privacy_level": "PUBLIC_TO_EVERYONE",
        "allow_duet": True,
        "allow_comment": True,
        "allow_stitch": True
    },
)

print(response)
```

#### Get Video Information

```python
from examples.tiktok_video_upload import get_tiktok_video_info

# Get video information
response = composio.tools.execute(
    user_id="default",
    slug=get_tiktok_video_info.slug,
    arguments={
        "video_id": "your_video_id"
    },
)

print(response)
```

### TypeScript SDK

```typescript
import { Composio } from '@composio/core';
import { uploadVideoToTikTok, getTikTokVideoInfo } from './examples/tiktok-video-upload';

const composio = new Composio({
  apiKey: process.env.COMPOSIO_API_KEY,
});

// Upload a video
const uploadResponse = await composio.tools.execute({
  userId: 'default',
  slug: uploadVideoToTikTok.slug,
  arguments: {
    videoFilePath: '/path/to/your/video.mp4',
    caption: 'Check out this amazing video! #composio #ai',
    privacyLevel: 'PUBLIC_TO_EVERYONE',
    allowDuet: true,
    allowComment: true,
    allowStitch: true
  },
});

console.log('Upload Response:', uploadResponse);
```

## Parameters

### Video Upload Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `video_file_path` | string | Yes | - | Path to the video file to upload |
| `caption` | string | No | - | Caption for the TikTok video |
| `privacy_level` | string | No | "PUBLIC_TO_EVERYONE" | Privacy level: "PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIEND", "SELF_ONLY" |
| `allow_duet` | boolean | No | true | Allow others to duet with this video |
| `allow_stitch` | boolean | No | true | Allow others to stitch with this video |
| `allow_comment` | boolean | No | true | Allow comments on this video |

### Video Info Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `video_id` | string | Yes | The ID of the TikTok video to get information about |

## Privacy Levels

- **PUBLIC_TO_EVERYONE**: Video is visible to all TikTok users
- **MUTUAL_FOLLOW_FRIEND**: Video is visible only to mutual followers and friends
- **SELF_ONLY**: Video is visible only to the uploader

## Error Handling

The integration includes comprehensive error handling:

- **File Not Found**: Returns error if video file doesn't exist
- **API Errors**: Handles TikTok API errors gracefully
- **Authentication Errors**: Manages authentication failures
- **Network Errors**: Handles network connectivity issues

## Response Format

### Successful Upload Response

```json
{
  "success": true,
  "message": "Video uploaded successfully to TikTok",
  "data": {
    "video_id": "tiktok_video_123",
    "status": "success"
  },
  "video_info": {
    "file_path": "/path/to/video.mp4",
    "caption": "Check out this amazing video!",
    "privacy_level": "PUBLIC_TO_EVERYONE"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Video file not found: /path/to/video.mp4",
  "message": "Video file not found"
}
```

## Testing

Run the test suite to verify the integration:

```bash
cd /Users/innovars_lab/composio-custom/python
python -m pytest tests/test_tiktok_integration.py -v
```

## Supported Video Formats

The TikTok API supports various video formats including:
- MP4
- MOV
- AVI
- WMV

## File Size Limits

- Maximum file size: 287MB
- Recommended resolution: 1080x1920 (9:16 aspect ratio)
- Duration: 15 seconds to 10 minutes

## Rate Limits

Be aware of TikTok API rate limits:
- Upload requests: Limited per hour
- Information requests: Limited per day

## Contributing

To contribute to this integration:

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Write tests
5. Submit a pull request

## License

This integration is part of the Composio project and follows the same MIT license.
