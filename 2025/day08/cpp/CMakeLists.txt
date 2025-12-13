cmake_minimum_required(VERSION 3.16)
project(day08 LANGUAGES CXX)

# Use clang-cl (MSVC-compatible driver)
set(CMAKE_CXX_COMPILER clang-cl)

# C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Single-config output layout for Ninja: put build artifacts under build/<CONFIG>
if(NOT CMAKE_CONFIGURATION_TYPES)
  if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
  endif()

  string(TOUPPER "${CMAKE_BUILD_TYPE}" _BUILD_TYPE_UPPER)
  set(_out_dir "${CMAKE_BINARY_DIR}/${CMAKE_BUILD_TYPE}")

  set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${_out_dir})
  set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${_out_dir})
  set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${_out_dir})
endif()

# Export compile commands for tools like clang-tidy/clangd
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Default to Debug for single-config generators unless the user set a build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()

# Compiler flags: enable common warnings; ensure debug symbols are emitted
if(MSVC)
    # MSVC / clang-cl flags
    add_compile_options(/W4 /permissive- /EHsc)
    if(CMAKE_BUILD_TYPE STREQUAL "Debug")
        add_compile_options(/Zi)
        # Tell the linker to produce a PDB for the executable
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /DEBUG")
    endif()
else()
    # gcc/clang (clang++ driver)
    add_compile_options(-Wall -Wextra -Wpedantic)
    if(CMAKE_BUILD_TYPE STREQUAL "Debug")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
    endif()
endif()

add_executable(day08
        day08.cpp
)