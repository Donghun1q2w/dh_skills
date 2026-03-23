using Aveva.Core.Database;
using Aveva.Core.Utilities.CommandLine;
using Aveva.Core.Utilities.Messaging;
using Aveva.E3D.Standalone;
using System;
using System.Collections;
using System.IO;
using System.Reflection;
using System.Text;

namespace E3DStandaloneTemplate
{
    /// <summary>
    /// E3D Standalone 접속 → PML 매크로 실행 → 종료 템플릿.
    /// Platform Target: x86, .NET Framework 4.0+
    /// </summary>
    public class E3DConnection : IDisposable
    {
        private bool _initialized;
        private bool _loggedIn;
        private string _e3dPath;

        /// <summary>
        /// E3D 설치 경로의 DLL을 런타임에 로드하기 위한 핸들러 등록.
        /// Main 진입 시 Standalone.Start 호출 전에 반드시 호출해야 함.
        /// </summary>
        public static void RegisterAssemblyResolver(string e3dPath)
        {
            AppDomain.CurrentDomain.AssemblyResolve += (sender, args) =>
            {
                string name = new AssemblyName(args.Name).Name;
                string dllPath = Path.Combine(e3dPath, name + ".dll");
                if (File.Exists(dllPath))
                    return Assembly.LoadFrom(dllPath);
                return null;
            };
        }

        /// <summary>
        /// E3D 엔진 초기화.
        /// </summary>
        /// <param name="env">환경변수 Hashtable (AVEVA_DESIGN_EXE, projects_dir 등)</param>
        /// <param name="moduleNumber">모듈 번호 (E3D Design = 78)</param>
        public void Initialize(Hashtable env, int moduleNumber = 78)
        {
            Standalone.Start(moduleNumber, env);
            _initialized = true;
        }

        /// <summary>
        /// 프로젝트 로그인.
        /// </summary>
        public void Login(string project, string userId, string password, string mdb)
        {
            if (!_initialized)
                throw new InvalidOperationException("Initialize()를 먼저 호출하세요.");

            PdmsMessage error;
            if (!Standalone.Open(project, userId, password, mdb, out error))
            {
                string msg = error.MessageText();
                Standalone.ExitError(msg);
                throw new Exception("E3D login failed: " + msg);
            }
            _loggedIn = true;
        }

        /// <summary>
        /// PML 명령 문자열 실행.
        /// </summary>
        public string RunCommand(string pmlText)
        {
            Command cmd = Command.CreateCommand(pmlText);
            if (!cmd.Run())
                throw new Exception("Command failed: " + cmd.Error.MessageText());

            try { return cmd.Result.Trim(); }
            catch { return string.Empty; }
        }

        /// <summary>
        /// PML 매크로 파일 실행.
        /// </summary>
        public void RunMacro(string macroFilePath)
        {
            RunCommand("$M /" + macroFilePath);
        }

        /// <summary>
        /// 매크로 파일 생성 후 실행.
        /// </summary>
        public void WriteMacroAndRun(string outputDir, string fileName, string macroContent)
        {
            string macroPath = Path.Combine(outputDir, fileName);
            File.WriteAllText(macroPath, macroContent, Encoding.UTF8);
            RunMacro(macroPath);
        }

        /// <summary>
        /// DB 루트 엘리먼트 가져오기.
        /// </summary>
        public DbElement GetWorldElement()
        {
            return DbElement.GetElement("/*");
        }

        public void Dispose()
        {
            if (_initialized)
            {
                try { Standalone.Finish(); }
                catch { /* safe to ignore */ }
                _initialized = false;
                _loggedIn = false;
            }
        }
    }

    // === 사용 예제 ===
    // static void Main()
    // {
    //     string e3dPath = @"C:\cae_prog\AVEVA\v2.x\e3d\";
    //     E3DConnection.RegisterAssemblyResolver(e3dPath);  // 필수: Standalone.Start 전에 호출
    //
    //     var env = EnvConfigHelper.BuildEnvHashtable(
    //         e3dPath: e3dPath,
    //         projectsDir: @"J:\cae_proj",
    //         userDataPath: @"C:\Users\Public\Documents\AVEVA\USERDATA",
    //         workPath: @"C:\temp\e3dwork"
    //     );
    //
    //     using (var conn = new E3DConnection())
    //     {
    //         conn.Initialize(env);
    //         conn.Login("TESTPROJ", "admin", "password", "TESTMDB");
    //
    //         // PML 명령 실행
    //         string result = conn.RunCommand("VAR !result FLNN");
    //         Console.WriteLine(result);
    //
    //         // 매크로 파일 실행
    //         conn.RunMacro(@"C:\macros\extract.mac");
    //     }
    // }
}
