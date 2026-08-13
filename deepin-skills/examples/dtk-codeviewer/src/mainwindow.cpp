#include "mainwindow.h"

#include <DApplication>
#include <DTitlebar>
#include <DMessageManager>
#include <DFileDialog>
#include <DGuiApplicationHelper>
#include <DIconTheme>
#include <DHorizontalLine>
#include <DPalette>
#include <DPlatformTheme>
#include <DWindowManagerHelper>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QCoreApplication>
#include <QIcon>
#include <QLoggingCategory>
#include <QPainter>
#include <QResizeEvent>
#include <QTimer>

DWIDGET_USE_NAMESPACE
DGUI_USE_NAMESPACE
DCORE_USE_NAMESPACE

Q_LOGGING_CATEGORY(lcApplicationWindow, "org.deepin.dtk.codeviewer.application")
Q_LOGGING_CATEGORY(lcConfiguration, "org.deepin.dtk.codeviewer.configuration")
Q_LOGGING_CATEGORY(lcFileLoadWindow, "org.deepin.dtk.codeviewer.fileload")

namespace {
constexpr auto kApplicationId = "org.deepin.dtk.codeviewer";
constexpr auto kConfigName = "org.deepin.dtk.codeviewer";
constexpr auto kApplicationIconName = "dtk-codeviewer";
constexpr int kDefaultWidth = 1000;
constexpr int kDefaultHeight = 700;
constexpr int kDefaultFontSize = 14;
constexpr int kDefaultOpacity = 80;
constexpr int kMaximumWindowWidth = 8192;
constexpr int kMaximumWindowHeight = 4320;
constexpr int kFileReadProgressMaximum = 50;

QIcon applicationIcon()
{
    return DIconTheme::findQIcon(
        QString::fromLatin1(kApplicationIconName),
        QIcon::fromTheme(QStringLiteral("application-x-executable")),
        DIconTheme::DontFallbackToQIconFromTheme);
}
}

class FallbackSurface : public QWidget
{
public:
    explicit FallbackSurface(QWidget *parent = nullptr)
        : QWidget(parent)
        , m_radius(8)
    {
        setAttribute(Qt::WA_TransparentForMouseEvents);
        setAttribute(Qt::WA_TranslucentBackground);
        setAutoFillBackground(false);
    }

    void setSurface(const QColor &color, int radius)
    {
        m_color = color;
        m_radius = qMax(0, radius);
        update();
    }

protected:
    void paintEvent(QPaintEvent *) override
    {
        QPainter painter(this);
        painter.setRenderHint(QPainter::Antialiasing);
        painter.setPen(Qt::NoPen);
        painter.setBrush(m_color);
        painter.drawRoundedRect(rect(), m_radius, m_radius);
    }

private:
    QColor m_color;
    int m_radius;
};

MainWindow::MainWindow(QWidget *parent)
    : DMainWindow(parent)
    , m_tabBar(nullptr)
    , m_codeView(nullptr)
    , m_backgroundSurface(nullptr)
    , m_fallbackSurface(nullptr)
    , m_windowBlur(nullptr)
    , m_spinFont(nullptr)
    , m_sliderOpacity(nullptr)
    , m_tabManager(nullptr)
    , m_statusLabel(nullptr)
    , m_opacityLabel(nullptr)
    , m_fontIcon(nullptr)
    , m_loadProgress(nullptr)
    , m_config(nullptr)
    , m_fileLoading(false)
    , m_contentLoading(false)
    , m_contentContinuesFileLoad(false)
    , m_updatingConfig(false)
    , m_configAvailable(false)
{
    setAttribute(Qt::WA_TranslucentBackground);
    setAutoFillBackground(false);
    setTranslucentBackground(true);
    setEnableBlurWindow(true);

    setupUI();
    setupTitlebar();
    setupConnections();
    setupConfig();
    restoreWindowState();

    qCInfo(lcApplicationWindow) << "Main window initialized";
}

MainWindow::~MainWindow()
{
    saveWindowState();
}

