cmake_minimum_required(VERSION 3.13)
if(POLICY CMP0177)
    cmake_policy(SET CMP0177 NEW)
endif()
project(dtk-codeviewer VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(GNUInstallDirs)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets LinguistTools)
find_package(Dtk6Core REQUIRED)
find_package(Dtk6Gui REQUIRED)
find_package(Dtk6Widget REQUIRED)

add_executable(dtk-codeviewer
    src/main.cpp
    src/mainwindow.cpp
    src/tabmanager.cpp
    src/codeview.cpp
    resources/icons.qrc
)

target_compile_definitions(dtk-codeviewer PRIVATE
    DTK_CODEVIEWER_VERSION="${PROJECT_VERSION}"
)

target_link_libraries(dtk-codeviewer PRIVATE
    Qt6::Core
    Qt6::Widgets
    Dtk6::Core
    Dtk6::Gui
    Dtk6::Widget
)

set(DTK_CODEVIEWER_TS_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/translations/dtk-codeviewer_en.ts
    ${CMAKE_CURRENT_SOURCE_DIR}/translations/dtk-codeviewer_zh_CN.ts
)
set_source_files_properties(${DTK_CODEVIEWER_TS_FILES}
    PROPERTIES OUTPUT_LOCATION ${CMAKE_CURRENT_BINARY_DIR}/translations
)
qt_add_translations(
    TARGETS dtk-codeviewer
    SOURCE_TARGETS dtk-codeviewer
    TS_FILES ${DTK_CODEVIEWER_TS_FILES}
    QM_FILES_OUTPUT_VARIABLE DTK_CODEVIEWER_QM_FILES
)

install(TARGETS dtk-codeviewer
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(FILES data/org.deepin.dtk.codeviewer.desktop
    DESTINATION ${CMAKE_INSTALL_DATADIR}/applications
)

# DIconTheme searches this directory by default for application DCI icons.
install(FILES resources/icons/dtk-codeviewer.dci
    DESTINATION ${CMAKE_INSTALL_DATADIR}/dsg/icons
)

install(FILES ${DTK_CODEVIEWER_QM_FILES}
    DESTINATION ${CMAKE_INSTALL_DATADIR}/dtk-codeviewer/translations
)

dtk_add_config_meta_files(
    APPID org.deepin.dtk.codeviewer
    FILES ${CMAKE_CURRENT_SOURCE_DIR}/configs/org.deepin.dtk.codeviewer.json
)
