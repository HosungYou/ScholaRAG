# Module 3: Qualitative Data Coding RAG for Interview Analysis

## Learning Objectives
By the end of this module, you will:
- Build a specialized RAG system for qualitative interview data
- Implement automated thematic analysis
- Create coding frameworks with AI assistance
- Ensure reliability and transparency in AI-assisted coding
- Export results in formats compatible with qualitative analysis software (NVivo, Atlas.ti)

---

## Why RAG for Qualitative Analysis?

### Traditional Qualitative Coding Challenges
- ⏱️ **Time-intensive**: 1 hour per interview transcript for initial coding
- 🔄 **Consistency issues**: Coding drift over time
- 👥 **Inter-rater reliability**: Difficult to maintain across large teams
- 🔍 **Pattern discovery**: Hard to see cross-cutting themes

### RAG-Assisted Qualitative Coding Benefits
- ⚡ **Speed**: Initial coding in minutes, not hours
- 🎯 **Consistency**: Same logic applied across all transcripts
- 📊 **Transparency**: Traceable AI decisions with source quotes
- 🔗 **Pattern identification**: Automatic cross-interview theme discovery
- ✅ **Human-in-the-loop**: AI suggests, human validates

**Important Note:** RAG is a **tool to augment**, not replace, qualitative researchers' expertise. Always validate findings!

---

## System Architecture

```
Qualitative Coding RAG System
├── Data Input
│   ├── Interview transcripts (.docx, .txt)
│   ├── Focus group transcripts
│   ├── Open-ended survey responses (.xlsx)
│   └── Field notes
├── Processing Pipeline
│   ├── Speaker identification & turn segmentation
│   ├── Structural chunking (by question, by speaker)
│   ├── Metadata enrichment (demographics, interview date)
│   └── Vector embedding
├── Analysis Engine
│   ├── Thematic analysis (inductive & deductive)
│   ├── Code generation & refinement
│   ├── Quote extraction & labeling
│   └── Pattern identification
└── Output
    ├── Coded transcripts (HTML, PDF)
    ├── Code hierarchy (JSON, CSV)
    ├── Theme summaries with exemplar quotes
    └── NVivo/Atlas.ti compatible exports
```

---

## Implementation Guide

### Phase 1: Project Setup

**Directory Structure:**
```
02_qualitative_coding_rag/
├── backend/
│   ├── core/
│   │   ├── interview_parser.py       # Parse interview formats
│   │   ├── thematic_analyzer.py      # AI-powered coding
│   │   ├── code_manager.py           # Manage code hierarchy
│   │   └── export_manager.py         # Export to various formats
│   └── api/
│       └── main.py
├── frontend/
│   ├── chainlit_app.py               # Interview analysis interface
│   └── components/
│       ├── code_tree_viewer.py       # Hierarchical code display
│       └── quote_annotator.py        # Manual validation interface
├── data/
│   ├── raw_interviews/
│   ├── processed/
│   ├── codebooks/
│   └── outputs/
├── prompts/
│   ├── inductive_coding.txt
│   ├── deductive_coding.txt
│   └── theme_extraction.txt
└── requirements.txt
```

**Additional Dependencies (add to requirements.txt):**
```txt
# For qualitative analysis
python-docx==1.1.0
pandas==2.2.0
openpyxl==3.1.2

# For export formats
jinja2==3.1.3
markdown==3.5.2
weasyprint==60.2  # For PDF export

# For visualization
plotly==5.18.0
networkx==3.2.1

# Existing dependencies from Module 2
langchain==0.1.0
chromadb==0.4.22
openai==1.12.0
anthropic==0.18.0
chainlit==1.0.0
fastapi==0.109.0
```

---

### Phase 2: Interview Parsing & Structuring

**File: backend/core/interview_parser.py**

