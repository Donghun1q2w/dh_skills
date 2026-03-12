---
name: excel
description: "Windows/macOS 크로스플랫폼 Excel 스킬. UTF-8 인코딩 우선 적용, cp949/euc-kr 자동 fallback으로 한글 데이터 처리에 특화. .xlsx, .xlsm, .csv, .tsv 파일의 읽기, 편집, 생성, 변환 작업 시 트리거. openpyxl/pandas 기반으로 외부 의존성 없이 동작."
---

# Requirements for Outputs

## All Excel files

### Professional Font
- Use a consistent, professional font (e.g., Arial, Times New Roman) for all deliverables unless otherwise instructed by the user

### Zero Formula Errors
- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

### Preserve Existing Templates (when updating templates)
- Study and EXACTLY match existing format, style, and conventions when modifying files
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

## Financial models

### Color Coding Standards
Unless otherwise stated by the user or existing template

#### Industry-Standard Color Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

### Number Formatting Standards

#### Required Format Rules
- **Years**: Format as text strings (e.g., "2024" not "2,024")
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers ("Revenue ($mm)")
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-")
- **Percentages**: Default to 0.0% format (one decimal)
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E)
- **Negative numbers**: Use parentheses (123) not minus -123

### Formula Construction Rules

#### Assumptions Placement
- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells
- Use cell references instead of hardcoded values in formulas
- Example: Use =B5*(1+$B$6) instead of =B5*1.05

#### Formula Error Prevention
- Verify all cell references are correct
- Check for off-by-one errors in ranges
- Ensure consistent formulas across all projection periods
- Test with edge cases (zero values, negative numbers)
- Verify no unintended circular references

#### Documentation Requirements for Hardcodes
- Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]"
- Examples:
  - "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  - "Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]"
  - "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"
  - "Source: FactSet, 8/20/2025, Consensus Estimates Screen"

# XLSX creation, editing, and analysis

## Overview

A user may ask you to create, edit, or analyze the contents of an .xlsx file. You have different tools and workflows available for different tasks.

## Important Requirements

**수식 재계산**: openpyxl은 수식을 문자열로 저장하며 값을 계산하지 않는다. 사용자에게 Excel/Numbers에서 파일을 열어 재계산하도록 안내한다.

## Reading and analyzing data

### Encoding - MANDATORY

**모든 파일 읽기에서 UTF-8을 최우선 적용**한다.

**Rule 1 - Bash 실행**: 반드시 `PYTHONIOENCODING=utf-8` 접두사 사용
```bash
PYTHONIOENCODING=utf-8 python script.py
```
> macOS는 기본 UTF-8이라 필수는 아니지만, 크로스플랫폼 호환을 위해 항상 붙인다.

**Rule 2 - Bash 인라인 Python**: `-c` 대신 heredoc(`<< 'PYEOF' ... PYEOF`) 사용 (셸 이스케이프 문제 방지)
```bash
PYTHONIOENCODING=utf-8 python << 'PYEOF'
import pandas as pd
df = pd.read_excel('file.xlsx')
print(df.head())
PYEOF
```

**Rule 3 - 파일 읽기 인코딩 우선순위**: UTF-8 → cp949 → euc-kr 순서로 시도

| 파일 형식 | 인코딩 처리 |
|-----------|------------|
| `.xlsx`, `.xlsm` | XML 기반이므로 항상 UTF-8 (인코딩 파라미터 불필요) |
| `.xls` | `pd.read_excel('file.xls', engine='xlrd')` — 내부 코드페이지 자동 감지 |
| `.csv`, `.tsv` | UTF-8 우선, 실패 시 cp949 fallback (아래 코드 참조) |

```python
# CSV/TSV 읽기: UTF-8 우선 적용
def read_tabular(filepath, **kwargs):
    for enc in ['utf-8', 'utf-8-sig', 'cp949', 'euc-kr']:
        try:
            return pd.read_csv(filepath, encoding=enc, **kwargs)
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"지원되는 인코딩으로 읽을 수 없습니다: {filepath}")
```

**Rule 4 - Excel 쓰기**: openpyxl 엔진 사용 (UTF-8 네이티브 지원)
```python
df.to_excel('output.xlsx', index=False, engine='openpyxl')
```

**Rule 5 - openpyxl 직접 사용**: .xlsx는 XML 기반(항상 UTF-8)이므로 인코딩 파라미터 불필요.

