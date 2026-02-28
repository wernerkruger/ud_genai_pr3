"""
Unified moderation result schema used by all moderation agents (text, image, video, audio).

A single ModerationResult model ensures consistent structure across the API and UI:
all endpoints return the same shape; agents set only the fields relevant to their content type.
"""

from pydantic import BaseModel, Field


class ModerationResult(BaseModel):
    """
    Single shared moderation output used by all agents.

    Required for all: rationale.
    Text/audio: contains_pii, is_unfriendly, is_unprofessional.
    Image/video: contains_pii, is_disturbing, is_low_quality.
    Audio only: transcription.
    Fields not relevant to a content type are set to False or empty by the agent.
    """

    rationale: str = Field(description="Explanation of what was harmful and why")

    # Used by text and audio moderation
    contains_pii: bool = Field(
        default=False,
        description="Whether the content contains personally-identifiable information (PII)",
    )
    is_unfriendly: bool = Field(
        default=False,
        description="Whether unfriendly tone or content was detected",
    )
    is_unprofessional: bool = Field(
        default=False,
        description="Whether unprofessional tone or content was detected",
    )

    # Used by image and video moderation
    is_disturbing: bool = Field(
        default=False,
        description="Whether the content is disturbing",
    )
    is_low_quality: bool = Field(
        default=False,
        description="Whether the content is low quality",
    )

    # Used by audio moderation only
    transcription: str = Field(
        default="",
        description="Transcription of the audio content (audio only)",
    )