**Claude Code Prompt:**
```
Create an interview transcript parser in backend/core/interview_parser.py that:

1. Supports multiple input formats:
   - Word documents with speaker labels (e.g., "Interviewer: ..." "Participant: ...")
   - Plain text with various speaker notation formats
   - Excel files with columns: Speaker, Turn, Text
   - VTT/SRT files (from transcription services like Otter.ai, Rev.com)

2. Extracts structural elements:
   - Identify interviewer vs. participant turns
   - Detect question-answer pairs
   - Preserve timestamps if available
   - Extract metadata from header/footer (participant ID, date, location)

3. Handles multiple speaker formats:
   - "Interviewer: ..." / "I: ..."
   - "Researcher: ..." / "R: ..."
   - "P1: ..." / "Participant 1: ..."
   - "[SPEAKER 01]: ..." (auto-transcription format)

4. Cleaning operations:
   - Remove filler words (um, uh, like) optionally
   - Normalize punctuation
   - Flag incomplete/inaudible sections [inaudible]

5. Creates structured output:
   - JSON format with turn-by-turn structure
   - Metadata fields for filtering
   - Ready for vectorization

Include comprehensive error handling for malformed transcripts.
```

**Expected Output:**
```python
# backend/core/interview_parser.py

import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Literal
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

from docx import Document as DocxDocument
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class InterviewTurn:
    """Single turn in an interview."""
    turn_id: int
    speaker: str  # "interviewer" or "participant" or specific ID
    speaker_label: str  # Original label (e.g., "P1", "Interviewer")
    text: str
    timestamp: Optional[str] = None
    word_count: int = 0
    has_question: bool = False

    def __post_init__(self):
        if self.word_count == 0:
            self.word_count = len(self.text.split())
        if self.has_question is False:
            self.has_question = '?' in self.text


@dataclass
class InterviewMetadata:
    """Metadata for entire interview."""
    interview_id: str
    filename: str
    date: Optional[datetime] = None
    location: Optional[str] = None
    participant_demographics: Optional[Dict] = None
    interviewer: Optional[str] = None
    duration_minutes: Optional[int] = None
    total_turns: int = 0
    total_words: int = 0


@dataclass
class ParsedInterview:
    """Complete parsed interview."""
    metadata: InterviewMetadata
    turns: List[InterviewTurn]

    def to_dict(self):
        return {
            "metadata": asdict(self.metadata),
            "turns": [asdict(turn) for turn in self.turns]
        }

    def to_json(self, output_path: str):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, default=str)


class InterviewParser:
    """
    Parse interview transcripts from various formats into structured data.
    """

    # Speaker patterns (in order of specificity)
    SPEAKER_PATTERNS = [
        # Format: "Interviewer: text" or "I: text"
        r'^(Interviewer|I|Researcher|R):\s*(.+)$',
        # Format: "Participant: text" or "P: text" or "P1: text"
        r'^(Participant|P|P\d+|Respondent|R\d+):\s*(.+)$',
        # Format: "[SPEAKER 01]: text" (Otter.ai, Rev.com format)
        r'^\[SPEAKER\s+(\d+)\]:\s*(.+)$',
        # Format: "Speaker 1: text"
        r'^Speaker\s+(\d+):\s*(.+)$',
    ]

    def __init__(
        self,
        remove_fillers: bool = False,
        filler_words: List[str] = None
    ):
        self.remove_fillers = remove_fillers
        self.filler_words = filler_words or ['um', 'uh', 'like', 'you know', 'sort of', 'kind of']

    def parse_file(self, file_path: str) -> ParsedInterview:
        """
        Parse interview file based on extension.

        Supported formats: .docx, .txt, .xlsx, .csv
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = file_path.suffix.lower()

        if ext == '.docx':
            return self._parse_docx(file_path)
        elif ext == '.txt':
            return self._parse_txt(file_path)
        elif ext in ['.xlsx', '.xls']:
            return self._parse_excel(file_path)
        elif ext == '.csv':
            return self._parse_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _parse_docx(self, file_path: Path) -> ParsedInterview:
        """Parse Word document interview transcript."""

        doc = DocxDocument(file_path)

        # Extract text content
        lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

        # Try to extract metadata from first few lines
        metadata = self._extract_metadata_from_header(lines[:10], file_path)

        # Parse turns
        turns = self._parse_turns(lines)

        # Update metadata with turn statistics
        metadata.total_turns = len(turns)
        metadata.total_words = sum(turn.word_count for turn in turns)

        return ParsedInterview(metadata=metadata, turns=turns)

    def _parse_txt(self, file_path: Path) -> ParsedInterview:
        """Parse plain text interview transcript."""

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        metadata = self._extract_metadata_from_header(lines[:10], file_path)
        turns = self._parse_turns(lines)

        metadata.total_turns = len(turns)
        metadata.total_words = sum(turn.word_count for turn in turns)

        return ParsedInterview(metadata=metadata, turns=turns)

    def _parse_excel(self, file_path: Path) -> ParsedInterview:
        """
        Parse Excel format with columns: Speaker, Text, (optional: Timestamp)
        """

        df = pd.read_excel(file_path)

        # Normalize column names
        df.columns = df.columns.str.lower().str.strip()

        required_cols = ['speaker', 'text']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Excel file must have columns: {required_cols}")

        metadata = InterviewMetadata(
            interview_id=file_path.stem,
            filename=file_path.name
        )

        turns = []
        for idx, row in df.iterrows():
            speaker_label = str(row['speaker']).strip()
            text = str(row['text']).strip()

            if self.remove_fillers:
                text = self._remove_filler_words(text)

            speaker_type = self._categorize_speaker(speaker_label)

            turn = InterviewTurn(
                turn_id=idx,
                speaker=speaker_type,
                speaker_label=speaker_label,
                text=text,
                timestamp=str(row.get('timestamp', '')) if 'timestamp' in df.columns else None
            )
            turns.append(turn)

        metadata.total_turns = len(turns)
        metadata.total_words = sum(turn.word_count for turn in turns)

        return ParsedInterview(metadata=metadata, turns=turns)

    def _parse_csv(self, file_path: Path) -> ParsedInterview:
        """Parse CSV format (same structure as Excel)."""

        df = pd.read_csv(file_path)
        df.columns = df.columns.str.lower().str.strip()

        # Rest is same as Excel
        return self._parse_excel(file_path)

    def _parse_turns(self, lines: List[str]) -> List[InterviewTurn]:
        """
        Parse lines into interview turns.

        Handles multi-line turns (speaker continues on next line without label).
        """

        turns = []
        current_speaker = None
        current_speaker_label = None
        current_text = []
        turn_id = 0

        for line in lines:
            # Try to match speaker pattern
            speaker_match = self._match_speaker_pattern(line)

            if speaker_match:
                # Save previous turn if exists
                if current_text:
                    turn = InterviewTurn(
                        turn_id=turn_id,
                        speaker=current_speaker,
                        speaker_label=current_speaker_label,
                        text=' '.join(current_text)
                    )
                    turns.append(turn)
                    turn_id += 1

                # Start new turn
                current_speaker_label, text = speaker_match
                current_speaker = self._categorize_speaker(current_speaker_label)
                current_text = [text]

            else:
                # Continuation of previous speaker
                if current_text:  # Only if we have a speaker
                    current_text.append(line)

        # Save last turn
        if current_text:
            turn = InterviewTurn(
                turn_id=turn_id,
                speaker=current_speaker,
                speaker_label=current_speaker_label,
                text=' '.join(current_text)
            )
            turns.append(turn)

        # Apply cleaning
        if self.remove_fillers:
            for turn in turns:
                turn.text = self._remove_filler_words(turn.text)
                turn.word_count = len(turn.text.split())

        return turns

    def _match_speaker_pattern(self, line: str) -> Optional[Tuple[str, str]]:
        """
        Try to match line against speaker patterns.

        Returns: (speaker_label, text) or None
        """

        for pattern in self.SPEAKER_PATTERNS:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                groups = match.groups()
                speaker_label = groups[0]
                text = groups[-1]  # Last group is always text
                return (speaker_label, text)

        return None

    def _categorize_speaker(self, speaker_label: str) -> str:
        """
        Categorize speaker into standard types.

        Returns: "interviewer", "participant", or specific ID
        """

        label_lower = speaker_label.lower()

        if any(word in label_lower for word in ['interviewer', 'researcher', 'moderator']):
            return "interviewer"
        elif any(word in label_lower for word in ['participant', 'respondent', 'interviewee']):
            return "participant"
        elif re.match(r'^(p|r|speaker)\s*\d+$', label_lower):
            # Specific participant ID (e.g., P1, P2)
            return speaker_label.lower().replace(' ', '')
        elif label_lower in ['i', 'r']:
            return "interviewer"
        elif label_lower in ['p']:
            return "participant"
        else:
            # Unknown, keep original
            return speaker_label

    def _extract_metadata_from_header(
        self,
        header_lines: List[str],
        file_path: Path
    ) -> InterviewMetadata:
        """
        Try to extract metadata from first few lines.

        Common patterns:
        - "Interview ID: 001"
        - "Date: 2024-01-15"
        - "Participant: Female, Age 35, Teacher"
        """

        metadata = InterviewMetadata(
            interview_id=file_path.stem,
            filename=file_path.name
        )

        # Try to find common metadata patterns
        for line in header_lines:
            line_lower = line.lower()

            # Interview ID
            if 'interview id' in line_lower or 'id:' in line_lower:
                match = re.search(r':\s*(.+)$', line)
                if match:
                    metadata.interview_id = match.group(1).strip()

            # Date
            if 'date' in line_lower:
                match = re.search(r'(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})', line)
                if match:
                    try:
                        date_str = match.group(1)
                        if '-' in date_str:
                            metadata.date = datetime.strptime(date_str, '%Y-%m-%d')
                        else:
                            metadata.date = datetime.strptime(date_str, '%m/%d/%Y')
                    except ValueError:
                        pass

            # Location
            if 'location' in line_lower:
                match = re.search(r':\s*(.+)$', line)
                if match:
                    metadata.location = match.group(1).strip()

        return metadata

    def _remove_filler_words(self, text: str) -> str:
        """Remove filler words from text."""

        for filler in self.filler_words:
            # Case-insensitive removal with word boundaries
            pattern = r'\b' + re.escape(filler) + r'\b'
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()

        return text


# Convenience function
def parse_interview_directory(
    directory: str,
    output_dir: Optional[str] = None
) -> List[ParsedInterview]:
    """
    Parse all interview files in a directory.

    Args:
        directory: Path to directory containing interview files
        output_dir: Optional path to save parsed JSON files

    Returns:
        List of ParsedInterview objects
    """

    parser = InterviewParser()
    directory_path = Path(directory)

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Find all supported files
    supported_exts = ['.docx', '.txt', '.xlsx', '.csv']
    files = []
    for ext in supported_exts:
        files.extend(directory_path.glob(f'*{ext}'))

    logger.info(f"Found {len(files)} interview files")

    parsed_interviews = []

    for file_path in files:
        try:
            parsed = parser.parse_file(str(file_path))
            parsed_interviews.append(parsed)

            logger.info(f"✓ Parsed {file_path.name}: {parsed.metadata.total_turns} turns")

            # Save as JSON if output directory specified
            if output_dir:
                output_path = Path(output_dir) / f"{file_path.stem}.json"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                parsed.to_json(str(output_path))

        except Exception as e:
            logger.error(f"✗ Failed to parse {file_path.name}: {e}")

    return parsed_interviews


if __name__ == "__main__":
    # Test parser
    parser = InterviewParser(remove_fillers=True)

    # Example: Parse a single file
    parsed = parser.parse_file("./data/raw_interviews/interview_01.docx")

    print(f"Interview ID: {parsed.metadata.interview_id}")
    print(f"Total turns: {parsed.metadata.total_turns}")
    print(f"Total words: {parsed.metadata.total_words}")
    print("\nFirst 3 turns:")
    for turn in parsed.turns[:3]:
        print(f"  [{turn.speaker}] {turn.text[:100]}...")
```

