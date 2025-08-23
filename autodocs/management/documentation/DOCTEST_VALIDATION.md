# RP Documentation Validation System (DOCTESTS)

**Novel Approach**: Test documentation quality by having weak LLMs attempt to use functions based solely on docstrings

## The Problem

Traditional documentation testing:
- **Doctests**: Only test examples that already exist
- **Manual review**: Subjective and inconsistent  
- **Integration tests**: Test functionality, not documentation clarity
- **User feedback**: Comes too late after poor docs are released

**None of these test whether documentation actually teaches users how to use functions correctly.**

## The RP Solution: LLM Documentation Validation

### Core Concept
1. **Give a weak LLM** (Claude Haiku) ONLY the function docstring
2. **Present increasingly complex use cases** 
3. **Ask it to write runnable code** using that function
4. **Execute the code** - if it runs correctly, the docs work!
5. **If it fails** - the documentation is insufficient/incorrect

### Why This Works

#### Weak LLMs as Documentation Validators
- **Limited reasoning** - can't "figure out" missing information
- **Literal interpretation** - follow documentation exactly
- **No external knowledge** - rely solely on provided docstring
- **Perfect proxy** for confused users

#### Progressive Complexity Testing
```python
# Level 1: Basic usage (should always work)
"Use load_image to load a single image file"

# Level 2: Common parameters (tests parameter docs)  
"Use load_image with caching enabled and error handling"

# Level 3: Edge cases (tests comprehensive coverage)
"Use load_image with a non-existent file and strict=False"

# Level 4: Integration (tests related function mentions)
"Load an image, resize it, and save the result"
```

## Implementation Architecture

### 1. Doctest Generator (`doctest_generator.py`)

```python
class DocTestGenerator:
    def generate_test_cases(self, function_name: str) -> List[TestCase]:
        """Generate progressive complexity test cases for a function"""
        
        # Analyze function signature and docstring
        # Generate appropriate complexity levels
        # Return structured test cases
```

**Test Case Categories**:
- **Basic usage**: Simple function call
- **Parameter variants**: Different parameter combinations  
- **Error handling**: Edge cases and error conditions
- **Integration**: Using with related functions
- **Performance**: Batch operations, large inputs

### 2. LLM Doctest Runner (`llm_doctest_runner.py`)

```python
class LLMDoctestRunner:
    def __init__(self, model="claude-haiku"):
        self.model = model
    
    def test_documentation(self, function_name: str, docstring: str, 
                          test_cases: List[TestCase]) -> DocTestResults:
        """Test documentation using LLM + execution"""
        
        for test_case in test_cases:
            # Give LLM only the docstring
            # Ask it to write code for the test case
            # Execute the generated code
            # Record success/failure with error details
```

**Execution Safety**:
- **Sandboxed execution** - isolated environment
- **Timeout protection** - prevent infinite loops
- **Resource limits** - memory and CPU constraints
- **Import restrictions** - only allow RP functions

### 3. Documentation Feedback Loop (`doc_improver.py`)

```python
class DocumentationImprover:
    def analyze_failures(self, results: DocTestResults) -> ImprovementSuggestions:
        """Analyze why LLM failed to understand documentation"""
        
        # Common failure patterns:
        # - Missing parameter explanations
        # - Unclear return value descriptions  
        # - No examples for complex usage
        # - Missing error condition documentation
```

**Failure Analysis**:
- **Parameter confusion** → Add clearer parameter descriptions
- **Return value errors** → Better return type documentation  
- **Import failures** → Missing usage examples
- **Type errors** → Clearer type information
- **Logic errors** → Missing behavioral explanations

## Integration with Minion Workflow

### Enhanced Work Package Process

#### Before Documentation (Current):
1. Minion receives function cluster with context
2. Minion enhances docstrings
3. Human reviews documentation
4. **DONE** ✅

#### After Documentation (New):
1. Minion receives function cluster with context
2. Minion enhances docstrings  
3. **LLM doctest validation** automatically runs
4. **If tests fail**: Minion gets specific feedback to fix
5. **If tests pass**: Documentation approved
6. Human spot-checks high-priority functions only
7. **DONE** ✅

### Minion Instructions Update

```markdown
## Enhanced Documentation Process

### Step 5: Validate Documentation (NEW)
After enhancing docstrings, your documentation will be automatically tested:

1. **LLM Validation**: A weak LLM will attempt to use your documented functions
2. **Progressive Testing**: From basic usage to complex edge cases  
3. **Execution Verification**: Generated code must actually run correctly

### Common Validation Failures & Fixes:

**"LLM couldn't figure out parameter types"**
→ Add explicit type information: `path (str): File path to image`

**"LLM used function incorrectly"** 
→ Add concrete usage example: `>>> load_image('photo.jpg')`

**"LLM missed error handling"**
→ Document error conditions: `Raises FileNotFoundError if path doesn't exist`

