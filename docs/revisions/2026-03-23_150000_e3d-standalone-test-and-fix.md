# e3d-standalone 스킬 테스트 및 런타임 DLL 로딩 패턴 추가

- **Date**: 2026-03-23 15:00:00
- **Author**: donghun.lee

## Rationale / Plan

e3d-standalone 스킬의 실제 동작을 검증하기 위해 ALP 프로젝트 대상 테스트 수행.
테스트 과정에서 런타임 시 AVEVA DLL 간접 의존성(DruidNet.dll 등) 로드 실패 문제를 발견하여
AssemblyResolve 핸들러 패턴을 스킬 문서와 템플릿에 반영함.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/e3d-standalone/SKILL.md` | Modified | AssemblyResolve 필수 패턴 및 evarProj.bat 환경변수 로드 섹션 추가 |
| `skills/e3d-standalone/references/e3d-connection-template.cs` | Modified | RegisterAssemblyResolver 정적 메서드 추가, 사용 예제 업데이트 |
| `refcode/e3dstandalone/E3DStandaloneTest/Program.cs` | Added | E3D Standalone 접속 테스트 콘솔 앱 |
| `refcode/e3dstandalone/E3DStandaloneTest/E3DStandaloneTest.csproj` | Added | .NET 4.0 x86 프로젝트 파일 |
| `refcode/e3dstandalone/E3DStandaloneTest/App.config` | Added | 런타임 설정 |
| `refcode/e3dstandalone/E3DStandaloneTest/run_test.bat` | Added | evarProj.bat 로드 후 테스트 실행 런처 |
| `refcode/e3dstandalone/E3DStandaloneTest/build.bat` | Added | MSBuild 빌드 스크립트 |

## Details

### `skills/e3d-standalone/SKILL.md` (Modified)

- "Runtime DLL Loading (필수)" 섹션 추가 — AssemblyResolve 핸들러 코드 및 설명
- "환경변수 로드 (evarProj.bat)" 섹션 추가 — bat 파일 패턴과 C# 연동 방법
- Error Handling 테이블의 "DLL 로드 실패" 항목에 AssemblyResolve 확인 추가

### `skills/e3d-standalone/references/e3d-connection-template.cs` (Modified)

- `using System.Reflection;` 추가
- `_e3dPath` 필드 추가
- `RegisterAssemblyResolver(string e3dPath)` 정적 메서드 추가 — E3D 경로에서 미해결 어셈블리 로드
- 사용 예제에 `RegisterAssemblyResolver` 호출 추가

### `refcode/e3dstandalone/E3DStandaloneTest/` (Added)

- 5단계 테스트: 환경변수 구성 → 엔진 초기화 → 로그인 → PML 명령 실행 → 종료
- ALP 프로젝트, SHIMUMCA/CA/SHIMUMCA 자격증명 사용
- evarProj.bat에서 시스템 환경변수 읽어 Hashtable 구성 (fallback 기본값 포함)
- 테스트 결과: Standalone.Start/Open/Command.Run/Finish 모두 성공