### Data analysis with pandas
For data analysis, visualization, and basic operations, use **pandas** which provides powerful data manipulation capabilities:

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

## Excel File Workflows

## CRITICAL: Use Formulas, Not Hardcoded Values

**Always use Excel formulas instead of calculating values in Python and hardcoding them.** This ensures the spreadsheet remains dynamic and updateable.

### WRONG - Hardcoding Calculated Values
```python
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# Bad: Computing growth rate in Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15

# Bad: Python calculation for average
avg = sum(values) / len(values)
sheet['D20'] = avg  # Hardcodes 42.5
```

### CORRECT - Using Excel Formulas
```python
# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'

# Good: Growth rate as Excel formula
sheet['C5'] = '=(C4-C2)/C2'

# Good: Average using Excel function
sheet['D20'] = '=AVERAGE(D2:D19)'
```

This applies to ALL calculations - totals, percentages, ratios, differences, etc. The spreadsheet should be able to recalculate when source data changes.

## Common Workflow
1. **Choose tool**: pandas for data, openpyxl for formulas/formatting
2. **Create/Load**: Create new workbook or load existing file
3. **Modify**: Add/edit data, formulas, and formatting
4. **Save**: Write to file
5. **수식 재계산 (수식 사용 시 필수)**: 사용자에게 Excel/Numbers에서 열어 재계산 안내
6. **오류 검증**: openpyxl `data_only=True`로 열어 `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?` 등 확인 후 수정

### Creating new Excel files

```python
# Using openpyxl for formulas and formatting
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### Editing existing Excel files

```python
# Using openpyxl to preserve formulas and formatting
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('existing.xlsx')
sheet = wb.active  # or wb['SheetName'] for specific sheet

# Working with multiple sheets
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insert row at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## 수식 재계산

openpyxl로 생성/수정한 Excel 파일은 수식이 문자열로만 저장되고 계산값이 없다. 사용자에게 파일을 열어 재계산하도록 안내한다.

| 플랫폼 | 앱 | 재계산 단축키 |
|--------|-----|-------------|
| Windows | Excel | Ctrl+Shift+F9 |
| macOS | Excel | Cmd+Shift+F9 |
| macOS | Numbers | .xlsx 열면 자동 재계산 |

### 수식 오류 검증 (Python)
```python
from openpyxl import load_workbook

wb = load_workbook('output.xlsx', data_only=True)
errors = []
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and cell.value.startswith('#'):
                errors.append(f"{ws.title}!{cell.coordinate}: {cell.value}")
if errors:
    print("수식 오류 발견:", errors)
```

## Formula Verification Checklist

### Essential Verification
- [ ] **2-3개 참조 테스트**: 전체 모델 작성 전 올바른 값을 가져오는지 확인
- [ ] **컬럼 매핑**: Excel 컬럼 확인 (예: column 64 = BL, not BK)
- [ ] **Row offset**: Excel은 1-indexed (DataFrame row 5 = Excel row 6)

### Common Pitfalls
- [ ] **NaN 처리**: `pd.notna()`로 null 값 확인
- [ ] **Division by zero**: 수식에서 나누기 전 분모 확인 (#DIV/0!)
- [ ] **Wrong references**: 모든 셀 참조가 의도한 셀을 가리키는지 확인 (#REF!)
- [ ] **Cross-sheet references**: `Sheet1!A1` 형식 사용

## Best Practices

### Library Selection
- **pandas**: Best for data analysis, bulk operations, and simple data export
- **openpyxl**: Best for complex formatting, formulas, and Excel-specific features

### Working with openpyxl
- Cell indices are 1-based (row=1, column=1 refers to cell A1)
- Use `data_only=True` to read calculated values: `load_workbook('file.xlsx', data_only=True)`
- **Warning**: If opened with `data_only=True` and saved, formulas are replaced with values and permanently lost
- For large files: Use `read_only=True` for reading or `write_only=True` for writing
- Formulas are preserved but not evaluated - Excel/Numbers에서 직접 열어 재계산 필요

### Working with pandas
- Specify data types to avoid inference issues: `pd.read_excel('file.xlsx', dtype={'id': str})`
- For large files, read specific columns: `pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- Handle dates properly: `pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## Code Style Guidelines
**IMPORTANT**: When generating Python code for Excel operations:
- Write minimal, concise Python code without unnecessary comments
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

**For Excel files themselves**:
- Add comments to cells with complex formulas or important assumptions
- Document data sources for hardcoded values
- Include notes for key calculations and model sections
