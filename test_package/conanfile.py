from conans import ConanFile, CMake
import os


channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "geotrac")


class JanssonTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "libjansson/2.10-togs1@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        if self.settings.arch == "x86":
            cmake = CMake(self)
            # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
            cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
            cmake.build()
        else:
            pass

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        if self.settings.arch == "x86":
            os.chdir("bin")
            self.run(".%sexample" % os.sep)
        else:
            pass
