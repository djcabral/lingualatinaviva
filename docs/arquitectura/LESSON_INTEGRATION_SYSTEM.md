# Lesson-Based Content Integration System
## Comprehensive Documentation

---

## Overview

This document describes the **Lesson-Based Content Integration System** implemented to ensure that students practice vocabulary and grammar relevant to their current learning stage.

### Problem Statement
Previously, the "Memorization" and "Analysis" modules presented random content from the entire database (~9,000 words), which was overwhelming and often irrelevant to the student's current lesson.

### Solution
We implemented a three-tier system:
1. **Smart Content Population**: Automatic assignment of words to lessons based on grammatical properties
2. **Context-Aware Selection**: Vocabulary and analysis exercises adapt to the user's current lesson
3. **Progressive Constraints**: Grammar analysis only presents forms that the student has learned

---

## System Architecture

### Database Schema
```
LessonVocabulary (Junction Table)
├── lesson_number: int (1-40)
├── word_id: int (FK → Word)
├── is_essential: bool
├── is_secondary: bool
└── presentation_order: int

UserVocabularyProgress (SRS Tracking)
├── user_id: int
├── word_id: int (FK → Word)
├── times_seen: int
├── times_correct: int
├── times_incorrect: int
├── mastery_level: float (0.0-1.0)
├── next_review_date: datetime
├── ease_factor: float (SM-2 algorithm)
└── interval_days: int

UserProgressSummary (Denormalized Cache)
├── user_id: int
├── current_lesson: int
├── lessons_completed: JSON array [1, 2, 3]
└── lessons_in_progress: JSON array [4]
```

---

## Component 1: Smart Content Population

### Script: `scripts/populate_lesson_content.py`

**Purpose**: Automatically assign 9,000+ words to appropriate lessons based on grammatical properties.

**Assignment Logic**:

| Lesson | Grammar Focus | Assignment Rules |
|--------|---------------|------------------|
| L1 (Intro) | Basic vocabulary | Sum/Es/Est, basic nouns (puella, puer), invariables (in, et, non) |
| L2 (Subject) | Nominative case | All 1st/2nd decl. nouns (level 1) |
| L3 (1st Decl) | Feminine -a nouns | declension="1", 1st conjugation verbs (amo) |
| L4 (2nd Decl) | Masculine -us, Neuter -um | declension="2", 2nd conjugation verbs |
| L5 (Neuter) | All neuter nouns | gender="n" |
| L6 (Consolidation) | Adjectives | part_of_speech="adjective" (1st/2nd class) |
| L7 (3rd Decl) | 3rd declension | declension="3", 3rd conjugation verbs |
| L8 (4th Decl) | 4th declension | declension="4", 4th conjugation verbs |
| L9 (5th Decl) | 5th declension | declension="5" |
| L12 (Pronouns) | Pronouns | part_of_speech="pron" or "pronoun" |

**Results** (from latest run):
```
✓ Population complete!
  - Added: 11,505 entries
  - Lesson 1: 1,267 words (basic vocab)
  - Lesson 2: 2,191 words (nominative practice)
  - Lesson 3: 1,690 words (1st declension)
  - Lesson 4: 1,579 words (2nd declension)
  - Lesson 7: 2,337 words (3rd declension)
```

**Idempotency**: The script checks for existing entries before adding, so it's safe to run multiple times.

---

## Component 2: Vocabulary Module (Memorization)

### File: `src/views/vocabulary.py`

**Old Logic**:
- Random selection from ALL words in database
- No consideration of user progress
- No SRS (Spaced Repetition System) integration

**New Logic**:

#### 1. Context Awareness
```python
def get_user_context():
    # Fetches UserProgressSummary
    return {
        "current_lesson": 3,  # example
        "completed_lessons": [1, 2]
    }
```

#### 2. Selection Pool
Two sources:
- **New Words**: From `LessonVocabulary` for current lesson, not yet seen
- **Review Words**: From completed lessons, due for SRS review

```python
def get_new_words(session, current_lesson: int):
    # Query LessonVocabulary for current lesson
    # Filter out words already in UserVocabularyProgress
    # Return up to 10 new words

def get_review_words(session, completed_lessons: list):
    # Query LessonVocabulary for completed lessons
    # Filter words where next_review_date <= now
    # Return up to 20 due words
```

