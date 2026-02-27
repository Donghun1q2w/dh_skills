/*
 * SharedApiKeyLoader.cs
 * =====================
 * 부서 공용서버에 위치한 .env 파일에서 API 키를 로드하는 유틸리티.
 *
 * 사용법:
 *     var loader = new SharedApiKeyLoader();       // settings.ini 자동 탐색
 *     loader.LoadSharedKeys();
 *     string apiKey = loader.GetKey("OPENAI_API_KEY");
 *
 * 의존성: 없음 (표준 라이브러리만 사용)
 */

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

/// <summary>
/// settings.ini에 지정된 공용서버 .env 파일에서 API 키를 로드한다.
/// </summary>
public class SharedApiKeyLoader
{
    private readonly string _settingsPath;
    private readonly Dictionary<string, string> _keys = new();

    /// <param name="settingsPath">
    /// settings.ini 경로. null이면 실행 파일과 같은 디렉토리에서 자동 탐색.
    /// </param>
    public SharedApiKeyLoader(string settingsPath = null)
    {
        _settingsPath = settingsPath
            ?? Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "settings.ini");
    }

    /// <summary>
    /// settings.ini에 지정된 공용서버 .env 파일을 읽어 내부 딕셔너리에 로드한다.
    /// </summary>
    /// <returns>공용서버 .env 로드 성공 여부</returns>
    public bool LoadSharedKeys()
    {
        if (!File.Exists(_settingsPath))
            throw new FileNotFoundException($"설정 파일을 찾을 수 없습니다: {_settingsPath}");

        var ini = ReadIni(_settingsPath);

        string envPath = GetIniValue(ini, "server", "env_path", "");
        string encoding = GetIniValue(ini, "options", "encoding", "utf-8");
        bool useFallback = GetIniValue(ini, "options", "use_local_fallback", "true")
            .Equals("true", StringComparison.OrdinalIgnoreCase);
        string localEnvPath = GetIniValue(ini, "options", "local_env_path", ".env");

        var enc = Encoding.GetEncoding(encoding);

        // 1) 공용서버 경로 시도
        if (!string.IsNullOrEmpty(envPath) && File.Exists(envPath))
        {
            LoadEnvFile(envPath, enc);
            Console.WriteLine($"[INFO] 공용서버 .env 로드 완료: {envPath}");
            return true;
        }

        Console.WriteLine($"[WARN] 공용서버 .env 접근 불가: {envPath}");

        // 2) 로컬 폴백
        if (useFallback)
        {
            string localPath = Path.IsPathRooted(localEnvPath)
                ? localEnvPath
                : Path.Combine(Directory.GetCurrentDirectory(), localEnvPath);

            if (File.Exists(localPath))
            {
                LoadEnvFile(localPath, enc);
                Console.WriteLine($"[INFO] 로컬 폴백 .env 로드 완료: {localPath}");
                return false;
            }
        }

        Console.WriteLine("[ERROR] 사용 가능한 .env 파일이 없습니다.");
        return false;
    }

    /// <summary>API 키를 가져온다.</summary>
    public string GetKey(string keyName, string defaultValue = null)
    {
        if (_keys.TryGetValue(keyName, out string value))
            return value;

        // 환경변수에서도 시도
        string envValue = Environment.GetEnvironmentVariable(keyName);
        if (envValue != null)
            return envValue;

        if (defaultValue == null)
            Console.WriteLine($"[WARN] 키를 찾을 수 없습니다: {keyName}");

        return defaultValue;
    }

    /// <summary>로드된 키 목록을 마스킹하여 반환한다.</summary>
    public Dictionary<string, string> ListKeys()
    {
        return _keys.ToDictionary(
            kv => kv.Key,
            kv => kv.Value.Length > 8
                ? kv.Value[..8] + new string('*', kv.Value.Length - 8)
                : kv.Value
        );
    }

    // ---------------------------------------------------------------
    // 내부 메서드
    // ---------------------------------------------------------------

    private void LoadEnvFile(string path, Encoding encoding)
    {
        foreach (string rawLine in File.ReadAllLines(path, encoding))
        {
            string line = rawLine.Trim();
            if (string.IsNullOrEmpty(line) || line.StartsWith("#"))
                continue;

            int idx = line.IndexOf('=');
            if (idx <= 0) continue;

            string key = line[..idx].Trim();
            string val = line[(idx + 1)..].Trim().Trim('"');
            _keys[key] = val;
            Environment.SetEnvironmentVariable(key, val);
        }
    }

    /// <summary>간이 INI 파서. [section] → key=value 구조를 딕셔너리로 반환.</summary>
    private static Dictionary<string, Dictionary<string, string>> ReadIni(string path)
    {
        var result = new Dictionary<string, Dictionary<string, string>>(
            StringComparer.OrdinalIgnoreCase);
        string currentSection = "";

        foreach (string rawLine in File.ReadAllLines(path, Encoding.UTF8))
        {
            string line = rawLine.Trim();
            if (string.IsNullOrEmpty(line) || line.StartsWith("#") || line.StartsWith(";"))
                continue;

            if (line.StartsWith("[") && line.EndsWith("]"))
            {
                currentSection = line[1..^1].Trim();
                if (!result.ContainsKey(currentSection))
                    result[currentSection] = new Dictionary<string, string>(
                        StringComparer.OrdinalIgnoreCase);
                continue;
            }

            int idx = line.IndexOf('=');
            if (idx > 0 && result.ContainsKey(currentSection))
            {
                string key = line[..idx].Trim();
                string val = line[(idx + 1)..].Trim();
                result[currentSection][key] = val;
            }
        }

        return result;
    }

    private static string GetIniValue(
        Dictionary<string, Dictionary<string, string>> ini,
        string section, string key, string fallback)
    {
        if (ini.TryGetValue(section, out var sec) && sec.TryGetValue(key, out string val))
            return val;
        return fallback;
    }
}

// ---------------------------------------------------------------------------
// 사용 예제 (콘솔 앱에서 직접 실행)
// ---------------------------------------------------------------------------
// class Program
// {
//     static void Main()
//     {
//         var loader = new SharedApiKeyLoader();
//         loader.LoadSharedKeys();
//
//         // 키 목록 (마스킹)
//         foreach (var kv in loader.ListKeys())
//             Console.WriteLine($"  {kv.Key}: {kv.Value}");
//
//         // 개별 키 참조
//         string openaiKey = loader.GetKey("OPENAI_API_KEY");
//         string anthropicKey = loader.GetKey("ANTHROPIC_API_KEY");
//     }
// }
