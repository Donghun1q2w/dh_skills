'
' SharedApiKeyLoader.bas
' ======================
' 부서 공용서버에 위치한 .env 파일에서 API 키를 로드하는 VBA 모듈.
'
' 사용법:
'     LoadSharedKeys
'     Dim apiKey As String
'     apiKey = GetKey("OPENAI_API_KEY")
'
' 설치:
'     1) VBA 편집기(Alt+F11) > 삽입 > 모듈
'     2) 이 코드를 붙여넣기
'     3) settings.ini를 통합 문서와 같은 폴더에 배치
'
Option Explicit

' ---------------------------------------------------------------------------
' 모듈 수준 변수
' ---------------------------------------------------------------------------
Private m_Keys As Object  ' Scripting.Dictionary
Private m_Loaded As Boolean

' ---------------------------------------------------------------------------
' Public API
' ---------------------------------------------------------------------------

''' settings.ini에 지정된 공용서버 .env 파일에서 키를 로드한다.
''' @return True=공용서버 로드 성공, False=폴백 또는 실패
Public Function LoadSharedKeys(Optional ByVal settingsPath As String = "") As Boolean
    Dim iniPath As String
    Dim envPath As String
    Dim encoding As String
    Dim useFallback As Boolean
    Dim localEnvPath As String

    ' 딕셔너리 초기화
    If m_Keys Is Nothing Then
        Set m_Keys = CreateObject("Scripting.Dictionary")
        m_Keys.CompareMode = vbTextCompare
    End If
    m_Keys.RemoveAll

    ' settings.ini 경로 결정
    If settingsPath = "" Then
        iniPath = ThisWorkbook.Path & "\settings.ini"
    Else
        iniPath = settingsPath
    End If

    If Dir(iniPath) = "" Then
        Debug.Print "[ERROR] 설정 파일을 찾을 수 없습니다: " & iniPath
        LoadSharedKeys = False
        Exit Function
    End If

    ' INI 읽기
    envPath = ReadIniValue(iniPath, "server", "env_path", "")
    encoding = ReadIniValue(iniPath, "options", "encoding", "utf-8")
    useFallback = (LCase(ReadIniValue(iniPath, "options", "use_local_fallback", "true")) = "true")
    localEnvPath = ReadIniValue(iniPath, "options", "local_env_path", ".env")

    ' 1) 공용서버 경로 시도
    If envPath <> "" And Dir(envPath) <> "" Then
        LoadEnvFile envPath
        Debug.Print "[INFO] 공용서버 .env 로드 완료: " & envPath
        m_Loaded = True
        LoadSharedKeys = True
        Exit Function
    End If

    Debug.Print "[WARN] 공용서버 .env 접근 불가: " & envPath

    ' 2) 로컬 폴백
    If useFallback Then
        Dim localPath As String
        If InStr(localEnvPath, ":") > 0 Or Left(localEnvPath, 2) = "\\" Then
            localPath = localEnvPath
        Else
            localPath = ThisWorkbook.Path & "\" & localEnvPath
        End If

        If Dir(localPath) <> "" Then
            LoadEnvFile localPath
            Debug.Print "[INFO] 로컬 폴백 .env 로드 완료: " & localPath
            m_Loaded = True
            LoadSharedKeys = False
            Exit Function
        End If
    End If

    Debug.Print "[ERROR] 사용 가능한 .env 파일이 없습니다."
    LoadSharedKeys = False
End Function


''' 환경변수에서 API 키를 가져온다.
''' @param keyName 키 이름 (예: "OPENAI_API_KEY")
''' @param defaultValue 키가 없을 때 반환할 기본값
''' @return 키 값 또는 기본값
Public Function GetKey(ByVal keyName As String, Optional ByVal defaultValue As String = "") As String
    If m_Keys Is Nothing Then
        Debug.Print "[WARN] LoadSharedKeys를 먼저 호출하세요."
        GetKey = defaultValue
        Exit Function
    End If

    If m_Keys.Exists(keyName) Then
        GetKey = m_Keys(keyName)
    ElseIf Environ(keyName) <> "" Then
        GetKey = Environ(keyName)
    Else
        If defaultValue = "" Then
            Debug.Print "[WARN] 키를 찾을 수 없습니다: " & keyName
        End If
        GetKey = defaultValue
    End If
End Function


