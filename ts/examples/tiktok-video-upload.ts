import { Composio } from '@composio/core';
import { z } from 'zod';
import * as fs from 'fs';

const composio = new Composio({
  apiKey: process.env.COMPOSIO_API_KEY,
});

// TikTok Video Upload Input Schema
const TikTokVideoUploadInput = z.object({
  videoFilePath: z.string().describe('Path to the video file to upload to TikTok'),
  caption: z.string().optional().describe('Caption for the TikTok video'),
  privacyLevel: z.enum(['PUBLIC_TO_EVERYONE', 'MUTUAL_FOLLOW_FRIEND', 'SELF_ONLY'])
    .default('PUBLIC_TO_EVERYONE')
    .describe('Privacy level for the video'),
  allowDuet: z.boolean().default(true).describe('Allow others to duet with this video'),
  allowStitch: z.boolean().default(true).describe('Allow others to stitch with this video'),
  allowComment: z.boolean().default(true).describe('Allow comments on this video'),
});

// TikTok Video Info Input Schema
const TikTokVideoInfoInput = z.object({
  videoId: z.string().describe('The ID of the TikTok video to get information about'),
});

// Register TikTok Video Upload Tool
const uploadVideoToTikTok = composio.tools.register({
  name: 'upload_video_to_tiktok',
  description: 'Upload a video to TikTok using the TikTok API with various privacy settings and content controls',
  parameters: TikTokVideoUploadInput,
  toolkit: 'tiktok',
  execute: async (params, { executeRequest, authCredentials }) => {
    try {
      const { videoFilePath, caption, privacyLevel, allowDuet, allowComment, allowStitch } = params;
      
      // Check if video file exists
      if (!fs.existsSync(videoFilePath)) {
        throw new Error(`Video file not found: ${videoFilePath}`);
      }
      
      // Read and encode video file
      const videoData = fs.readFileSync(videoFilePath);
      const videoBase64 = videoData.toString('base64');
      
      // Prepare the request payload
      const payload = {
        video: {
          video_data: videoBase64
        },
        post_info: {
          title: caption || 'Uploaded via Composio',
          privacy_level: privacyLevel,
          disable_duet: !allowDuet,
          disable_comment: !allowComment,
          disable_stitch: !allowStitch,
          video_cover_timestamp_ms: 1000
        }
      };
      
      // Make the API request to TikTok
      const response = await executeRequest({
        endpoint: '/v2/post/publish/video/init/',
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authCredentials.access_token}`,
          'Content-Type': 'application/json',
        },
        data: payload
      });
      
      return {
        success: true,
        message: 'Video uploaded successfully to TikTok',
        data: response.data,
        videoInfo: {
          filePath: videoFilePath,
          caption: caption,
          privacyLevel: privacyLevel
        }
      };
      
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        message: 'Failed to upload video to TikTok'
      };
    }
  }
});

// Register TikTok Video Info Tool
const getTikTokVideoInfo = composio.tools.register({
  name: 'get_tiktok_video_info',
  description: 'Get information about a TikTok video',
  parameters: TikTokVideoInfoInput,
  toolkit: 'tiktok',
  execute: async (params, { executeRequest, authCredentials }) => {
    try {
      const { videoId } = params;
      
      const response = await executeRequest({
        endpoint: '/v2/video/info/',
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authCredentials.access_token}`,
        },
        queryParams: {
          video_id: videoId
        }
      });
      
      return {
        success: true,
        data: response.data
      };
      
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        message: 'Failed to get video information'
      };
    }
  }
});

// Example usage function
export async function exampleTikTokUpload() {
  try {
    // Example: Upload a video
    const uploadResponse = await composio.tools.execute({
      userId: 'default',
      slug: uploadVideoToTikTok.slug,
      arguments: {
        videoFilePath: '/path/to/your/video.mp4',
        caption: 'Check out this amazing video! #composio #ai',
        privacyLevel: 'PUBLIC_TO_EVERYONE' as const,
        allowDuet: true,
        allowComment: true,
        allowStitch: true
      },
    });
    
    console.log('Upload Response:', uploadResponse);
    
    // Example: Get video info (if you have a video ID)
    if (uploadResponse.data?.video_id) {
      const infoResponse = await composio.tools.execute({
        userId: 'default',
        slug: getTikTokVideoInfo.slug,
        arguments: {
          videoId: uploadResponse.data.video_id
        },
      });
      
      console.log('Video Info Response:', infoResponse);
    }
    
  } catch (error) {
    console.error('Error:', error);
  }
}

// Export the tools for use in other modules
export { uploadVideoToTikTok, getTikTokVideoInfo };
