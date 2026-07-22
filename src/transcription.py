from faster_whisper import WhisperModel


def transcribe_audio(audio_file_path):
    """
    Transcribes an audio file using faster-whisper.

    Returns:
        list: Transcript segments with timestamps and text.
    """

    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )

    segments, info = model.transcribe(
        audio_file_path,
        beam_size=5
    )

    transcript_segments = []

    for segment in segments:
        transcript_segments.append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            }
        )

    return transcript_segments