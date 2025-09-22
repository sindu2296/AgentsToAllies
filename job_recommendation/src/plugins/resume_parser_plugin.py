# Example plugin for resume parsing
import json
from semantic_kernel.functions import kernel_function

class ResumeParserPlugin:
    """Native plugin exposing resume parsing as a callable SK function."""

    @kernel_function(
        name="parse_resume",
        description=(
            "Parse a resume text and extract structured information such as name, skills, experience, education. "
            "Returns a JSON object with parsed fields."
        ),
    )
    def parse_resume(self, resume_text: str) -> str:
        # Example: Use a simple rule-based extraction (replace with LLM or external API as needed)
        # For demonstration, just return the text as a single field
        # In production, integrate with an actual resume parsing API or LLM
        parsed = {
            "raw_text": resume_text,
            "name": "",
            "skills": [],
            "experience": [],
            "education": []
        }
        return json.dumps(parsed)
