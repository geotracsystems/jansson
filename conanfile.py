import os
from conans import ConanFile, CMake, tools


class JanssonConan(ConanFile):
    name = "libjansson"
    description = "jansson C JSON parsing library"
    version = "2.10-togs1"
    license = "MIT"
    url = "https://github.com/geotracsystems/jansson"
    settings = "os", "compiler", "build_type", "arch"
    options = {"no_documentation": [True, False], "shared": [True, False]}
    default_options = "no_documentation=True", "shared=False"
    generators = "cmake"
    exports_sources = "*"

    def build(self):
        cmake = CMake(self)
        no_documentation = "-DJANSSON_BUILD_DOCS=OFF" if self.options.no_documentation else ""
        shared = "-DJANSSON_BUILD_SHARED_LIBS=ON" if self.options.shared else ""
        install_dir = "-DCMAKE_INSTALL_PREFIX=%s" % self.package_folder
        if self.settings.arch == "armv7":
            os.environ["CFLAGS"] = "-lm"
        elif self.settings.arch == "x86":
            os.environ["CFLAGS"] = "-m32"
        os.environ["CFLAGS"] += " -g"
        self.run('cmake ./ %s %s %s %s' % (cmake.command_line, no_documentation, shared, install_dir))
        self.run("cmake --build . %s" % cmake.build_config)
        # Run tests on the host platform
        if self.settings.arch == "x86":
            self.run("make check")
        self.run("make install")

    def package_info(self):
        self.cpp_info.libs = ["jansson"]
