# Application Review: lingua-latina-viva

## Overview
The `lingua-latina-viva` application is a React-based educational tool designed to teach Latin. The app uses a component-based architecture, with modular components handling different functionalities such as dashboard, lessons, syntactic analysis, and spaced repetition systems (SRS).

## Key Components

### 1. Dashboard
- **File Path:** [Dashboard.tsx](file:///home/diego/Projects/latin-python/recycle_bin/lingua-latina-viva/components/Dashboard.tsx#L9-L171)
- **Purpose:** Displays user progress and recommendations.
- **Key Features:**
  - Progress tracking using `useState`
  - Recommendations display

```typescript
const [progress, setProgress] = useState<UserProgress | null>(null);
const [recs, setRecs] = useState<Recommendation[]>([]);
```

### 2. LessonView
- **File Path:** [LessonView.tsx](file:///home/diego/Projects/latin-python/recycle_bin/lingua-latina-viva/components/LessonView.tsx#L10-L141)
- **Purpose:** Shows lesson content with Markdown-like formatting.
- **Key Features:**
  - Lesson completion handling

```typescript
const lesson = LESSONS.find(l => l.id === lessonId);
const handleFinish = () => {
  completeLesson(lessonId);
  onComplete();
};
```

### 3. Analyzer
- **File Path:** [Analyzer.tsx](file:///home/diego/Projects/latin-python/recycle_bin/lingua-latina-viva/components/Analyzer.tsx)
- **Purpose:** Provides a syntactic analysis lab for Latin texts.
- **Key Features:**
  - Asynchronous text analysis

```typescript
const handleAnalyze = async () => {
  if (!input.trim()) return;
  setLoading(true);
  setError('');
  setAnalysis(null);
  setSelectedWordId(null);
  try {
    const result = await analyzeLatinText(input);
    setAnalysis(result);
  } catch (e) {
    setError("Error analyzing text.");
  } finally {
    setLoading(false);
  }
};
```

### 4. SRS (Spaced Repetition System)
- **File Path:** [SRS.tsx](file:///home/diego/Projects/latin-python/recycle_bin/lingua-latina-viva/components/SRS.tsx)
- **Purpose:** Implements a spaced repetition system (SRS) for vocabulary.
- **Key Features:**
  - Vocabulary mastery updates

```typescript
const handleNext = (rating: 'hard' | 'good' | 'easy') => {
  const success = rating === 'good' || rating === 'easy';
  updateVocabMastery(currentCard.id, success);
  setIsFlipped(false);
  setTimeout(() => {
    if (currentCardIndex < deck.length - 1) {
      setCurrentCardIndex(prev => prev + 1);
    } else {
      setSessionComplete(true);
    }
  }, 200);
};
```

## README
- **File Path:** [README.md](file:///home/diego/Projects/latin-python/README.md)
- **Content:** Describes project structure, features, and setup instructions.

---

This document serves as a comprehensive review of the `lingua-latina-viva` application, highlighting its organization and key technical concepts that could be adapted to your Streamlit project.