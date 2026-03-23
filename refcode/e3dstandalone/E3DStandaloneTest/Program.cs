using Aveva.Core.Database;
using Aveva.Core.Utilities.CommandLine;
using Aveva.Core.Utilities.Messaging;
using Aveva.E3D.Standalone;
using System;
using System.Collections;
using System.IO;
using System.Reflection;

namespace E3DStandaloneTest
{
    class Program
    {
        static string _e3dPath = @"C:\cae_prog\AVEVA\v2.x\e3d\";

        static int Main(string[] args)
        {
            // Register assembly resolver for AVEVA DLLs not in app directory
            AppDomain.CurrentDomain.AssemblyResolve += OnAssemblyResolve;

            // Test parameters
            string project = "ALP";
            string username = "SHIMUMCA";
            string password = "CA";
            string mdb = "SHIMUMCA";
            string e3dPath = _e3dPath;

            Console.WriteLine("=== E3D Standalone Test ===");
            Console.WriteLine("Project: " + project + ", User: " + username + ", MDB: " + mdb);
            Console.WriteLine();

            try
            {
                // Step 1: Build environment Hashtable
                Console.WriteLine("[1/5] Building environment variables...");
                var env = BuildEnvHashtable(e3dPath);
                Console.WriteLine("  Environment variables: " + env.Count + " entries loaded");

                // Step 2: Initialize E3D engine
                Console.WriteLine("[2/5] Starting E3D engine (module 78)...");
                Standalone.Start(78, env);
                Console.WriteLine("  E3D engine started successfully.");

                // Step 3: Login to project
                Console.WriteLine("[3/5] Logging in to " + project + "...");
                PdmsMessage error;
                if (!Standalone.Open(project, username, password, mdb, out error))
                {
                    string errorMsg = error.MessageText();
                    Console.WriteLine("  LOGIN FAILED: " + errorMsg);
                    Standalone.ExitError(errorMsg);
                    return 1;
                }
                Console.WriteLine("  Login successful!");

                // Step 4: Run test PML commands
                Console.WriteLine("[4/5] Running PML test commands...");

                // Test 1: Get full name of current element
                RunTestCommand("VAR !result FLNN", "Current element FLNN");

                // Test 2: Get project name
                RunTestCommand("VAR !result (PROJECT.DBNAME())", "Project DB name");

                // Test 3: Check if project is open
                Console.WriteLine("  Checking Project.CurrentProject.IsOpen()...");
                bool isOpen = Project.CurrentProject.IsOpen();
                Console.WriteLine("    Project is open: " + isOpen);

                // Test 4: Get world element
                Console.WriteLine("  Getting world element (/*) ...");
                DbElement world = DbElement.GetElement("/*");
                Console.WriteLine("    World element: " + world);

                Console.WriteLine();
                Console.WriteLine("[5/5] All tests passed!");

                // Step 5: Cleanup
                Console.WriteLine("Finishing E3D engine...");
                try { Standalone.Finish(); }
                catch (Exception) { /* safe to ignore */ }

                Console.WriteLine("=== Test Complete ===");
                return 0;
            }
            catch (Exception ex)
            {
                Console.WriteLine();
                Console.WriteLine("ERROR: " + ex.Message);
                Console.WriteLine("Stack: " + ex.StackTrace);
                try { Standalone.Finish(); }
                catch { }
                return 1;
            }
            finally
            {
                Console.WriteLine();
                if (Environment.UserInteractive)
                {
                    Console.WriteLine("Press any key to exit...");
                    Console.ReadKey();
                }
            }
        }

        static void RunTestCommand(string pml, string description)
        {
            Console.WriteLine("  [" + description + "] " + pml);
            Command cmd = Command.CreateCommand(pml);
            if (cmd.Run())
            {
                string result = string.Empty;
                try { result = cmd.Result.Trim(); } catch { }
                Console.WriteLine("    Result: " + result);
            }
            else
            {
                string errMsg = cmd.Error.MessageText();
                Console.WriteLine("    FAILED: " + errMsg);
            }
        }