void MainWindow::setupUI()
{
    setMinimumSize(800, 500);
    resize(kDefaultWidth, kDefaultHeight);

    // 使用一个覆盖整个窗口的模糊层，标题栏和内容区共享同一模糊源与遮罩。
    m_fallbackSurface = new FallbackSurface(this);
    m_fallbackSurface->setGeometry(rect());
    m_fallbackSurface->hide();
    m_fallbackSurface->lower();

    m_windowBlur = new DBlurEffectWidget(this);
    m_windowBlur->setBlendMode(DBlurEffectWidget::BehindWindowBlend);
    m_windowBlur->setMaskColor(DBlurEffectWidget::AutoColor);
    m_windowBlur->setAttribute(Qt::WA_TransparentForMouseEvents);
    m_windowBlur->setGeometry(rect());
    m_windowBlur->show();
    m_windowBlur->lower();

    m_backgroundSurface = new QWidget(this);
    m_backgroundSurface->setAttribute(Qt::WA_TranslucentBackground);
    m_backgroundSurface->setAutoFillBackground(false);
    m_backgroundSurface->setBackgroundRole(QPalette::NoRole);
    QVBoxLayout *mainLayout = new QVBoxLayout(m_backgroundSurface);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(0);

    // 标签栏
    m_tabBar = new DTabBar(this);
    m_tabBar->setTabsClosable(true);
    m_tabBar->setMovable(true);
    m_tabBar->setExpanding(false);
    m_tabBar->setVisibleAddButton(true);
    m_tabBar->setAttribute(Qt::WA_TranslucentBackground);
    m_tabBar->setAutoFillBackground(false);
    mainLayout->addWidget(m_tabBar);

    // Tab 管理器
    m_tabManager = new TabManager(m_tabBar, this);

    // 代码视图与居中的 DTK 水波加载提示
    QWidget *codeContainer = new QWidget(this);
    codeContainer->setAttribute(Qt::WA_TranslucentBackground);
    codeContainer->setAutoFillBackground(false);
    QGridLayout *codeLayout = new QGridLayout(codeContainer);
    codeLayout->setContentsMargins(0, 0, 0, 0);
    codeLayout->setSpacing(0);

    m_codeView = new CodeView(codeContainer);
    // 编辑器自身不再叠加独立底色，直接透出与标题栏共用的窗口模糊背景。
    m_codeView->setBackgroundOpacity(0);
    codeLayout->addWidget(m_codeView, 0, 0);

    m_loadProgress = new DWaterProgress(codeContainer);
    m_loadProgress->setFixedSize(72, 72);
    m_loadProgress->setValue(0);
    m_loadProgress->setTextVisible(true);
    m_loadProgress->setAttribute(Qt::WA_TransparentForMouseEvents);
    m_loadProgress->hide();
    codeLayout->addWidget(m_loadProgress, 0, 0, Qt::AlignCenter);

    mainLayout->addWidget(codeContainer, 1);

    // 分隔
    DHorizontalLine *sep = new DHorizontalLine(this);
    mainLayout->addWidget(sep);

    // 字体与编辑区背景透明度调节栏
    QHBoxLayout *viewOptionsLayout = new QHBoxLayout();
    viewOptionsLayout->setContentsMargins(8, 4, 8, 4);
    viewOptionsLayout->setSpacing(8);

    m_fontIcon = new DLabel(this);
    m_fontIcon->setFixedSize(16, 16);
    viewOptionsLayout->addWidget(m_fontIcon);

    m_spinFont = new DSpinBox(this);
    m_spinFont->setRange(10, 24);
    m_spinFont->setSingleStep(1);
    m_spinFont->setValue(14);
    m_spinFont->setSuffix(QStringLiteral(" px"));
    m_spinFont->setFixedWidth(100);
    m_spinFont->setToolTip(tr("Editor font size"));
    viewOptionsLayout->addWidget(m_spinFont);

    viewOptionsLayout->addSpacing(16);

    DLabel *opacityTitle = new DLabel(tr("Opacity"), this);
    opacityTitle->setToolTip(tr("Window blur background opacity"));
    DFontSizeManager::instance()->bind(opacityTitle, DFontSizeManager::T7);
    viewOptionsLayout->addWidget(opacityTitle);

    m_sliderOpacity = new DSlider(Qt::Horizontal, this);
    m_sliderOpacity->setMinimum(0);
    m_sliderOpacity->setMaximum(100);
    m_sliderOpacity->setValue(80);
    m_sliderOpacity->setFixedWidth(160);
    m_sliderOpacity->setToolTip(tr("Window blur background opacity"));
    viewOptionsLayout->addWidget(m_sliderOpacity);

    m_opacityLabel = new DLabel(tr("%1%").arg(kDefaultOpacity), this);
    m_opacityLabel->setFixedWidth(44);
    viewOptionsLayout->addWidget(m_opacityLabel);

    viewOptionsLayout->addStretch();
    mainLayout->addLayout(viewOptionsLayout);

    // 状态栏
    DHorizontalLine *sep2 = new DHorizontalLine(this);
    mainLayout->addWidget(sep2);

    QHBoxLayout *statusLayout = new QHBoxLayout();
    statusLayout->setContentsMargins(8, 4, 8, 4);
    statusLayout->setSpacing(8);

    m_statusLabel = new DLabel(tr("No file opened"), this);
    m_statusLabel->setForegroundRole(DPalette::TextTips);
    m_statusLabel->setElideMode(Qt::ElideMiddle);
    statusLayout->addWidget(m_statusLabel, 1);

    mainLayout->addLayout(statusLayout);
    setCentralWidget(m_backgroundSurface);

    // 字体绑定
    DFontSizeManager::instance()->bind(m_tabBar, DFontSizeManager::T6);
    DFontSizeManager::instance()->bind(m_opacityLabel, DFontSizeManager::T7);
    DFontSizeManager::instance()->bind(m_statusLabel, DFontSizeManager::T8);

    refreshThemeIcons();
    updateWindowEffects();
}

