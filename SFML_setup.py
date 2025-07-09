import os
import subprocess
import textwrap
from pathlib import Path
import shutil
import platform
import sys

# Platform check
if os.name != "nt":
    print("This script is currently only compatible with Windows (Visual Studio).")
    sys.exit(1)

# ---------------------------------------------------------------------------
# validation: if cmake is in PATH
# ---------------------------------------------------------------------------
if shutil.which("cmake") is None:
    print("CMake is not installed or not in your system PATH.")
    print("Download from: https://cmake.org/download/")
    sys.exit(1)

# Asking for Directory
folder_name = input("Enter the project name: ").strip()
target_path = Path(input("Enter the full path where you want to create the project (e.g., C:/Users/HP/Desktop): ").strip())
sfml_root = Path(input("Enter the SFML root folder (e.g., C:/SFML-2.6.0): ").strip().rstrip("\\/"))

sfml_bin = sfml_root / "bin"
sfml_cmake = sfml_root / "lib" / "cmake" / "SFML"

if not sfml_bin.exists() or not sfml_cmake.exists():
    print(f"Error! Could not find SFML in: {sfml_root}")
    sys.exit(1)

# derived paths
base_project_path = (target_path / folder_name).resolve()
src_path   = base_project_path / "src"
build_path = base_project_path / "build"
include_path = base_project_path / "include"
main_cpp_path = src_path / "main.cpp"

# Making directories
for p in (src_path, build_path, include_path):
    p.mkdir(parents=True, exist_ok=True)


if not main_cpp_path.exists():
    main_cpp_path.write_text(textwrap.dedent("""
        #include <SFML/Graphics.hpp>

        int main() {
            sf::RenderWindow window(sf::VideoMode(800, 600), "My SFML Window");
            while (window.isOpen()) {
                sf::Event event;
                while (window.pollEvent(event)) {
                    if (event.type == sf::Event::Closed)
                        window.close();
                }
                window.clear();
                window.display();
            }
            return 0;
        }
        """))
    print(f"Created main.cpp inside src/.")

# Creating CMakeLists.txt with SFML paths
sfml_bin_str = str(sfml_bin).replace('\\', '/')     # Windows directory structure
sfml_cmake_str = str(sfml_cmake).replace('\\', '/')

cmake_code = textwrap.dedent(f"""
    cmake_minimum_required(VERSION 3.10)
    project("{folder_name}")
    set(CMAKE_CXX_STANDARD 17)

    set(SFML_DIR "{sfml_cmake_str}")

    find_package(SFML REQUIRED COMPONENTS graphics window system audio)

    file(GLOB SFML_DLLS "{sfml_bin_str}/*.dll")
    foreach(DLL ${{SFML_DLLS}})
        configure_file(${{DLL}} ${{CMAKE_CURRENT_BINARY_DIR}} COPYONLY)
    endforeach()

    include_directories(include)
    add_executable({folder_name} src/main.cpp)
    target_link_libraries({folder_name} sfml-graphics sfml-window sfml-system sfml-audio)
    """)

(base_project_path / "CMakeLists.txt").write_text(cmake_code)
print("CMakeLists.txt generated.")

# Running CMake to produce the Visual Studio solution
print("Running CMake to generate Visual Studio solution…\n")
subprocess.run([
    "cmake",
    "-G", "Visual Studio 17 2022",   #    for VS17 
    f"-DSFML_DIR={sfml_cmake_str}",
    "..",
], cwd=build_path, check=True)



solution_file = build_path / f"{folder_name}.sln"
if solution_file.exists():
    print("Opening solution in Visual Studio…")
    os.startfile(solution_file)
    print(f"Project has been created. In the Solution Explorer, set {folder_name} as \"StartUp Project\" and run it.")
