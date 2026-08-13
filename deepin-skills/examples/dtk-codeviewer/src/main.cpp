#include <DApplication>
#include <DIconTheme>
#include <DLog>
#include <QApplication>
#include <QCoreApplication>
#include <QLoggingCategory>

#include "mainwindow.h"

DWIDGET_USE_NAMESPACE
DCORE_USE_NAMESPACE
DGUI_USE_NAMESPACE

Q_LOGGING_CATEGORY(lcApplicationMain, "org.deepin.dtk.codeviewer.application")

namespace {
constexpr auto kApplicationId = "org.deepin.dtk.codeviewer";
constexpr auto kApplicationIconName = "dtk-codeviewer";

QIcon applicationIcon()
{
    return DIconTheme::findQIcon(
        QString::fromLatin1(kApplicationIconName),
        QIcon::fromTheme(QStringLiteral("application-x-executable")),
        DIconTheme::DontFallbackToQIconFromTheme);
}
}

int main(int argc, char *argv[])
{
    // DSGApplication 会在 DTK 静态初始化阶段读取 appId，必须早于 DApplication。
    qputenv("DSG_APP_ID", QByteArray(kApplicationId));

    // Must be called before creating QGuiApplication instance
    QApplication::setHighDpiScaleFactorRoundingPolicy(Qt::HighDpiScaleFactorRoundingPolicy::PassThrough);

    QCoreApplication::setOrganizationName(QStringLiteral("deepin"));
    QCoreApplication::setOrganizationDomain(QStringLiteral("deepin.org"));
    QCoreApplication::setApplicationName(QStringLiteral("dtk-codeviewer"));
    QCoreApplication::setApplicationVersion(QString::fromLatin1(DTK_CODEVIEWER_VERSION));
    QGuiApplication::setDesktopFileName(QString::fromLatin1(kApplicationId));

    DApplication a(argc, argv);
    a.loadTranslator();

    a.setProductName(QObject::tr("DTK Code Viewer"));
    const QIcon appIcon = applicationIcon();
    a.setWindowIcon(appIcon);
    a.setProductIcon(appIcon);
    a.setApplicationDescription(QObject::tr("A code file viewer built with DTK framework."));
    a.setApplicationHomePage(QStringLiteral("https://github.com/linuxdeepin/dtk-codeviewer"));
    a.setApplicationLicense(QStringLiteral("GPLv3"));

    DLogManager::registerConsoleAppender();
    DLogManager::registerFileAppender();

    if (!a.setSingleInstance(QString::fromLatin1(kApplicationId))) {
        qCWarning(lcApplicationMain) << "Another instance is already running";
        return 0;
    }

    qCInfo(lcApplicationMain) << "Application started"
                              << "version" << QCoreApplication::applicationVersion()
                              << "logFile" << DLogManager::getlogFilePath();

    MainWindow w;
    QObject::connect(&a, &DApplication::newInstanceStarted, &w, [&w] {
        Qt::WindowStates states = w.windowState();
        if (states.testFlag(Qt::WindowMinimized)) {
            states.setFlag(Qt::WindowMinimized, false);
            w.setWindowState(states);
        }

        w.show();
        w.raise();
        w.activateWindow();
        qCInfo(lcApplicationMain) << "Main window activated by a new instance request";
    });
    w.show();

    const int result = a.exec();
    qCInfo(lcApplicationMain) << "Application exited with code" << result;
    return result;
}