#### 3. Prioritization Strategy
```python
def select_next_card():
    new_words = get_new_words(...)
    review_words = get_review_words(...)
    
    if new_words and review_words:
        # 40% probability: new word
        # 60% probability: review word
        return weighted_choice(new_words, review_words)
    elif new_words:
        return random.choice(new_words)
    elif review_words:
        return random.choice(review_words)
    else:
        # Fallback: any word from lessons 1-current
```

#### 4. SRS Integration
After each review:
```python
def process_review(word_id, quality):
    # Update UserVocabularyProgress
    progress.times_seen += 1
    progress.times_correct += (1 if quality >= 3 else 0)
    
    # Calculate mastery
    progress.mastery_level = correct / (correct + incorrect)
    
    # SM-2 Algorithm
    srs_data = calculate_next_review(quality, previous_review)
    progress.interval_days = srs_data["interval"]
    progress.next_review_date = now + interval_days
```

**Benefits**:
- Students see words they're currently learning
- SRS ensures optimal review timing
- Prevents overwhelming beginners with advanced vocabulary

---

## Component 3: Analysis Module (Grammar Practice)

### File: `src/views/analysis.py`

**Old Logic**:
- Random word, random form
- Could ask for Subjunctive Pluperfect when student is on Lesson 1

**New Logic**:

#### 1. Progressive Grammar Constraints
```python
GRAMMAR_CONSTRAINTS = {
    1: {
        "noun_cases": ["nominative"],
        "noun_numbers": ["singular"],
        "verb_tenses": ["present"],
        "verb_moods": ["indicative"],
        "verb_voices": ["active"]
    },
    3: {
        "noun_cases": ["nominative", "accusative", "ablative"],
        "noun_numbers": ["singular", "plural"],
        ...
    },
    13: {
        # All cases
        "verb_voices": ["active", "passive"]  # Passive unlocked
    },
    18: {
        "verb_moods": ["indicative", "subjunctive"]  # Subjunctive unlocked
    }
}
```

#### 2. Context-Aware Word Selection
```python
def select_word_for_analysis(session, current_lesson: int):
    # Get words from lessons (current - 2) to current
    # Prioritize essential words
    # Ensures relevance to recent material
```

#### 3. Form Generation
```python
def generate_noun_form(word, constraints):
    all_forms = LatinMorphology.decline_noun(word)
    
    # Filter by constraints
    valid_forms = {
        key: value for key, value in all_forms.items()
        if case in constraints["noun_cases"] and
           number in constraints["noun_numbers"]
    }
    
    return random.choice(valid_forms)
```

**Example Progression**:
- **Lesson 1**: "puella" → nominative singular only
- **Lesson 3**: "rosa" → nominative/accusative/ablative (sing/pl)
- **Lesson 7**: "rex" → all 6 cases (3rd declension)
- **Lesson 13**: "amor" → passive forms introduced

---

## Usage Guide

### For Developers

#### 1. Running the Population Script
```bash
# First time (populate database)
.venv/bin/python scripts/populate_lesson_content.py

# Re-populate (clear + repopulate)
.venv/bin/python scripts/populate_lesson_content.py --clear
```

#### 2. Adding New Words
1. Add word to `Word` table via seed data or admin panel
2. Run population script (it will auto-assign to appropriate lessons)
3. No manual intervention needed

#### 3. Customizing Lesson Assignments
Edit `scripts/populate_lesson_content.py`:
```python
def get_lesson_assignment(word: Word) -> list[int]:
    assignments = []
    
    # Add custom logic here
    if word.latin == "carpe":
        assignments.append(36)  # Horace lesson
    
    return assignments
```

### For Students (User Experience)

#### Memorization Flow
1. **Start**: User is on Lesson 3
2. **Opens Memorization**: Sees "📘 Practicando desde la Lección 3"
3. **Card 1**: "rosa" (new word from L3)
4. **Card 2**: "puella" (review from L1, due today)
5. **Card 3**: "dominus" (new word from L2, backfill)

