"""
Tests for the unified ModerationResult model.

The project uses a single ModerationResult schema for all moderation agents
(text, image, video, audio) so the system behaves predictably everywhere.
"""

import pytest
from pydantic import ValidationError

from multimodal_moderation.types.moderation_result import ModerationResult


class TestModerationResult:
    """Test the unified ModerationResult class"""

    def test_has_rationale_field(self):
        """Verify ModerationResult has rationale field"""
        result = ModerationResult(rationale="Test rationale")
        assert hasattr(result, "rationale"), "ModerationResult should have a 'rationale' attribute"
        assert isinstance(result.rationale, str), "rationale should be a string"
        assert result.rationale == "Test rationale", "rationale should contain the provided value"

    def test_rationale_is_required(self):
        """Verify rationale field is required"""
        with pytest.raises(ValidationError, match="rationale"):
            ModerationResult()

    def test_is_pydantic_model(self):
        """Verify ModerationResult is a Pydantic BaseModel"""
        result = ModerationResult(rationale="Test")
        assert hasattr(result, "model_dump"), "ModerationResult should have model_dump method (Pydantic BaseModel)"
        assert hasattr(result, "model_validate"), "ModerationResult should have model_validate method (Pydantic BaseModel)"

    def test_has_all_required_fields(self):
        """Verify ModerationResult has contains_pii, is_unfriendly, is_unprofessional, and rationale"""
        result = ModerationResult(
            rationale="Test rationale",
            contains_pii=True,
            is_unfriendly=False,
            is_unprofessional=True,
        )
        assert hasattr(result, "rationale"), "ModerationResult should have 'rationale' field"
        assert hasattr(result, "contains_pii"), "ModerationResult should have 'contains_pii' field"
        assert hasattr(result, "is_unfriendly"), "ModerationResult should have 'is_unfriendly' field"
        assert hasattr(result, "is_unprofessional"), "ModerationResult should have 'is_unprofessional' field"

    def test_has_image_video_audio_fields(self):
        """Verify ModerationResult has is_disturbing, is_low_quality, transcription for multimodal use"""
        result = ModerationResult(
            rationale="Test",
            is_disturbing=True,
            is_low_quality=False,
            transcription="Hello",
        )
        assert hasattr(result, "is_disturbing"), "ModerationResult should have 'is_disturbing' field"
        assert hasattr(result, "is_low_quality"), "ModerationResult should have 'is_low_quality' field"
        assert hasattr(result, "transcription"), "ModerationResult should have 'transcription' field"

    def test_field_types(self):
        """Verify all fields have correct types"""
        result = ModerationResult(
            rationale="Test rationale",
            contains_pii=True,
            is_unfriendly=False,
            is_unprofessional=False,
            is_disturbing=False,
            is_low_quality=False,
            transcription="",
        )
        assert isinstance(result.rationale, str), "rationale should be a string"
        assert isinstance(result.contains_pii, bool), "contains_pii should be a boolean"
        assert isinstance(result.is_unfriendly, bool), "is_unfriendly should be a boolean"
        assert isinstance(result.is_unprofessional, bool), "is_unprofessional should be a boolean"
        assert isinstance(result.is_disturbing, bool), "is_disturbing should be a boolean"
        assert isinstance(result.is_low_quality, bool), "is_low_quality should be a boolean"
        assert isinstance(result.transcription, str), "transcription should be a string"

    def test_sensible_defaults(self):
        """Verify optional fields have sensible default values"""
        result = ModerationResult(rationale="Test")
        assert result.contains_pii is False, "contains_pii should default to False"
        assert result.is_unfriendly is False, "is_unfriendly should default to False"
        assert result.is_unprofessional is False, "is_unprofessional should default to False"
        assert result.is_disturbing is False, "is_disturbing should default to False"
        assert result.is_low_quality is False, "is_low_quality should default to False"
        assert result.transcription == "", "transcription should default to empty string"
