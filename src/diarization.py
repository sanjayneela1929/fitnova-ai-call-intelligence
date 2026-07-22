def assign_speaker_labels(transcript_segments):
    """
    Assigns simple speaker labels to transcript segments.

    This is a prototype diarisation approach.
    Later, this module can be replaced with
    pyannote.audio for real speaker diarisation.
    """

    labeled_segments = []

    for index, segment in enumerate(transcript_segments):

        # Temporary prototype logic
        if index % 2 == 0:
            speaker = "Advisor"
        else:
            speaker = "Customer"

        labeled_segments.append(
            {
                "start": segment["start"],
                "end": segment["end"],
                "speaker": speaker,
                "text": segment["text"]
            }
        )

    return labeled_segments