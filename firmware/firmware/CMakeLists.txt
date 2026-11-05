# CMakeList.txt: firmware için CMake projesi, kaynağı ekleyin ve tanımlayın
# projeye özgü mantık burada bulunur.
#
# Kaynağı bu projenin yürütülebilir dosyasına ekleyin.

# Kaynak dosyaları ekleyin
add_executable(firmware
    firmware.cpp
    src/motor.cpp
    src/esc.cpp
    src/controller.cpp
    src/safety_manager.cpp
    src/main.cpp
)

set_property(TARGET firmware PROPERTY CXX_STANDARD 20)

# Include dizinleri
target_include_directories(firmware
    PRIVATE
        .
        src
)

# Derleyici seçenekleri
if (MSVC)
    target_compile_options(firmware PRIVATE /W4 /WX)
else()
    target_compile_options(firmware PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

# Testleri ve yükleme hedefleri (opsiyonel)
enable_testing()
add_test(NAME firmware_test COMMAND firmware)