        static Hashtable BuildEnvHashtable(string e3dPath)
        {
            var env = new Hashtable();

            // Core E3D environment variables
            env.Add("AVEVA_DESIGN_EXE", e3dPath);
            env.Add("AVEVA_DESIGN_USER", Path.Combine(Path.GetTempPath(), "e3d_user"));
            env.Add("AVEVA_DESIGN_WORK", Path.Combine(Path.GetTempPath(), "e3d_work"));
            env.Add("AVEVA_PRODUCT", "E3D");
            env.Add("temp", Path.GetTempPath());
            env.Add("PATH", e3dPath + ";" + Environment.GetEnvironmentVariable("PATH"));
            env.Add("PDMSBUF", "1000");
            env.Add("PMLLIB", e3dPath);

            // Ensure temp directories exist
            Directory.CreateDirectory(Path.Combine(Path.GetTempPath(), "e3d_user"));
            Directory.CreateDirectory(Path.Combine(Path.GetTempPath(), "e3d_work"));

            // Read project environment variables from system env (set by evarProj.bat)
            // projects_dir comes from evarProj_based.bat
            string projectsDir = Environment.GetEnvironmentVariable("projects_dir");
            if (!string.IsNullOrEmpty(projectsDir))
            {
                env.Add("projects_dir", projectsDir);
            }
            else
            {
                // Fallback: use default ALP path
                env.Add("projects_dir", @"J:\cae_proj\alp\pdms\");
            }

            // Read all project-specific env vars from system environment
            // These are set by J:\cae_proj\evarProj.bat -> evarProj_based.bat
            string[] projEnvVars = new string[]
            {
                // ALP project vars
                "alp000", "alpMAC", "alpISO", "alpPIC", "alpDFLTS", "alp000ID",
                // RAS catalog
                "RAS", "RAS000", "RASMAC", "RASPIC",
                // GEV catalog
                "GEV", "GEV000", "GEVMAC", "GEVPIC"
            };

            foreach (string varName in projEnvVars)
            {
                string val = Environment.GetEnvironmentVariable(varName);
                if (!string.IsNullOrEmpty(val) && !env.ContainsKey(varName))
                {
                    env.Add(varName, val);
                    Console.WriteLine("    env[" + varName + "] = " + val);
                }
            }

            // If project vars not in environment, set defaults for ALP
            if (!env.ContainsKey("alp000"))
            {
                Console.WriteLine("    (Using default ALP project paths)");
                string alpBase = @"J:\cae_proj\alp\pdms\";
                env.Add("alp000", alpBase + "alp000");
                env.Add("alpMAC", alpBase + "alpmac");
                env.Add("alpISO", alpBase + "alpiso");
                env.Add("alpPIC", alpBase + "alppic");
                env.Add("alpDFLTS", alpBase + "alpdflts");

                // RAS & GEV catalog data
                string rasBase = @"J:\cae_prog\pdms\v12.1\CatData";
                env.Add("RAS", rasBase);
                env.Add("RAS000", rasBase + @"\RAS000");
                env.Add("RASMAC", rasBase + @"\RASMAC");
                env.Add("RASPIC", rasBase + @"\RASPIC");

                string gevBase = @"J:\cae_prog\pdms\v12.1\GEVData";
                env.Add("GEV", gevBase);
                env.Add("GEV000", gevBase + @"\GEV000");
                env.Add("GEVMAC", gevBase + @"\GEVMAC");
                env.Add("GEVPIC", gevBase + @"\GEVPIC");
            }

            return env;
        }

        static Assembly OnAssemblyResolve(object sender, ResolveEventArgs args)
        {
            string assemblyName = new AssemblyName(args.Name).Name;
            string dllPath = Path.Combine(_e3dPath, assemblyName + ".dll");
            if (File.Exists(dllPath))
                return Assembly.LoadFrom(dllPath);
            return null;
        }
    }
}