void MainWindow::setupConnections()
{
    connect(m_tabBar, &DTabBar::tabAddRequested, this, &MainWindow::onOpenFile);

    connect(m_tabManager, &TabManager::tabChanged, this, &MainWindow::onTabChanged);
    connect(m_tabManager, &TabManager::tabsEmpty, this, &MainWindow::onTabsEmpty);
    connect(m_tabManager, &TabManager::fileLoadStarted,
            this, &MainWindow::onFileLoadStarted);
    connect(m_tabManager, &TabManager::fileLoadProgress,
            this, &MainWindow::onFileLoadProgress);
    connect(m_tabManager, &TabManager::fileOpened,
            this, &MainWindow::onFileOpened);
    connect(m_tabManager, &TabManager::fileOpenFailed,
            this, &MainWindow::onFileOpenFailed);
    connect(m_tabManager, &TabManager::fileLoadFinished,
            this, &MainWindow::onFileLoadFinished);
    connect(m_codeView, &CodeView::contentLoadStarted,
            this, &MainWindow::onContentLoadStarted);
    connect(m_codeView, &CodeView::contentLoadProgress,
            this, &MainWindow::onContentLoadProgress);
    connect(m_codeView, &CodeView::contentLoadFinished,
            this, &MainWindow::onContentLoadFinished);

    connect(m_spinFont, QOverload<int>::of(&DSpinBox::valueChanged),
            this, &MainWindow::onFontSizeChanged);
    connect(m_sliderOpacity, &DSlider::valueChanged, this, &MainWindow::onOpacityChanged);

    auto *guiHelper = DGuiApplicationHelper::instance();
    connect(guiHelper, &DGuiApplicationHelper::themeTypeChanged,
            this, [this] {
                refreshThemeIcons();
                updateWindowEffects();
            });
    connect(guiHelper, &DGuiApplicationHelper::applicationPaletteChanged,
            this, &MainWindow::updateWindowEffects);

    if (DPlatformTheme *theme = guiHelper->applicationTheme()) {
        connect(theme, &DPlatformTheme::windowRadiusChanged,
                this, &MainWindow::updateWindowEffects);
    }

    auto *windowManager = DWindowManagerHelper::instance();
    connect(windowManager, &DWindowManagerHelper::hasBlurWindowChanged,
            this, &MainWindow::updateWindowEffects);
    connect(windowManager, &DWindowManagerHelper::hasCompositeChanged,
            this, &MainWindow::updateWindowEffects);

    if (auto *application = qobject_cast<DApplication *>(QCoreApplication::instance())) {
        connect(application, &DApplication::iconThemeChanged,
                this, &MainWindow::refreshThemeIcons);
    }
}

void MainWindow::setupTitlebar()
{
    DTitlebar *tb = titlebar();
    tb->setTitle(tr("DTK Code Viewer"));
    tb->setIcon(applicationIcon());
    tb->setSwitchThemeMenuVisible(true);
    tb->setBlurBackground(false);
    tb->setBackgroundTransparent(true);
}

