# Hancom Equation Script Syntax (hp:equation)

Reference for Hancom Office equation script used in `<hp:script>` elements.
This is NOT LaTeX. Use Hancom-native syntax only.

## Table of Contents

- [Basic Rules](#basic-rules)
- [Fractions and Roots](#fractions-and-roots)
- [Superscripts and Subscripts](#superscripts-and-subscripts)
- [Integrals, Sums, Products](#integrals-sums-products)
- [Limits](#limits)
- [Brackets](#brackets)
- [Matrices](#matrices)
- [Systems of Equations](#systems-of-equations)
- [Decorations](#decorations)
- [Greek Letters](#greek-letters)
- [Special Symbols](#special-symbols)
- [Font Styles](#font-styles)
- [Built-in Functions](#built-in-functions)
- [Grade-Level Examples](#grade-level-examples)

## Basic Rules

| Rule | Description |
|------|-------------|
| `{ }` | Grouping (combine multiple terms) |
| `~` | Space (1em) |
| `` ` `` | 1/4 space |
| `#` | Line break (within equation) |
| `&` | Column alignment (matrices, systems) |
| `"..."` | Text mode (disable equation parsing) |

## Fractions and Roots

| Expression | Script | Example |
|------------|--------|---------|
| Fraction | `a over b` | `{x+1} over {x-1}` |
| Square root | `sqrt {x}` | `sqrt {b^2 - 4ac}` |
| n-th root | `root n of {x}` | `root 3 of {27}` |

## Superscripts and Subscripts

| Expression | Script |
|------------|--------|
| Superscript | `x^2` or `x SUP 2` |
| Subscript | `x_i` or `x SUB i` |
| Both | `x_i ^2` |

## Integrals, Sums, Products

| Expression | Script |
|------------|--------|
| Definite integral | `int _{a} ^{b} f(x) dx` |
| Double integral | `dint f(x,y) dxdy` |
| Triple integral | `tint f dxdydz` |
| Summation (sigma) | `sum _{k=1} ^{n} a_k` |
| Product (pi) | `prod _{i=1} ^{n} x_i` |

## Limits

| Expression | Script |
|------------|--------|
| Limit | `lim _{x -> 0} f(x)` |
| Uppercase | `Lim _{n -> inf}` |

## Brackets

| Expression | Script |
|------------|--------|
| Auto-sized parentheses | `left ( {a over b} right )` |
| Auto-sized square brackets | `left [ x right ]` |
| Auto-sized curly braces | `left lbrace x right rbrace` |
| Absolute value | `left | x right |` |

## Matrices

| Expression | Script |
|------------|--------|
| Basic matrix | `matrix {a & b # c & d}` |
| Parenthesized | `pmatrix {a & b # c & d}` |
| Bracketed | `bmatrix {1 & 0 # 0 & 1}` |
| Determinant | `dmatrix {a & b # c & d}` |

## Systems of Equations

| Expression | Script |
|------------|--------|
| System | `cases {2x+y=5 # 3x-2y=4}` |
| Aligned equations | `eqalign {a &= b # c &= d}` |
| Vertical stack | `pile {a # b # c}` |

## Decorations

| Decoration | Script |
|------------|--------|
| Hat (^) | `hat a` |
| Tilde | `tilde a` |
| Vector arrow | `vec v` |
| Overline | `bar x` |
| Underline | `under x` |
| Single dot | `dot a` |
| Double dot | `ddot a` |

## Greek Letters

Lowercase: `alpha`, `beta`, `gamma`, `delta`, `epsilon`, `zeta`, `eta`, `theta`, `iota`, `kappa`, `lambda`, `mu`, `nu`, `xi`, `pi`, `rho`, `sigma`, `tau`, `upsilon`, `phi`, `chi`, `psi`, `omega`

Uppercase: `ALPHA`, `BETA`, `GAMMA`, `DELTA`, etc.

Variants: `vartheta`, `varphi`, `varepsilon`

## Special Symbols

| Symbol | Script |
|--------|--------|
| Infinity | `inf` |
| Partial derivative | `partial` |
| Nabla | `nabla` |
| Therefore | `therefore` |
| Because | `because` |
| For all | `forall` |
| Exists | `exist` |
| Plus-minus | `+-` or `pm` |
| Not equal | `ne` |
| Less or equal | `le` or `leq` |
| Greater or equal | `ge` or `geq` |
| Approximately | `approx` |
| Equivalent | `equiv` |
| Subset | `subset` |
| Element of | `in` |
| Right arrow | `->` or `rarrow` |
| Left arrow | `larrow` |
| Bidirectional | `<->` or `lrarrow` |
| Ellipsis (centered) | `cdots` |

## Font Styles

| Style | Command |
|-------|---------|
| Roman (upright) | `rm` |
| Italic | `it` |
| Bold | `bold` |
| Bold roman | `rmbold` |

## Built-in Functions

Auto-roman: `sin`, `cos`, `tan`, `cot`, `sec`, `csc`, `arcsin`, `arccos`, `arctan`, `log`, `ln`, `lg`, `exp`, `det`, `mod`, `gcd`, `max`, `min`, `sinh`, `cosh`, `tanh`

---

## Grade-Level Examples

### Middle School (Grade 7-9)

```
# Linear equation
2x + 3 = 7

# Fraction equation
{2x+1} over 3 = {x-2} over 5

# System of equations
cases {2x + y = 5 # 3x - 2y = 4}

# Square root
sqrt 12 + sqrt 27 - sqrt 48

# Inequality
3x - 5 > 2x + 1

# Quadratic equation
x^2 - 5x + 6 = 0

# Pythagorean theorem
a^2 + b^2 = c^2

# Linear function
y = ax + b
```

### High School Math I (Grade 10)

```
# Exponent rules
a^m times a^n = a^{m+n}

# Logarithm
log _a xy = log _a x + log _a y

# Absolute value
left | x - 3 right | < 5

# Quadratic vertex form
y = a(x - p)^2 + q

# Quadratic formula
x = {-b +- sqrt {b^2 - 4ac}} over {2a}
```

### High School Math II (Grade 11)

```
# Limit
lim _{x -> 0} {sin x} over x = 1

# Derivative definition
f'(x) = lim _{h -> 0} {f(x+h) - f(x)} over h

# Definite integral
int _{0} ^{pi} sin x dx = 2

# Series
sum _{k=1} ^{n} k = {n(n+1)} over 2

# Arithmetic sequence
a_n = a_1 + (n-1)d
```

### Probability and Statistics

```
# Combination
{_n}C{_r} = {n!} over {r!(n-r)!}

# Binomial theorem
(a+b)^n = sum _{k=0} ^{n} {_n}C{_k} a^{n-k} b^k

# Probability
P(A cup B) = P(A) + P(B) - P(A cap B)

# Normal distribution
f(x) = {1} over {sigma sqrt {2 pi}} e^{-{(x- mu)^2} over {2 sigma ^2}}
```

### Calculus

```
# Derivative
{d} over {dx} x^n = n x^{n-1}

# Chain rule
{dy} over {dx} = {dy} over {du} times {du} over {dx}

# Integration by parts
int u dv = uv - int v du

# Substitution
int f(g(x)) g'(x) dx = int f(u) du

# Taylor series
e^x = sum _{n=0} ^{inf} {x^n} over {n!}
```

### Geometry

```
# Dot product
vec a cdot vec b = left | vec a right | left | vec b right | cos theta

# Circle equation
(x-a)^2 + (y-b)^2 = r^2

# Ellipse
{x^2} over {a^2} + {y^2} over {b^2} = 1

# Hyperbola
{x^2} over {a^2} - {y^2} over {b^2} = 1

# Matrix multiplication
pmatrix {a & b # c & d} pmatrix {x # y} = pmatrix {ax+by # cx+dy}
```
