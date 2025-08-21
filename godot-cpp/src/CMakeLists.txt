cmake_minimum_required(VERSION 3.30)
project(godot-cpp)

if (WIN32)
	set(OS_SUFFIX "windows")
	set(LIB_SUFFIX ".lib")
elseif (APPLE)
	set(OS_SUFFIX "osx")
	set(LIB_SUFFIX ".a")
elseif (UNIX)
	set(OS_SUFFIX "linux")
	set(LIB_SUFFIX ".a")
else()
	message(FATAL_ERROR "Unsupported platform for godot-cpp")
endif()

set(godot-cpp_RELEASE_LIB "${CMAKE_INSTALL_PREFIX}/lib/libgodot-cpp.${OS_SUFFIX}.release.64${LIB_SUFFIX}")
set(godot-cpp_DEBUG_LIB   "${CMAKE_INSTALL_PREFIX}/lib/libgodot-cpp.${OS_SUFFIX}.debug.64${LIB_SUFFIX}")

include(CMakePackageConfigHelpers)

configure_package_config_file(
	"${CMAKE_CURRENT_SOURCE_DIR}/godot-cppConfig.cmake.in"
	"${CMAKE_CURRENT_BINARY_DIR}/godot-cppConfig.cmake"
	INSTALL_DESTINATION cmake/godot-cpp
)

write_basic_package_version_file(
	"${CMAKE_CURRENT_BINARY_DIR}/godot-cppConfigVersion.cmake"
	VERSION 3.5
	COMPATIBILITY AnyNewerVersion
)

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bin/"
		DESTINATION lib
		FILES_MATCHING
			PATTERN "libgodot-cpp.*.lib"
			PATTERN "libgodot-cpp.*.a"
)

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/include/"
		DESTINATION include/godot-cpp
		FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp"
)

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/godot-headers/"
		DESTINATION include/godot-cpp/godot-headers
		FILES_MATCHING PATTERN "*.h"
)

install(FILES
	"${CMAKE_CURRENT_BINARY_DIR}/godot-cppConfig.cmake"
	"${CMAKE_CURRENT_BINARY_DIR}/godot-cppConfigVersion.cmake"
	DESTINATION lib/cmake/godot-cpp
)