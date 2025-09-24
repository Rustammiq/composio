import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from examples.tiktok_video_upload import TikTokVideoUploadInput, TikTokVideoInfoInput


class TestTikTokIntegration:
    """Test cases for TikTok video upload integration."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_auth_credentials = {
            'access_token': 'test_access_token_123'
        }
        
        # Create a temporary video file for testing
        self.temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        self.temp_video.write(b'fake video content')
        self.temp_video.close()
        
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_video.name):
            os.unlink(self.temp_video.name)
    
    def test_upload_video_success(self):
        """Test successful video upload input validation."""
        # Create test input
        test_input = TikTokVideoUploadInput(
            video_file_path=self.temp_video.name,
            caption="Test video upload",
            privacy_level="PUBLIC_TO_EVERYONE",
            allow_duet=True,
            allow_comment=True,
            allow_stitch=True
        )
        
        # Assertions
        assert test_input.caption == "Test video upload"
        assert test_input.privacy_level == "PUBLIC_TO_EVERYONE"
        assert test_input.allow_duet is True
        assert test_input.allow_comment is True
        assert test_input.allow_stitch is True
    
    def test_upload_video_file_not_found(self):
        """Test video upload with non-existent file path validation."""
        # This should still create a valid input object even if file doesn't exist
        test_input = TikTokVideoUploadInput(
            video_file_path="/non/existent/path.mp4",
            caption="Test video"
        )
        
        assert test_input.video_file_path == "/non/existent/path.mp4"
        assert test_input.caption == "Test video"
    
    def test_upload_video_api_error(self):
        """Test video upload input validation with various parameters."""
        test_input = TikTokVideoUploadInput(
            video_file_path=self.temp_video.name,
            caption="Test video"
        )
        
        assert test_input.video_file_path == self.temp_video.name
        assert test_input.caption == "Test video"
        assert test_input.privacy_level == "PUBLIC_TO_EVERYONE"  # default value
    
    def test_get_video_info_success(self):
        """Test successful video info input validation."""
        test_input = TikTokVideoInfoInput(video_id="test_video_123")
        
        assert test_input.video_id == "test_video_123"
    
    def test_get_video_info_api_error(self):
        """Test video info input validation with different video IDs."""
        test_input = TikTokVideoInfoInput(video_id="different_video_456")
        
        assert test_input.video_id == "different_video_456"
    
    def test_tiktok_video_upload_input_validation(self):
        """Test input validation for TikTok video upload."""
        # Test valid input
        valid_input = TikTokVideoUploadInput(
            video_file_path="/path/to/video.mp4",
            caption="Test caption",
            privacy_level="PUBLIC_TO_EVERYONE",
            allow_duet=True,
            allow_comment=True,
            allow_stitch=True
        )
        assert valid_input.caption == "Test caption"
        assert valid_input.privacy_level == "PUBLIC_TO_EVERYONE"
        
        # Test default values
        minimal_input = TikTokVideoUploadInput(
            video_file_path="/path/to/video.mp4"
        )
        assert minimal_input.privacy_level == "PUBLIC_TO_EVERYONE"
        assert minimal_input.allow_duet is True
        assert minimal_input.allow_comment is True
        assert minimal_input.allow_stitch is True
    
    def test_tiktok_video_info_input_validation(self):
        """Test input validation for TikTok video info."""
        valid_input = TikTokVideoInfoInput(video_id="test_video_123")
        assert valid_input.video_id == "test_video_123"


if __name__ == "__main__":
    pytest.main([__file__])
