# AI-PRISMA Prompt Optimization Strategy

## Current Performance Issue

- **Current Speed**: 360 papers/hour (6 papers/minute)
- **Total Papers**: 4,365
- **Estimated Time**: ~12 hours
- **Model**: Claude Haiku 4.5 (should be VERY fast)
- **Problem**: Unexpectedly slow for Haiku model

## Current Prompt Analysis

### Prompt Length
- **Estimated tokens**: ~1,500-2,000 tokens
- **Structure**: Very detailed 6-dimension rubric with extensive examples
- **Components**:
  1. Research question + title + abstract
  2. Detailed PICOC+S framework explanation
  3. 6 scoring dimensions with examples
  4. Evidence grounding requirements
  5. JSON format specification
  6. Academic citations and lineage

### Verbose Elements
1. **Academic Citations** (13 citations): Booth et al., 2012; Richardson et al., 1995; Higgins et al., 2022; Page et al., 2021; O'Mara-Eves et al., 2015
2. **Detailed Examples**: For each dimension, multiple examples with research question substitution
3. **Extensive Guidelines**: Point-by-point scoring for each dimension
4. **Repetitive Instructions**: Evidence grounding repeated multiple times
5. **Formatting Instructions**: JSON structure explained in detail

## Optimization Strategies

### Strategy 1: Minimal Prompt (Aggressive)
**Approach**: Strip to absolute minimum
**Estimated Token Reduction**: 70% (300-600 tokens)
**Risk**: Lower scoring accuracy

```
Research Question: {question}
Title: {title}
Abstract: {abstract}

Score relevance (0-50):
- Domain match (0-10)
- Intervention match (0-10)
- Method rigor (0-5)
- Outcomes clarity (0-10)
- Exclusions (-20 to 0)
- Title bonus (0 or 10)

Return JSON: {scores, total_score, decision, reasoning, evidence_quotes}
Decision: ≥40 include, <0 exclude, else review
```

### Strategy 2: Moderate Simplification (Balanced)
**Approach**: Keep core rubric, remove examples and citations
**Estimated Token Reduction**: 40% (900-1,200 tokens)
**Risk**: Medium - maintains structure

```
Research Question: {question}
Title: {title}
Abstract: {abstract}

SCORING RUBRIC:
1. Domain (0-10): Target population/context relevance
2. Intervention (0-10): Specific technology/tool focus
3. Method (0-5): Study design rigor (RCT=5, qualitative=2, theory=0)
4. Outcomes (0-10): Measured results clarity
5. Exclusion (-20 to 0): Penalties for reviews (-10), wrong domain (-20)
6. Title Bonus (0 or 10): Both domain+intervention in title

JSON: {scores, total_score, decision, reasoning, evidence_quotes}
Rules: ≥40 auto-include, <0 auto-exclude, else human-review
Evidence: Direct quotes from abstract only (no labels)
```

### Strategy 3: Template Caching (Technical)
**Approach**: Use Anthropic's prompt caching to cache the static rubric
**Estimated Cost Reduction**: 90% for cached portions
**Speed**: May improve with cache hits
**Implementation**: Requires Anthropic API parameter changes

### Strategy 4: Batch Processing (Architectural)
**Approach**: Score multiple papers in single API call
**Estimated Speed**: 3-5x faster
**Risk**: Higher - more complex parsing
**Example**: Process 5 papers per call instead of 1

## Recommendations for Codex Discussion

### Questions for Codex:
1. **Speed vs Accuracy Tradeoff**: What's the optimal balance for systematic reviews?
2. **Prompt Caching**: Is this supported in current Anthropic SDK version?
3. **Batch Processing**: Feasible with current JSON parsing logic?
4. **Token Estimation**: What's the actual token count of current prompt?
5. **Alternative Approaches**:
   - Pre-filter with simple keyword matching?
   - Two-stage screening (fast filter + detailed review)?
   - Use Haiku for filtering, Sonnet for detailed scoring?

### Test Plan:
1. Create 3 prompt versions (minimal, moderate, current)
2. Test on same 50 papers
3. Compare:
   - Speed (papers/minute)
   - Accuracy (match with human judgment)
   - Consistency (same papers get same scores)
4. Select optimal version

## Implementation Priority

**Recommended Approach**: Strategy 2 (Moderate Simplification)
- Best balance of speed/accuracy
- Low implementation risk
- Maintains academic rigor
- Should achieve 2-3x speedup (6-7 hours total)

**If that's insufficient**: Strategy 4 (Batch Processing)
- Requires more code changes
- Higher risk but 3-5x faster
- Could finish in 2-3 hours