**"LLM couldn't use with other functions"**
→ Add integration examples: `Often used with resize_image() and save_image()`
```

## Test Case Templates

### Template 1: Basic Function Usage
```python
def generate_basic_test(func_name: str) -> str:
    return f"""
Task: Use the {func_name} function for its most common purpose.
Context: You are a new RP user who has never used this function before.
Requirements: Write working Python code using ONLY the information in the docstring.
    """
```

### Template 2: Parameter Exploration  
```python
def generate_parameter_test(func_name: str, param_name: str) -> str:
    return f"""
Task: Use {func_name} with the {param_name} parameter in a meaningful way.
Context: You need to understand what this parameter does and use it correctly.
Requirements: Write code that demonstrates the parameter's effect.
    """
```

### Template 3: Error Handling
```python
def generate_error_test(func_name: str) -> str:
    return f"""
Task: Use {func_name} in a way that might cause an error, but handle it properly.
Context: You're writing defensive code and need to handle potential failures.
Requirements: Show proper error handling based on docstring information.
    """
```

### Template 4: Integration Testing
```python
def generate_integration_test(func_name: str, related_funcs: List[str]) -> str:
    return f"""
Task: Use {func_name} as part of a workflow with {', '.join(related_funcs)}.
Context: You're building a pipeline that processes data through multiple steps.
Requirements: Chain these functions together logically.
    """
```

## Quality Metrics

### Documentation Quality Score
```python
def calculate_doc_quality(results: DocTestResults) -> float:
    """
    Returns 0.0-1.0 based on LLM success rate across complexity levels
    
    Weights:
    - Basic usage: 40% (must work)
    - Parameters: 30% (important for usability)  
    - Error handling: 20% (prevents user frustration)
    - Integration: 10% (nice-to-have)
    """
```

### Success Criteria
- **Excellent docs (0.9-1.0)**: LLM succeeds at all complexity levels
- **Good docs (0.7-0.9)**: LLM succeeds at basic + most parameter cases
- **Adequate docs (0.5-0.7)**: LLM succeeds at basic usage reliably
- **Poor docs (0.0-0.5)**: LLM fails even basic usage

## Implementation Timeline

### Phase 1: Infrastructure (Week 1)
- [ ] Build doctest generator with test case templates
- [ ] Create sandboxed LLM execution environment
- [ ] Integrate with existing work package system

### Phase 2: Validation Pipeline (Week 2)  
- [ ] Test on sample of well-documented functions
- [ ] Refine test case generation based on results
- [ ] Add failure analysis and improvement suggestions

### Phase 3: Minion Integration (Week 3)
- [ ] Update minion work package instructions
- [ ] Add automatic validation to documentation workflow
- [ ] Create feedback loop for iterative improvement

### Phase 4: Full Deployment (Week 4)
- [ ] Run validation on all existing documentation
- [ ] Generate improvement priorities based on validation scores
- [ ] Establish quality gates for new documentation

## Expected Benefits

### For RP Users
- **Actually usable documentation** - tested by proxy users (LLMs)
- **Fewer support questions** - docs that actually explain how to use functions
- **Better examples** - validated to work in real scenarios

### for Documentation Process  
- **Objective quality measurement** - no more subjective "looks good"
- **Automatic feedback** - specific suggestions for improvement
- **Scalable validation** - can test all 2001 functions systematically

### For RP Development
- **Higher confidence** in documentation quality
- **Reduced maintenance** - fewer docs that need fixing later  
- **Better API design** - hard-to-document APIs get redesigned

## Technical Considerations

### LLM Selection
- **Primary**: Claude Haiku (fast, cheap, appropriately limited)
- **Backup**: GPT-3.5-turbo (if Claude unavailable)
- **Never use**: GPT-4, Claude Opus (too smart - would pass bad docs)

### Execution Environment
- **Docker container** with minimal RP installation
- **Resource limits**: 1 CPU, 512MB RAM, 30s timeout
- **Network isolated** - no external dependencies
- **File system**: Read-only except temp directory

### Cost Optimization
- **Batch requests** - test multiple functions per LLM call
- **Cache results** - don't re-test unchanged documentation  
- **Smart sampling** - test representative cases, not exhaustive

---

**This novel approach ensures RP documentation actually works for users, not just developers who already understand the functions.**