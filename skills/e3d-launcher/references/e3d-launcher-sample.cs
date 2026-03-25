using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

/// <summary>
/// E3D Module Launcher (C#)
/// mon.exe를 통해 E3D Design/Drawing/Paragon/Admin 모듈을 프로세스로 실행한다.
/// </summary>
namespace E3DLauncher
{
    // ── 기본 경로 ──────────────────────────────────────────

    public static class DefaultPaths
    {
        public static readonly string[] DesignPaths =
        {
            @"C:\cae_prog\AVEVA\v2.x\e3d",
            @"C:\Program Files (x86)\AVEVA\Everything3D2.10",
        };

        public static readonly string[] AdminPaths =
        {
            @"C:\cae_prog\AVEVA\v2.x\Administration",
            @"C:\Program Files (x86)\AVEVA\Administration",
        };
    }

    // ── Config Models ──────────────────────────────────────

    public class LaunchConfig
    {
        [JsonPropertyName("settings")]
        public LaunchSettings Settings { get; set; } = new();

        [JsonPropertyName("projects")]
        public Dictionary<string, ProjectCredential> Projects { get; set; } = new();
    }

    public class LaunchSettings
    {
        [JsonPropertyName("aveva_design_installed_dir")]
        public string DesignDir { get; set; } = @"C:\cae_prog\AVEVA\v2.x\e3d";

        [JsonPropertyName("aveva_admin_installed_dir")]
        public string AdminDir { get; set; } = @"C:\cae_prog\AVEVA\v2.x\Administration";

        [JsonPropertyName("target_dir")]
        public string TargetDir { get; set; } = @"%PUBLIC%\Documents\AVEVA\USERDATA";

        [JsonPropertyName("working_dir")]
        public string WorkingDir { get; set; } = "";

        [JsonPropertyName("batch_file")]
        public string BatchFile { get; set; } = "";
    }

    public class ProjectCredential
    {
        [JsonPropertyName("USERNAME")]
        public string Username { get; set; } = "";

        [JsonPropertyName("PASSWORD")]
        public string Password { get; set; } = "";

        [JsonPropertyName("MDB")]
        public string Mdb { get; set; } = "";

        [JsonPropertyName("systemUSERNAME")]
        public string SystemUsername { get; set; } = "";

        [JsonPropertyName("systemPASSWORD")]
        public string SystemPassword { get; set; } = "";

        [JsonPropertyName("systeMDB")]
        public string SystemMdb { get; set; } = "";
    }

    // ── Module Definitions ─────────────────────────────────

    public enum E3DModule { Design, Drawing, Paragon, Admin }

    public enum StartMode { TTY, CONSOLE, NOCONSOLE }

    // ── Launcher ───────────────────────────────────────────

    public static class E3DModuleLauncher
    {
        private static string? _lastTempInitPath;

        /// <summary>config.json을 로드한다.</summary>
        public static LaunchConfig LoadConfig(string configPath)
        {
            var json = File.ReadAllText(configPath);
            return JsonSerializer.Deserialize<LaunchConfig>(json)
                ?? throw new InvalidOperationException($"Config 역직렬화 실패: {configPath}");
        }

        /// <summary>E3D 모듈을 프로세스로 실행한다.</summary>
        public static Process Launch(
            E3DModule module,
            string projectCode,
            StartMode startMode = StartMode.CONSOLE,
            string? command = null,
            LaunchConfig? config = null)
        {
            config ??= LoadConfig("config.json");
            projectCode = projectCode.ToUpperInvariant();

            if (!config.Projects.TryGetValue(projectCode, out var cred))
                throw new InvalidOperationException($"프로젝트 '{projectCode}'를 config에서 찾을 수 없습니다.");

            return module switch
            {
                E3DModule.Design  => LaunchE3D(config.Settings, cred, projectCode, startMode, command ?? "design"),
                E3DModule.Drawing => LaunchE3D(config.Settings, cred, projectCode, startMode, command ?? "drawing"),
                E3DModule.Paragon => LaunchCatalogue(config.Settings, cred, projectCode, startMode, command),
                E3DModule.Admin   => LaunchAdmin(config.Settings, cred, projectCode, startMode, command),
                _ => throw new ArgumentOutOfRangeException(nameof(module))
            };
        }

        /// <summary>마지막에 생성된 temp init 파일을 삭제한다.</summary>
        public static void CleanupTempInit()
        {
            if (_lastTempInitPath != null && File.Exists(_lastTempInitPath)
                && _lastTempInitPath.EndsWith("_temp.init"))
            {
                File.Delete(_lastTempInitPath);
                Console.WriteLine($"[Cleanup] Temp init 삭제: {_lastTempInitPath}");
                _lastTempInitPath = null;
            }
        }

        // ── Design / Drawing ───────────────────────────────

        private static Process LaunchE3D(
            LaunchSettings settings, ProjectCredential cred,
            string projectCode, StartMode mode, string command)
        {
            var designDir = ResolveInstallPath(settings.DesignDir, DefaultPaths.DesignPaths);
            var exePath = Path.Combine(designDir, "mon.exe");
            var initPath = Path.Combine(designDir, "launch.init");
            initPath = ApplyBatchFile(initPath, settings.BatchFile);

            var args = $"PROD E3D init \"{initPath}\" {mode} {projectCode} " +
                       $"{cred.Username}/{cred.Password} /{cred.Mdb} {command}";

            return StartProcess(exePath, args, settings.WorkingDir);
        }

