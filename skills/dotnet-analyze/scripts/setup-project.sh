#!/bin/bash
# ============================================
# .NET Analyzer 공통 프로젝트 설정 스크립트
# 모든 dotnet-* 스킬이 공유하는 기반 프로젝트를 생성한다.
# ============================================

PROJ_DIR="/tmp/dotnet-analyzer"

if [ -f "$PROJ_DIR/DotNetAnalyzer.csproj" ]; then
    echo "[OK] 프로젝트가 이미 존재합니다: $PROJ_DIR"
    exit 0
fi

echo "[SETUP] .NET Analyzer 프로젝트 초기화 중..."

mkdir -p "$PROJ_DIR"
cd "$PROJ_DIR"

# 프로젝트 파일 생성
cat > DotNetAnalyzer.csproj << 'CSPROJ'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="ICSharpCode.Decompiler" Version="8.2.0.7535" />
    <PackageReference Include="dnlib" Version="4.4.0" />
  </ItemGroup>
</Project>
CSPROJ

# NuGet 패키지 복원
echo "[SETUP] NuGet 패키지 복원 중..."
dotnet restore --verbosity quiet

if [ $? -eq 0 ]; then
    echo "[OK] 프로젝트 설정 완료: $PROJ_DIR"
else
    echo "[ERROR] NuGet 패키지 복원 실패. .NET 8 SDK가 설치되어 있는지 확인하세요."
    echo "  다운로드: https://dotnet.microsoft.com/download/dotnet/8.0"
    exit 1
fi