void MainWindow::setupConfig()
{
    m_config = DConfig::create(QString::fromLatin1(kApplicationId),
                               QString::fromLatin1(kConfigName),
                               QString(),
                               this);
    m_configAvailable = m_config->isValid();
    if (!m_configAvailable) {
        qCWarning(lcConfiguration)
            << "DConfig is unavailable; using built-in defaults. Install the meta file to enable persistence.";
        return;
    }

    connect(m_config, &DConfig::valueChanged,
            this, &MainWindow::applyConfigValue);
    qCInfo(lcConfiguration) << "DConfig initialized with keys" << m_config->keyList();
}

void MainWindow::refreshThemeIcons()
{
    const QIcon appIcon = applicationIcon();
    titlebar()->setIcon(appIcon);
    setWindowIcon(appIcon);
    if (auto *application = qobject_cast<DApplication *>(QCoreApplication::instance())) {
        application->setWindowIcon(appIcon);
        application->setProductIcon(appIcon);
    }

    const QIcon fontIcon = DIconTheme::findQIcon(
        QStringLiteral("preferences-desktop-font"),
        DIconTheme::findQIcon(QStringLiteral("edit")));
    m_fontIcon->setPixmap(fontIcon.pixmap(m_fontIcon->size()));
}

void MainWindow::updateWindowEffects()
{
    auto *windowManager = DWindowManagerHelper::instance();
    const bool blurAvailable = windowManager->hasComposite()
        && windowManager->hasBlurWindow();

    DPlatformTheme *theme = DGuiApplicationHelper::instance()->applicationTheme();
    const int radius = theme ? qMax(0, theme->windowRadius(8)) : 8;

    m_windowBlur->setBlurRectXRadius(radius);
    m_windowBlur->setBlurRectYRadius(radius);
    m_windowBlur->setBlurEnabled(blurAvailable);
    m_windowBlur->setVisible(blurAvailable);
    setEnableBlurWindow(blurAvailable);

    m_fallbackSurface->setVisible(!blurAvailable);
    applySurfaceOpacity(m_sliderOpacity ? m_sliderOpacity->value() : kDefaultOpacity);

    if (blurAvailable) {
        m_windowBlur->lower();
    } else {
        m_fallbackSurface->lower();
    }

    qCInfo(lcApplicationWindow) << "Window effects updated"
                                << "composite" << windowManager->hasComposite()
                                << "blur" << windowManager->hasBlurWindow()
                                << "radius" << radius;
}

void MainWindow::onOpenFile()
{
    if (m_tabManager->isLoading()) {
        return;
    }

    DFileDialog *dlg = new DFileDialog(this);
    dlg->setAcceptMode(QFileDialog::AcceptOpen);
    dlg->setFileMode(QFileDialog::ExistingFile);
    dlg->setNameFilter(tr(
        "All Files (*);;Text Files (*.txt);;Source Files (*.cpp *.h *.py *.js *.qml)"));

    connect(dlg, &DFileDialog::accepted, this, [this, dlg]() {
        const QStringList files = dlg->selectedFiles();
        dlg->deleteLater();
        if (files.isEmpty()) return;

        m_tabManager->addTab(files.first());
    });

    connect(dlg, &DFileDialog::rejected, dlg, &QObject::deleteLater);
    dlg->open();
}

void MainWindow::onTabChanged(const FileTab &tab)
{
    m_codeView->setContent(tab.content);
    updateStatusBar(tab);
}

void MainWindow::onTabsEmpty()
{
    m_codeView->clear();
    clearStatusBar();
}

void MainWindow::onFontSizeChanged(int value)
{
    m_codeView->setFontSize(value);
    if (!m_updatingConfig) {
        setConfigValue(QStringLiteral("fontPixelSize"), value);
    }
}

void MainWindow::onOpacityChanged(int value)
{
    applySurfaceOpacity(value);
    m_opacityLabel->setText(tr("%1%").arg(value));
    if (!m_updatingConfig) {
        setConfigValue(QStringLiteral("backgroundOpacity"), value);
    }
}

void MainWindow::applySurfaceOpacity(int value)
{
    const int alpha = qRound(255.0 * qBound(0, value, 100) / 100.0);
    m_windowBlur->setMaskAlpha(static_cast<quint8>(alpha));
    m_windowBlur->update();

    DPalette palette = DGuiApplicationHelper::instance()->applicationPalette();
    QColor fallbackColor = palette.color(QPalette::Window);
    // 无合成器时保留最低遮罩，避免完全透明导致正文失去对比度。
    fallbackColor.setAlpha(qMax(alpha, 102));
    DPlatformTheme *theme = DGuiApplicationHelper::instance()->applicationTheme();
    const int radius = theme ? qMax(0, theme->windowRadius(8)) : 8;
    m_fallbackSurface->setSurface(fallbackColor, radius);
}