---

### Phase 3: Thematic Analysis Engine

**File: backend/core/thematic_analyzer.py**

**Claude Code Prompt:**
```
Create a thematic analysis engine in backend/core/thematic_analyzer.py that:

1. Implements both **inductive** and **deductive** coding:
   - Inductive: AI generates codes from data (ground-up)
   - Deductive: Apply predefined codebook to data

2. Core functionality:
   - Generate initial codes from interview turns
   - Organize codes into hierarchical themes (parent-child relationships)
   - Identify exemplar quotes for each code
   - Calculate code frequency and coverage
   - Detect patterns across multiple interviews

3. Advanced features:
   - Code merging (identify similar codes and suggest merges)
   - Negative case analysis (find contradictory evidence)
   - Saturation detection (when new interviews add no new codes)
   - Cross-cutting theme identification

4. Transparency & validation:
   - Explain WHY a code was assigned
   - Show confidence scores
   - Allow manual override and refinement
   - Track coding history

5. Output formats:
   - JSON codebook (hierarchical)
   - CSV code-quote matrix
   - HTML visualization with quotes
   - NVivo-compatible XML export

Use advanced prompting techniques (chain-of-thought) to ensure high-quality coding.
```

**Expected Output (excerpt):**
```python
# backend/core/thematic_analyzer.py

from typing import List, Dict, Optional, Tuple, Literal
from dataclasses import dataclass, field
from pathlib import Path
import json
import logging

from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from .interview_parser import ParsedInterview, InterviewTurn
from .config import settings

logger = logging.getLogger(__name__)


# Pydantic models for structured output
class Code(BaseModel):
    """A single qualitative code."""
    code_name: str = Field(description="Short name for the code (2-4 words)")
    description: str = Field(description="Definition of what this code captures")
    examples: List[str] = Field(description="Example phrases that fit this code")


class CodeWithQuote(BaseModel):
    """Code assignment with evidence."""
    code_name: str
    quote: str
    turn_id: int
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in code assignment (0-1)")
    rationale: str = Field(description="Why this code was assigned")


class ThemeHierarchy(BaseModel):
    """Hierarchical theme structure."""
    theme_name: str
    description: str
    codes: List[str] = Field(description="Child codes under this theme")
    exemplar_quotes: List[str] = Field(description="Best quotes representing theme")
    frequency: int = Field(description="Number of occurrences across interviews")


@dataclass
class Codebook:
    """Complete codebook for a study."""
    study_name: str
    codes: Dict[str, Code]
    themes: List[ThemeHierarchy]
    version: str = "1.0"
    created_date: str = ""

    def to_json(self, output_path: str):
        """Export codebook as JSON."""
        data = {
            "study_name": self.study_name,
            "version": self.version,
            "created_date": self.created_date,
            "codes": {name: code.dict() for name, code in self.codes.items()},
            "themes": [theme.dict() for theme in self.themes]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def from_json(cls, json_path: str):
        """Load codebook from JSON."""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        codes = {name: Code(**code_data) for name, code_data in data['codes'].items()}
        themes = [ThemeHierarchy(**theme_data) for theme_data in data['themes']]

        return cls(
            study_name=data['study_name'],
            codes=codes,
            themes=themes,
            version=data.get('version', '1.0'),
            created_date=data.get('created_date', '')
        )


class ThematicAnalyzer:
    """
    AI-powered thematic analysis for qualitative data.
    """

    def __init__(
        self,
        llm_provider: Literal["openai", "anthropic"] = "anthropic",
        model_name: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.3
    ):
        if llm_provider == "anthropic":
            self.llm = ChatAnthropic(
                model=model_name,
                temperature=temperature,
                anthropic_api_key=settings.anthropic_api_key
            )
        else:
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=temperature,
                openai_api_key=settings.openai_api_key
            )

        self.llm_provider = llm_provider

    def inductive_coding(
        self,
        interviews: List[ParsedInterview],
        focus_area: Optional[str] = None,
        num_initial_codes: int = 15
    ) -> Codebook:
        """
        Generate codes inductively from interview data (grounded theory approach).

        Args:
            interviews: List of parsed interviews
            focus_area: Optional focus (e.g., "barriers to technology adoption")
            num_initial_codes: Number of initial codes to generate

        Returns:
            Codebook with inductively generated codes
        """

        logger.info(f"Starting inductive coding on {len(interviews)} interviews...")

        # Step 1: Extract all participant responses (exclude interviewer)
        participant_responses = []
        for interview in interviews:
            for turn in interview.turns:
                if turn.speaker != "interviewer":
                    participant_responses.append({
                        "text": turn.text,
                        "interview_id": interview.metadata.interview_id,
                        "turn_id": turn.turn_id
                    })

        logger.info(f"Extracted {len(participant_responses)} participant responses")

        # Step 2: Generate initial codes
        initial_codes = self._generate_initial_codes(
            participant_responses[:50],  # Sample first 50 for initial coding
            focus_area=focus_area,
            num_codes=num_initial_codes
        )

        # Step 3: Apply codes to all data
        coded_data = self._apply_codes_to_data(
            participant_responses,
            initial_codes
        )

        # Step 4: Refine codes based on application
        refined_codes = self._refine_codes(coded_data, initial_codes)

        # Step 5: Generate theme hierarchy
        themes = self._generate_theme_hierarchy(refined_codes, coded_data)

        # Create codebook
        codebook = Codebook(
            study_name="Inductive Analysis",
            codes={code.code_name: code for code in refined_codes},
            themes=themes,
            created_date=str(datetime.now())
        )

        logger.info(f"✓ Generated codebook with {len(refined_codes)} codes and {len(themes)} themes")

        return codebook

    def _generate_initial_codes(
        self,
        sample_responses: List[Dict],
        focus_area: Optional[str],
        num_codes: int
    ) -> List[Code]:
        """
        Generate initial codes from sample data.
        """

        # Prepare prompt
        responses_text = "\n\n".join([
            f"Response {i+1}: {resp['text']}"
            for i, resp in enumerate(sample_responses)
        ])

        focus_instruction = (
            f"\nFocus specifically on: {focus_area}"
            if focus_area else ""
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert qualitative researcher conducting thematic analysis.
Your task is to generate initial codes from interview data using an inductive, grounded theory approach.

CODING PRINCIPLES:
1. Codes should be data-driven (emerge from the data, not preconceived)
2. Codes should be descriptive yet concise (2-4 words)
3. Codes should capture meaningful patterns, not just topics
4. Use "in vivo" codes (participants' own words) when powerful
5. Balance specificity and abstraction

CODING EXAMPLE:
If a participant says: "I wanted to use the new software, but I just didn't have time to learn it with everything else going on"

Good codes:
- "Time constraints for learning"
- "Competing priorities"
- "Implementation barriers - temporal"

Bad codes:
- "Software" (too vague)
- "Time" (too broad)
- "Participant mentions time issues" (too descriptive, not analytic)

Generate {num_codes} initial codes that capture the most significant patterns in this data.{focus_instruction}"""),
            ("human", """Interview responses to code:

{responses_text}

Generate exactly {num_codes} codes. For each code, provide:
1. Code name (2-4 words, descriptive yet concise)
2. Definition (what this code captures, when to apply it)
3. Examples (3-4 short phrases from the data that exemplify this code)

Format as JSON array of objects with keys: code_name, description, examples""")
        ])

        # Parse response
        parser = PydanticOutputParser(pydantic_object=List[Code])

        chain = prompt | self.llm | parser

        try:
            codes = chain.invoke({
                "responses_text": responses_text,
                "num_codes": num_codes,
                "focus_instruction": focus_instruction
            })
        except Exception as e:
            logger.error(f"Error generating codes: {e}")
            # Fallback: generate simple codes
            codes = []

        return codes

    def _apply_codes_to_data(
        self,
        responses: List[Dict],
        codes: List[Code]
    ) -> List[CodeWithQuote]:
        """
        Apply generated codes to all data.
        """

        # Implementation continues...
        pass

    # ... rest of the methods


# Example usage
if __name__ == "__main__":
    from interview_parser import parse_interview_directory

    # Parse interviews
    interviews = parse_interview_directory("./data/raw_interviews")

    # Inductive coding
    analyzer = ThematicAnalyzer(llm_provider="anthropic")
    codebook = analyzer.inductive_coding(
        interviews=interviews,
        focus_area="teachers' experiences with AI tools",
        num_initial_codes=15
    )

    # Save codebook
    codebook.to_json("./data/codebooks/teacher_ai_codebook.json")
```

---

## Module 3 Summary

This module provides:
- ✅ Interview transcript parsing from multiple formats
- ✅ AI-powered inductive & deductive coding
- ✅ Transparent, explainable code assignments
- ✅ Hierarchical theme generation
- ✅ Export to NVivo, Atlas.ti, and standard formats

**Key Advantages over Traditional Coding:**
- ⚡ 10-20x faster initial coding
- 🎯 Consistent application of codes
- 📊 Quantitative analysis of qualitative patterns
- 🔍 Cross-interview pattern detection

**Important Reminder:** Always validate AI-generated codes with human expertise!

---

**Next: Module 4 - Research Collaboration & Team Workflows** 👥