#### Analysis Flow
1. **Start**: User is on Lesson 3
2. **Opens Analysis**: Sees "📘 Analizando gramática hasta la Lección 3"
3. **Exercise 1**: "rosam" → Identify accusative singular (allowed for L3)
4. **Exercise 2**: "puellae" → Identify genitive singular (allowed for L3)
5. **Not shown**: "rēgī" (dative, 3rd decl → requires L7)

---

## Testing

### Manual Testing Checklist

**Test Scenario 1: Lesson 1 (Beginner)**
- [ ] Memorization shows only basic words (sum, puella, puer)
- [ ] Analysis shows only nominative singular
- [ ] No 3rd declension or passive forms

**Test Scenario 2: Lesson 3 (1st Decl)**
- [ ] Memorization includes 1st declension feminine nouns
- [ ] Analysis includes accusative and ablative
- [ ] Still no passive voice

**Test Scenario 3: Lesson 13 (Passive)**
- [ ] Memorization includes advanced vocab
- [ ] Analysis includes passive forms (amor, amatur)
- [ ] All cases available

### Verification Commands
```bash
# Check population results
.venv/bin/python -c "from database import get_session, LessonVocabulary; from sqlmodel import select; session = next(get_session()); print(f'L1: {len(session.exec(select(LessonVocabulary).where(LessonVocabulary.lesson_number == 1)).all())} words')"

# Check user's current lesson
.venv/bin/python -c "from database import get_session, UserProgressSummary; from sqlmodel import select; session = next(get_session()); summary = session.exec(select(UserProgressSummary)).first(); print(f'Current Lesson: {summary.current_lesson if summary else 1}')"
```

---

## Performance Considerations

### Database Queries
- **Vocabulary Selection**: 3 queries (user context + new words + review words)
- **Analysis Selection**: 2 queries (user context + word selection)
- **All queries indexed** on `lesson_number`, `word_id`, `user_id`

### Caching Opportunities
- `UserProgressSummary` is denormalized for fast access
- Consider caching `GRAMMAR_CONSTRAINTS` in app memory (already done)

### Scalability
- Current: 11,505 LessonVocabulary entries for ~9,000 words
- Scales linearly with vocabulary size
- No N+1 queries (uses batch queries + filters)

---

## Future Enhancements

### Planned Features
1. **Adaptive Difficulty**: Adjust word frequency based on user performance
2. **Weak Area Detection**: Track error patterns and recommend targeted practice
3. **Challenge Integration**: Link vocabulary to specific challenges
4. **Author-Specific Vocabulary**: Practice Caesar's vocabulary when reading Caesar

### Migration Path (Lessons 31-40)
These lessons currently have 0 entries in `LessonVocabulary`. Plan:
1. Define author-specific vocabulary for expert lessons
2. Assign literary vocabulary (e.g., "bellum" → Caesar lesson)
3. Add stylistic practice (e.g., "carpe" → Horace lesson)

---

## Maintenance

### Regular Tasks
1. **Monthly**: Review population script accuracy
2. **After major vocab additions**: Re-run population script
3. **Monitor**: User feedback on vocabulary relevance

### Troubleshooting

**Issue**: User sees too many new words
- **Solution**: Adjust prioritization ratio in `select_next_card()` (currently 40% new, 60% review)

**Issue**: Not enough review words
- **Solution**: Lower SRS interval multiplier in `calculate_next_review()`

**Issue**: Advanced grammar appears too early
- **Solution**: Adjust `GRAMMAR_CONSTRAINTS` in `analysis.py`

---

## Conclusion

This system provides a **progressive, context-aware learning experience** that adapts to each student's current capabilities. By tightly integrating vocabulary and grammar practice with lesson progression, we ensure that students:
- Never feel overwhelmed by irrelevant content
- Practice what they've just learned
- Review at optimal intervals
- Build mastery progressively

**Total Implementation**:
- **1 population script** (165 lines)
- **2 refactored modules** (vocabulary: 280 lines, analysis: 243 lines)
- **11,505 intelligent word-lesson assignments**
- **0 manual data entry required**

---

*Document created: 2025-11-29*
*Author: Antigravity AI Assistant*
