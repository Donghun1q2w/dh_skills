# Financial Model Rules

## Color Coding Standards

Unless otherwise stated by the user or existing template.

### Industry-Standard Color Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

---

## Number Formatting Standards

### Required Format Rules
- **Years**: Format as text strings (e.g., "2024" not "2,024")
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers ("Revenue ($mm)")
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-")
- **Percentages**: Default to 0.0% format (one decimal)
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E)
- **Negative numbers**: Use parentheses (123) not minus -123

---

## Formula Construction Rules

### Assumptions Placement
- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells
- Use cell references instead of hardcoded values in formulas
- Example: Use =B5*(1+$B$6) instead of =B5*1.05

### Formula Error Prevention
- Verify all cell references are correct
- Check for off-by-one errors in ranges
- Ensure consistent formulas across all projection periods
- Test with edge cases (zero values, negative numbers)
- Verify no unintended circular references

### Documentation Requirements for Hardcodes
- Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]"
- Examples:
  - "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  - "Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]"
  - "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"
  - "Source: FactSet, 8/20/2025, Consensus Estimates Screen"

---

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
