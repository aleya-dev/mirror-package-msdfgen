from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import rmdir
import os


required_conan_version = ">=2.0"


class MsdfGenConan(ConanFile):
    name = "msdfgen"
    version = "1.12"
    python_requires = "aleya-conan-base/1.3.0@aleya/public"
    python_requires_extend = "aleya-conan-base.AleyaConanBase"

    exports_sources = "source/*"

    options = {
        "shared": [False, True],
        "fPIC": [False, True]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    requires = ["libpng/1.6.40@aleya/public", "freetype/2.13.2@aleya/public"]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["MSDFGEN_BUILD_STANDALONE"] = False
        tc.variables["MSDFGEN_USE_VCPKG"] = False
        tc.variables["MSDFGEN_USE_SKIA"] = False
        tc.variables["MSDFGEN_INSTALL"] = True
        tc.variables["MSDFGEN_DYNAMIC_RUNTIME"] = True
        tc.variables["MSDFGEN_DISABLE_SVG"] = True
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "msdfgen")

        self.cpp_info.components["libmsdfgen-core"].libs = ["msdfgen-core"]
        self.cpp_info.components["libmsdfgen-core"].set_property("cmake_target_name", "msdfgen::core")
        self.cpp_info.components["libmsdfgen-core"].includedirs = ["include/msdfgen"]

        self.cpp_info.components["libmsdfgen-ext"].libs = ["msdfgen-ext"]
        self.cpp_info.components["libmsdfgen-ext"].set_property("cmake_target_name", "msdfgen::ext")
        self.cpp_info.components["libmsdfgen-ext"].includedirs = ["include/msdfgen"]
        self.cpp_info.components["libmsdfgen-ext"].requires = \
            ["libmsdfgen-core", "libpng::libpng", "freetype::freetype"]
