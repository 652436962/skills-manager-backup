#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <DMainWindow>
#include <DTabBar>
#include <DSlider>
#include <DSpinBox>
#include <DLabel>
#include <DFontSizeManager>
#include <DWaterProgress>
#include <DBlurEffectWidget>
#include <DConfig>
#include <QElapsedTimer>

#include "tabmanager.h"
#include "codeview.h"

DWIDGET_USE_NAMESPACE

class FallbackSurface;

class MainWindow : public DMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

protected:
    void resizeEvent(QResizeEvent *event) override;

private slots:
    void onOpenFile();
    void onTabChanged(const FileTab &tab);
    void onTabsEmpty();
    void onFontSizeChanged(int value);
    void onOpacityChanged(int value);
    void onFileLoadStarted(const QString &filePath);
    void onFileLoadProgress(const QString &filePath, int progress);
    void onFileOpened(const FileTab &tab);
    void onFileOpenFailed(const QString &filePath, const QString &errorString);
    void onFileLoadFinished(const QString &filePath);
    void onContentLoadStarted();
    void onContentLoadProgress(int progress);
    void onContentLoadFinished();

private:
    void setupUI();
    void setupConnections();
    void setupTitlebar();
    void setupConfig();
    void refreshThemeIcons();
    void updateWindowEffects();
    void applySurfaceOpacity(int value);
    void applyConfigValue(const QString &key);
    void setConfigValue(const QString &key, const QVariant &value);
    void showLoadingIndicator();
    void tryHideLoadingIndicator();
    void updateStatusBar(const FileTab &tab);
    void clearStatusBar();
    void saveWindowState();
    void restoreWindowState();

    DTabBar      *m_tabBar;
    CodeView     *m_codeView;
    QWidget      *m_backgroundSurface;
    FallbackSurface *m_fallbackSurface;
    DBlurEffectWidget *m_windowBlur;
    DSpinBox     *m_spinFont;
    DSlider      *m_sliderOpacity;
    TabManager   *m_tabManager;
    DLabel       *m_statusLabel;
    DLabel       *m_opacityLabel;
    DLabel       *m_fontIcon;
    DWaterProgress *m_loadProgress;
    DTK_CORE_NAMESPACE::DConfig *m_config;
    QElapsedTimer m_loadIndicatorElapsed;
    bool m_fileLoading;
    bool m_contentLoading;
    bool m_contentContinuesFileLoad;
    bool m_updatingConfig;
    bool m_configAvailable;
};

#endif // MAINWINDOW_H
