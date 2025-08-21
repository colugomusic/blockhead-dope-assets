cmake_minimum_required(VERSION 3.30)
project(madronalib)
add_library(madronalib INTERFACE)
add_library(madronalib::madronalib ALIAS madronalib)
target_sources(madronalib PUBLIC
	FILE_SET HEADERS
	BASE_DIRS
		external/sse2neon
		source
	FILES
		external/sse2neon/sse2neon.h
		source/DSP/MLDSPBuffer.h
		source/DSP/MLDSPFilters.h
		source/DSP/MLDSPFunctional.h
		source/DSP/MLDSPGens.h
		source/DSP/MLDSPMath.h
		source/DSP/MLDSPMathNEON.h
		source/DSP/MLDSPMathSSE.h
		source/DSP/MLDSPOps.h
		source/DSP/MLDSPProjections.h
		source/DSP/MLDSPRatio.h
		source/DSP/MLDSPRouting.h
		source/DSP/MLDSPSample.h
		source/DSP/MLDSPScalarMath.h
		source/DSP/MLDSPScale.h
		source/DSP/MLDSPUtils.h
)
install(
	TARGETS madronalib
	EXPORT madronalib
	FILE_SET HEADERS
)
install(EXPORT madronalib
    FILE madronalibConfig.cmake
    NAMESPACE madronalib::
    DESTINATION lib/cmake/madronalib
)