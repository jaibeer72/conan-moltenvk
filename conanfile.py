from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
import os


class MoltenVKConan(ConanFile):
    name = "moltenvk"
    description = "MoltenVK is a Vulkan Portability implementation. It " \
                  "layers a subset of the high-performance, industry-standard " \
                  "Vulkan graphics and compute API over Apple's Metal " \
                  "graphics framework, enabling Vulkan applications to run " \
                  "on iOS and macOS. "
    license = "Apache-2.0"
    topics = ("conan", "moltenvk", "khronos", "vulkan", "metal")
    homepage = "https://github.com/KhronosGroup/MoltenVK"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        if not tools.is_apple_os(self.settings.os):
            raise ConanInvalidConfiguration("MoltenVK only supported on MacOS, iOS and tvOS")

    def requirements(self):
        self.requires("cereal/1.3.0")
        self.requires("glslang/8.13.3559")
        self.requires("spirv-cross/20210115")
        self.requires("spirv-headers/1.5.4")
        self.requires("spirv-tools/v2020.5")
        self.requires("vulkan-headers/1.2.162.0")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("MoltenVK-" + self.version, self._source_subfolder)

    def build(self):
        # TODO
        pass

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        # TODO

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs()
