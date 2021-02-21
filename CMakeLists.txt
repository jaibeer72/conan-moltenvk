cmake_minimum_required(VERSION 3.1)
project(MoltenVK)

include(conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

# PIC required for objects targets linked into shared MoltenVK
if(BUILD_SHARED_LIBS)
    set(CMAKE_POSITION_INDEPENDENT_CODE ON)
endif()

# Required Apple Frameworks
find_library(CORE_FOUNDATION_FRAMEWORK CoreFoundation)
find_library(CORE_GRAPHICS_FRAMEWORK CoreGraphics)
find_library(QUARTZ_CORE_FRAMEWORK QuartzCore)
find_library(FOUNDATION_FRAMEWORK Foundation)
find_library(IOKIT_FRAMEWORK IOKit)
find_library(APPKIT_FRAMEWORK AppKit)
find_library(IOSURFACE_FRAMEWORK IOSurface)
find_library(METAL_FRAMEWORK Metal)

set(PROJECT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder)

# MoltenVKCommon
# * direct dependencies:
#   - external: None
#   - internal: None
#   - frameworks: Foundation)
file(GLOB MVK_COMMON_SOURCES ${PROJECT_DIR}/common/*.mm)
add_library(MoltenVKCommon OBJECT ${MVK_COMMON_SOURCES})

# MoltenVKShaderConverter
# * direct dependencies:
#   - external: spirv-cross, spirv-tools and glslang
#   - internal: MoltenVKCommon
#   - frameworks: Foundation
file(GLOB MVK_SC_SOURCES
    ${PROJECT_DIR}/MoltenVKShaderConverter/common/*.cpp
    ${PROJECT_DIR}/MoltenVKShaderConverter/MoltenVKShaderConverter/*.cpp
    ${PROJECT_DIR}/MoltenVKShaderConverter/MoltenVKShaderConverter/*.mm
)
add_library(MoltenVKShaderConverter OBJECT ${MVK_SC_SOURCES})
target_include_directories(MoltenVKShaderConverter PUBLIC
    ${PROJECT_DIR}/common
    ${PROJECT_DIR}/MoltenVKShaderConverter/common
)

# MoltenVKShaderConverterTool
# * direct dependencies:
#   - external: None
#   - internal: MoltenVKShaderConverter and MoltenVKCommon
#   - frameworks: Foundation and Metal
file(GLOB MVK_SCT_SOURCES
    ${PROJECT_DIR}/MoltenVKShaderConverter/MoltenVKShaderConverterTool/*.cpp
    ${PROJECT_DIR}/MoltenVKShaderConverter/MoltenVKShaderConverterTool/*.mm
)
add_executable(MoltenVKShaderConverterTool ${MVK_SCT_SOURCES})
target_include_directories(MoltenVKShaderConverterTool PRIVATE
    ${PROJECT_DIR}/MoltenVKShaderConverter/MoltenVKShaderConverter
)
target_link_libraries(MoltenVKShaderConverterTool PRIVATE
    MoltenVKCommon
    MoltenVKShaderConverter
    ${CONAN_LIBS}
    ${FOUNDATION_FRAMEWORK}
    ${METAL_FRAMEWORK}
)

# MoltenVK
# * direct dependencies:
#   - external: cereal, spirv-cross and vulkan-headers
#   - internal: MoltenVKShaderConverter and MoltenVKCommon
#   - frameworks: CoreFoundation, CoreGraphics, QuartzCore, Foundation, IOKit, AppKit, IOSurface and Metal (TBC)
file(GLOB_RECURSE MVK_SOURCES
    ${PROJECT_DIR}/MoltenVK/*.m
    ${PROJECT_DIR}/MoltenVK/*.mm
    ${PROJECT_DIR}/MoltenVK/*.cpp
)
add_library(MoltenVK ${MVK_SOURCES})
target_include_directories(MoltenVK PRIVATE
    ${PROJECT_DIR}/Common
    ${PROJECT_DIR}/MoltenVKShaderConverter
    ${PROJECT_DIR}/MoltenVK/MoltenVK/API
    ${PROJECT_DIR}/MoltenVK/MoltenVK/Commands
    ${PROJECT_DIR}/MoltenVK/MoltenVK/GPUObjects
    ${PROJECT_DIR}/MoltenVK/MoltenVK/Layers
    ${PROJECT_DIR}/MoltenVK/MoltenVK/OS
    ${PROJECT_DIR}/MoltenVK/MoltenVK/Utility
    ${PROJECT_DIR}/MoltenVK/MoltenVK/Vulkan
)
target_link_libraries(MoltenVK PRIVATE
    MoltenVKCommon
    MoltenVKShaderConverter
    ${CONAN_LIBS}
    ${CORE_FOUNDATION_FRAMEWORK}
    ${CORE_GRAPHICS_FRAMEWORK}
    ${QUARTZ_CORE_FRAMEWORK}
    ${FOUNDATION_FRAMEWORK}
    ${IOKIT_FRAMEWORK}
    ${APPKIT_FRAMEWORK}
    ${IOSURFACE_FRAMEWORK}
    ${METAL_FRAMEWORK}
)

install(
    TARGETS MoltenVK MoltenVKShaderConverterTool
    BUNDLE DESTINATION ${CMAKE_INSTALL_BINDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

file(GLOB MVK_PUBLIC_HEADERS ${PROJECT_DIR}/MoltenVK/MoltenVK/API/*.h)
install(
    FILES ${MVK_PUBLIC_HEADERS}
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/MoltenVK
)

file(GLOB MVK_SCT_PUBLIC_HEADERS
    ${PROJECT_DIR}/MoltenVKShaderConverter/MoltenVKShaderConverter/*Conversion.h
    ${PROJECT_DIR}/MoltenVKShaderConverter/MoltenVKShaderConverter/*Converter.h
)
install(
    FILES ${MVK_SCT_PUBLIC_HEADERS}
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/MoltenVKShaderConverter
)