        // ── Paragon (Catalogue) ────────────────────────────

        private static Process LaunchCatalogue(
            LaunchSettings settings, ProjectCredential cred,
            string projectCode, StartMode mode, string? command)
        {
            var designDir = ResolveInstallPath(settings.DesignDir, DefaultPaths.DesignPaths);
            var exePath = Path.Combine(designDir, "mon.exe");
            var initPath = Path.Combine(designDir, "catalogue.init");
            initPath = ApplyBatchFile(initPath, settings.BatchFile);

            var args = $"PROD CATALOGUE init \"{initPath}\" {mode} {projectCode} " +
                       $"{cred.Username}/{cred.Password} /{cred.Mdb} {command ?? "PARAGON"}";

            return StartProcess(exePath, args, settings.WorkingDir);
        }

        // ── Admin ──────────────────────────────────────────

        private static Process LaunchAdmin(
            LaunchSettings settings, ProjectCredential cred,
            string projectCode, StartMode mode, string? command)
        {
            var adminDir = ResolveInstallPath(settings.AdminDir, DefaultPaths.AdminPaths);
            var exePath = Path.Combine(adminDir, "mon.exe");
            var initPath = Path.Combine(adminDir, "admin.init");
            initPath = ApplyBatchFile(initPath, settings.BatchFile);

            var args = $"PROD ADMIN init \"{initPath}\" {mode} {projectCode} " +
                       $"{cred.SystemUsername}/{cred.SystemPassword} /{cred.SystemMdb} {command ?? "ADMIN"}";

            return StartProcess(exePath, args, settings.WorkingDir);
        }

        // ── Temp Init ──────────────────────────────────────

        /// <summary>batch_file이 있으면 temp init 파일을 생성하여 경로를 반환한다.</summary>
        private static string ApplyBatchFile(string initPath, string batchFile)
        {
            if (string.IsNullOrWhiteSpace(batchFile) || !File.Exists(batchFile))
                return initPath;

            var content = File.ReadAllText(initPath).TrimEnd()
                + Environment.NewLine
                + $"call \"{batchFile}\""
                + Environment.NewLine;

            var tempPath = initPath.Replace(".init", "_temp.init");
            File.WriteAllText(tempPath, content);
            _lastTempInitPath = tempPath;

            Console.WriteLine($"[Temp Init] {tempPath}");
            return tempPath;
        }

        // ── Helpers ────────────────────────────────────────

        private static Process StartProcess(string exePath, string arguments, string workingDir)
        {
            if (!File.Exists(exePath))
                throw new FileNotFoundException($"mon.exe를 찾을 수 없습니다: {exePath}");

            var psi = new ProcessStartInfo
            {
                FileName = exePath,
                Arguments = arguments,
                WorkingDirectory = Directory.Exists(workingDir) ? workingDir : "",
                UseShellExecute = false,
            };

            Console.WriteLine($"[E3D Launcher] Exe: {exePath}");
            Console.WriteLine($"[E3D Launcher] Args: {arguments}");

            return Process.Start(psi)
                ?? throw new InvalidOperationException("프로세스 시작 실패");
        }

        /// <summary>사용자 지정 경로 → 기본 경로 목록 → v2.x→v3.x 대체 순으로 탐색.</summary>
        private static string ResolveInstallPath(string customPath, string[] defaultPaths)
        {
            if (!string.IsNullOrWhiteSpace(customPath) && Directory.Exists(customPath))
                return customPath;

            foreach (var path in defaultPaths)
            {
                if (Directory.Exists(path))
                    return path;

                var v3 = path.Replace("v2.x", "v3.x", StringComparison.OrdinalIgnoreCase);
                if (v3 != path && Directory.Exists(v3))
                    return v3;
            }

            throw new FileNotFoundException("E3D 설치 경로를 찾을 수 없습니다.");
        }
    }

    // ── Usage Example ──────────────────────────────────────
    //
    //   var config = E3DModuleLauncher.LoadConfig("config.json");
    //
    //   // Design 모듈 실행 (batch_file이 config에 있으면 자동 temp init 생성)
    //   var process = E3DModuleLauncher.Launch(E3DModule.Design, "TESTPROJ", config: config);
    //   process.WaitForExit();
    //   E3DModuleLauncher.CleanupTempInit();
    //
    //   // Drawing 모듈 실행
    //   E3DModuleLauncher.Launch(E3DModule.Drawing, "TESTPROJ", StartMode.NOCONSOLE, config: config);
    //
    //   // Admin 모듈 실행
    //   E3DModuleLauncher.Launch(E3DModule.Admin, "TESTPROJ", config: config);
    //
    //   // 매크로 경로를 COMMAND로 전달
    //   E3DModuleLauncher.Launch(E3DModule.Design, "TESTPROJ", command: @"J:\cae_mac\script.mac", config: config);
}
