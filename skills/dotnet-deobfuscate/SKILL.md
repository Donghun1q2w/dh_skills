---
name: dotnet-deobfuscate
description: "난독화된 .NET 어셈블리를 정리한다. 읽을 수 없는 이름 복원, 암호화된 문자열 복호화, 난독화 어트리뷰트 제거, 데드코드 정리를 수행하여 분석 가능한 깨끗한 DLL/EXE를 생성한다. '난독화 해제', '이름 복원', '문자열 복호화', 'deobfuscate', '코드가 읽히지 않는다', '변수명이 이상하다', 'ConfuserEx 해제', 'Dotfuscator 해제' 같은 요청에 반드시 이 스킬을 사용하라. 난독화 감지만 원하면 dotnet-analyze를 사용한다."
allowed-tools: Bash, Read, Write, Grep, Glob
---

# .NET 어셈블리 난독화 해제

dnlib을 사용하여 난독화된 .NET 어셈블리를 정리하고, 분석 가능한 깨끗한 바이너리를 생성한다.

## 사전 요건

- .NET 8 SDK
- 공통 프로젝트: `dotnet-analyze` 스킬의 `scripts/setup-project.sh` 실행

## 난독화 해제 4단계 파이프라인

### 1단계: 이름 복원 (Name Restoration)

난독화된 이름을 타입과 용도를 기반으로 추론한 의미있는 이름으로 교체한다.

**이름 복원 전략:**

| 대상 | 복원 규칙 | 예시 |
|------|-----------|------|
| 타입 (Class) | `{Kind}_{Namespace}_{순번}` | `Class_Services_001` |
| 타입 (Interface) | `IFace_{Namespace}_{순번}` | `IFace_Data_002` |
| 타입 (Enum) | `Enum_{Namespace}_{순번}` | `Enum_Models_003` |
| 메서드 (void 반환) | `Do_{순번}` 또는 `Process_{순번}` | `Do_0012` |
| 메서드 (bool 반환) | `Check_{순번}` | `Check_0015` |
| 메서드 (string 반환) | `GetText_{순번}` | `GetText_0018` |
| 메서드 (컬렉션 반환) | `GetList_{순번}` | `GetList_0020` |
| 필드 (static) | `s_field_{순번}` | `s_field_0025` |
| 필드 (bool) | `m_flag_{순번}` | `m_flag_0030` |
| 필드 (string) | `m_text_{순번}` | `m_text_0031` |
| 필드 (int) | `m_num_{순번}` | `m_num_0032` |
| 프로퍼티 | `Prop_{순번}` | `Prop_0040` |

### 2단계: 문자열 복호화 (String Decryption)

정적 분석으로 감지 가능한 패턴을 처리한다.

**지원하는 패턴:**
- `ldstr` + `call FromBase64String` → Base64 디코딩 후 인라인 치환
- `ldstr` + `call XorDecrypt` (단순 상수 키) → XOR 복호화 시도
- 문자열 프록시 메서드 감지 (상수 인덱스로 배열 접근)

**한계:**
- 동적 키를 사용하는 복호화는 정적 분석으로 불가능
- ConfuserEx의 상수 보호는 런타임 분석이 필요 (de4dot 추천)
- 커스텀 암호화 알고리즘은 수동 분석 필요

### 3단계: 난독화 어트리뷰트 제거

모듈, 어셈블리, 타입 레벨에서 다음 키워드를 포함하는 CustomAttribute를 제거한다:

`Dotfuscator`, `Obfusc`, `ConfusedBy`, `SmartAssembly`, `Suppress`, `NETGuard`, `Babel`, `Eazfuscator`, `CryptoObfuscator`, `ILProtector`

### 4단계: 데드코드 정리

- 연속 NOP 명령어 제거 (분기 대상 NOP 제외)
- 참조되지 않는 빈 타입 식별 (삭제는 하지 않고 보고만)

## 스크립트 템플릿

상세 구현은 `references/deobfuscate-template.cs`를 참조한다.

## 핵심 코드 패턴

```csharp
using dnlib.DotNet;
using dnlib.DotNet.Writer;

var module = ModuleDefMD.Load(inputPath);

// 이름 복원
foreach (var type in module.GetTypes())
{
    if (IsObfuscatedName(type.Name))
        type.Name = $"Class_{counter++:D3}";

    foreach (var method in type.Methods)
    {
        if (method.IsConstructor) continue;
        if (IsObfuscatedName(method.Name))
            method.Name = $"Method_{counter++:D4}";
    }
}

// 저장
var options = new ModuleWriterOptions(module)
{
    Logger = DummyLogger.NoThrowInstance  // 오류 시 예외 대신 무시
};
module.Write(outputPath, options);
```

## 출력

```
┌──────────────────────────────────────┐
│      난독화 해제 결과                │
├─────────────────┬────────────────────┤
│ 이름 복원       │ 247                │
│ 문자열 복호화   │ 12                 │
│ 어트리뷰트 제거 │ 3                  │
│ 데드코드 정리   │ 1,204              │
│ 합계            │ 1,466              │
└─────────────────┴────────────────────┘
✓ 출력 파일: MyApp_cleaned.dll
```

## 권장 워크플로우

```
1. dotnet-analyze로 난독화 감지
     ↓ (난독화 확인됨)
2. dotnet-deobfuscate로 정리
     ↓ (깨끗한 DLL 생성)
3. dotnet-decompile로 소스 복원
     ↓ (읽을 수 있는 C# 코드)
4. dotnet-callgraph로 구조 시각화
```

## 고급: de4dot 통합

ConfuserEx 등 고도의 난독화에는 오픈소스 도구 de4dot의 사용을 권장한다:

```bash
# de4dot 사용 (별도 설치 필요)
de4dot target.dll -o target_cleaned.dll

# 이후 이 스킬의 이름 복원을 추가로 적용할 수 있다
```

## 주의사항

- 난독화 해제된 DLL은 원본과 동일하게 실행되지 않을 수 있다 (서명 무효화)
- Strong Name이 있는 어셈블리는 재서명이 필요하다
- 라이선스 보호 목적의 난독화 해제는 법적 문제가 될 수 있다
- 이 스킬은 보안 분석/호환성 유지/레거시 코드 이해 목적으로만 사용한다
