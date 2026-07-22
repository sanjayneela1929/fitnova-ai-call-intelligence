from src.transcription import transcribe_audio

from src.diarization import assign_speaker_labels

from src.llm_analysis import analyze_call_with_llm


def process_call(audio_file_path):
    """
    Processes an audio call from start to finish.

    Pipeline:

    1. Transcribe audio
    2. Assign speaker labels
    3. Analyze call using Gemini

    Returns:
        tuple:
            transcript
            labeled_transcript
            analysis_result
    """

    transcript = transcribe_audio(
        audio_file_path
    )

    labeled_transcript = assign_speaker_labels(
        transcript
    )

    analysis_result = analyze_call_with_llm(
        labeled_transcript
    )

    return (

        transcript,

        labeled_transcript,

        analysis_result

    )