void MainWindow::resizeEvent(QResizeEvent *event)
{
    DMainWindow::resizeEvent(event);
    if (m_windowBlur) {
        m_windowBlur->setGeometry(rect());
        m_windowBlur->lower();
    }
    if (m_fallbackSurface) {
        m_fallbackSurface->setGeometry(rect());
        if (m_fallbackSurface->isVisible()) {
            m_fallbackSurface->lower();
        }
    }
}

void MainWindow::onFileLoadStarted(const QString &filePath)
{
    m_fileLoading = true;
    showLoadingIndicator();
    m_statusLabel->setText(tr("Loading: %1").arg(filePath));
    qCInfo(lcFileLoadWindow) << "Loading started" << filePath;
}

void MainWindow::onFileLoadProgress(const QString &filePath, int progress)
{
    Q_UNUSED(filePath)
    const int boundedProgress = qBound(0, progress, 100);
    m_loadProgress->setValue(
        (boundedProgress * kFileReadProgressMaximum) / 100);
}

void MainWindow::onFileOpened(const FileTab &tab)
{
    DMessageManager::instance()->sendMessage(
        this,
        DIconTheme::findQIcon(
            QStringLiteral("document-open"),
            DIconTheme::findQIcon(QStringLiteral("icon_success"))),
        tr("Opened: %1").arg(tab.fileName));
}

void MainWindow::onFileOpenFailed(const QString &filePath, const QString &errorString)
{
    DMessageManager::instance()->sendMessage(
        this,
        DIconTheme::findQIcon(
            QStringLiteral("dialog-error"),
            DIconTheme::findQIcon(QStringLiteral("icon_warning"))),
        tr("Cannot open %1: %2").arg(filePath, errorString));

    qCWarning(lcFileLoadWindow) << "Cannot open file" << filePath << errorString;

    if (m_tabManager->tabCount() > 0) {
        updateStatusBar(m_tabManager->currentTab());
    } else {
        clearStatusBar();
    }
}

void MainWindow::onFileLoadFinished(const QString &filePath)
{
    Q_UNUSED(filePath)
    m_fileLoading = false;
    tryHideLoadingIndicator();
    qCInfo(lcFileLoadWindow) << "Loading finished" << filePath;
}

void MainWindow::onContentLoadStarted()
{
    m_contentLoading = true;
    m_contentContinuesFileLoad = m_fileLoading;
    showLoadingIndicator();
    m_loadProgress->setValue(
        m_contentContinuesFileLoad ? kFileReadProgressMaximum : 0);
}

void MainWindow::onContentLoadProgress(int progress)
{
    const int boundedProgress = qBound(0, progress, 100);
    if (m_contentContinuesFileLoad) {
        const int contentProgressRange = 100 - kFileReadProgressMaximum;
        m_loadProgress->setValue(
            kFileReadProgressMaximum
            + (boundedProgress * contentProgressRange) / 100);
    } else {
        m_loadProgress->setValue(boundedProgress);
    }
}

void MainWindow::onContentLoadFinished()
{
    m_contentLoading = false;
    m_contentContinuesFileLoad = false;
    tryHideLoadingIndicator();
}

void MainWindow::showLoadingIndicator()
{
    if (m_loadProgress->isVisible()) {
        m_loadProgress->raise();
        return;
    }

    m_loadIndicatorElapsed.restart();
    m_loadProgress->setValue(0);
    m_loadProgress->show();
    m_loadProgress->raise();
    m_loadProgress->start();
}

void MainWindow::tryHideLoadingIndicator()
{
    if (m_fileLoading || m_contentLoading) {
        return;
    }

    m_loadProgress->setValue(100);

    // 小文件也至少短暂显示一次水波提示，避免开始和结束发生在同一帧。
    const int minimumVisibleMs = 300;
    const int elapsed = m_loadIndicatorElapsed.isValid()
        ? static_cast<int>(m_loadIndicatorElapsed.elapsed())
        : minimumVisibleMs;
    const int remaining = qMax(0, minimumVisibleMs - elapsed);
    QTimer::singleShot(remaining, this, [this] {
        if (!m_fileLoading && !m_contentLoading) {
            m_loadProgress->stop();
            m_loadProgress->hide();
        }
    });
}