''' 로드된 키 목록을 마스킹하여 Immediate 창에 출력한다.
Public Sub ListKeys()
    If m_Keys Is Nothing Or Not m_Loaded Then
        Debug.Print "[WARN] 로드된 키가 없습니다."
        Exit Sub
    End If

    Dim k As Variant
    Dim v As String
    Dim masked As String

    Debug.Print "--- 로드된 키 목록 (마스킹) ---"
    For Each k In m_Keys.Keys
        v = m_Keys(k)
        If Len(v) > 8 Then
            masked = Left(v, 8) & String(Len(v) - 8, "*")
        Else
            masked = v
        End If
        Debug.Print "  " & k & ": " & masked
    Next k
End Sub


' ---------------------------------------------------------------------------
' 내부 메서드
' ---------------------------------------------------------------------------

''' .env 파일을 파싱하여 딕셔너리에 저장한다.
Private Sub LoadEnvFile(ByVal filePath As String)
    Dim fso As Object
    Dim ts As Object
    Dim line As String
    Dim eqPos As Long
    Dim keyName As String
    Dim keyValue As String

    Set fso = CreateObject("Scripting.FileSystemObject")
    Set ts = fso.OpenTextFile(filePath, 1, False, -1)  ' -1 = TristateTrue (Unicode)

    Do While Not ts.AtEndOfStream
        line = Trim(ts.ReadLine)

        ' 빈 줄, 주석 건너뛰기
        If line = "" Or Left(line, 1) = "#" Then GoTo NextLine

        eqPos = InStr(line, "=")
        If eqPos <= 1 Then GoTo NextLine

        keyName = Trim(Left(line, eqPos - 1))
        keyValue = Trim(Mid(line, eqPos + 1))

        ' 따옴표 제거
        If Left(keyValue, 1) = """" And Right(keyValue, 1) = """" Then
            keyValue = Mid(keyValue, 2, Len(keyValue) - 2)
        End If

        m_Keys(keyName) = keyValue
NextLine:
    Loop

    ts.Close
    Set ts = Nothing
    Set fso = Nothing
End Sub


''' 간이 INI 파서. 지정된 섹션/키의 값을 반환한다.
Private Function ReadIniValue(ByVal filePath As String, ByVal section As String, _
                              ByVal key As String, ByVal fallback As String) As String
    Dim fso As Object
    Dim ts As Object
    Dim line As String
    Dim inSection As Boolean

    Set fso = CreateObject("Scripting.FileSystemObject")

    If Not fso.FileExists(filePath) Then
        ReadIniValue = fallback
        Exit Function
    End If

    Set ts = fso.OpenTextFile(filePath, 1, False)
    inSection = False

    Do While Not ts.AtEndOfStream
        line = Trim(ts.ReadLine)

        If line = "" Or Left(line, 1) = "#" Or Left(line, 1) = ";" Then GoTo NextIniLine

        ' 섹션 헤더 확인
        If Left(line, 1) = "[" And Right(line, 1) = "]" Then
            Dim secName As String
            secName = Trim(Mid(line, 2, Len(line) - 2))
            inSection = (LCase(secName) = LCase(section))
            GoTo NextIniLine
        End If

        ' 해당 섹션 내 키=값 확인
        If inSection Then
            Dim eqPos2 As Long
            eqPos2 = InStr(line, "=")
            If eqPos2 > 0 Then
                Dim k As String
                k = Trim(Left(line, eqPos2 - 1))
                If LCase(k) = LCase(key) Then
                    ReadIniValue = Trim(Mid(line, eqPos2 + 1))
                    ts.Close
                    Exit Function
                End If
            End If
        End If
NextIniLine:
    Loop

    ts.Close
    Set ts = Nothing
    Set fso = Nothing

    ReadIniValue = fallback
End Function


' ---------------------------------------------------------------------------
' 사용 예제 (테스트용 서브루틴)
' ---------------------------------------------------------------------------
' Sub TestApiKeyLoader()
'     LoadSharedKeys
'
'     ' 키 목록 확인
'     ListKeys
'
'     ' 개별 키 참조
'     Dim openaiKey As String
'     openaiKey = GetKey("OPENAI_API_KEY")
'     Debug.Print "OPENAI_API_KEY = " & openaiKey
'
'     ' HTTP 요청 예시 (WinHttp 사용)
'     ' Dim http As Object
'     ' Set http = CreateObject("WinHttp.WinHttpRequest.5.1")
'     ' http.Open "POST", "https://api.openai.com/v1/chat/completions", False
'     ' http.SetRequestHeader "Authorization", "Bearer " & openaiKey
'     ' http.SetRequestHeader "Content-Type", "application/json"
'     ' http.Send "{""model"":""gpt-4o"",""messages"":[{""role"":""user"",""content"":""Hello!""}]}"
'     ' Debug.Print http.ResponseText
' End Sub