void MainWindow::updateStatusBar(const FileTab &tab)
{
    m_statusLabel->setText(tr("%1 | %2 lines | %3 KB")
        .arg(tab.filePath)
        .arg(tab.lineCount)
        .arg(tab.fileSize / 1024.0, 0, 'f', 1));
}

void MainWindow::clearStatusBar()
{
    m_statusLabel->setText(tr("No file opened"));
}

void MainWindow::applyConfigValue(const QString &key)
{
    if (m_updatingConfig || !m_configAvailable) {
        return;
    }

    const bool previousUpdatingState = m_updatingConfig;
    m_updatingConfig = true;

    if (key == QLatin1String("windowWidth") || key == QLatin1String("windowHeight")) {
        const int configuredWidth = qBound(
            minimumWidth(),
            m_config->value(QStringLiteral("windowWidth"), kDefaultWidth).toInt(),
            kMaximumWindowWidth);
        const int configuredHeight = qBound(
            minimumHeight(),
            m_config->value(QStringLiteral("windowHeight"), kDefaultHeight).toInt(),
            kMaximumWindowHeight);
        resize(configuredWidth, configuredHeight);
    } else if (key == QLatin1String("fontPixelSize")) {
        const int value = qBound(
            m_spinFont->minimum(),
            m_config->value(key, kDefaultFontSize).toInt(),
            m_spinFont->maximum());
        m_spinFont->setValue(value);
        m_codeView->setFontSize(value);
    } else if (key == QLatin1String("backgroundOpacity")) {
        const int value = qBound(
            m_sliderOpacity->minimum(),
            m_config->value(key, kDefaultOpacity).toInt(),
            m_sliderOpacity->maximum());
        m_sliderOpacity->setValue(value);
        applySurfaceOpacity(value);
        m_opacityLabel->setText(tr("%1%").arg(value));
    }

    m_updatingConfig = previousUpdatingState;
    qCInfo(lcConfiguration) << "Applied configuration change" << key;
}

void MainWindow::setConfigValue(const QString &key, const QVariant &value)
{
    if (!m_configAvailable) {
        return;
    }
    if (m_config->value(key) == value) {
        return;
    }
    m_config->setValue(key, value);
    qCInfo(lcConfiguration) << "Saved configuration" << key << value;
}

void MainWindow::saveWindowState()
{
    const int savedWidth = width();
    const int savedHeight = height();
    const int savedFontSize = m_spinFont->value();
    const int savedOpacity = m_sliderOpacity->value();

    m_updatingConfig = true;
    setConfigValue(QStringLiteral("windowWidth"), savedWidth);
    setConfigValue(QStringLiteral("windowHeight"), savedHeight);
    setConfigValue(QStringLiteral("fontPixelSize"), savedFontSize);
    setConfigValue(QStringLiteral("backgroundOpacity"), savedOpacity);
    m_updatingConfig = false;
}

void MainWindow::restoreWindowState()
{
    const int configuredWidth = m_configAvailable
        ? m_config->value(QStringLiteral("windowWidth"), kDefaultWidth).toInt()
        : kDefaultWidth;
    const int configuredHeight = m_configAvailable
        ? m_config->value(QStringLiteral("windowHeight"), kDefaultHeight).toInt()
        : kDefaultHeight;
    const int fontSize = m_configAvailable
        ? m_config->value(QStringLiteral("fontPixelSize"), kDefaultFontSize).toInt()
        : kDefaultFontSize;
    const int opacity = m_configAvailable
        ? m_config->value(QStringLiteral("backgroundOpacity"), kDefaultOpacity).toInt()
        : kDefaultOpacity;

    m_updatingConfig = true;
    resize(qBound(minimumWidth(), configuredWidth, kMaximumWindowWidth),
           qBound(minimumHeight(), configuredHeight, kMaximumWindowHeight));

    const int boundedFontSize = qBound(m_spinFont->minimum(), fontSize, m_spinFont->maximum());
    m_spinFont->setValue(boundedFontSize);
    m_codeView->setFontSize(boundedFontSize);

    const int boundedOpacity = qBound(
        m_sliderOpacity->minimum(), opacity, m_sliderOpacity->maximum());
    m_sliderOpacity->setValue(boundedOpacity);
    applySurfaceOpacity(boundedOpacity);
    m_opacityLabel->setText(tr("%1%").arg(boundedOpacity));
    m_updatingConfig = false;

    qCInfo(lcConfiguration) << "Window settings restored"
                            << size() << boundedFontSize << boundedOpacity;
}
