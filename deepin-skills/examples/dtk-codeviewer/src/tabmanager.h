#ifndef TABMANAGER_H
#define TABMANAGER_H

#include <QObject>
#include <QStringDecoder>
#include <DTabBar>

class QFile;
class QTimer;

DWIDGET_USE_NAMESPACE

struct FileTab {
    QString filePath;
    QString fileName;
    QString content;
    int lineCount = 0;
    qint64 fileSize = 0;
};

class TabManager : public QObject
{
    Q_OBJECT

public:
    explicit TabManager(DTabBar *tabBar, QObject *parent = nullptr);

    bool addTab(const QString &filePath);
    void removeTab(int index);
    FileTab currentTab() const;
    int tabCount() const;
    int currentIndex() const;
    bool isLoading() const;

signals:
    void tabChanged(const FileTab &tab);
    void tabsEmpty();
    void fileLoadStarted(const QString &filePath);
    void fileLoadProgress(const QString &filePath, int progress);
    void fileOpened(const FileTab &tab);
    void fileOpenFailed(const QString &filePath, const QString &errorString);
    void fileLoadFinished(const QString &filePath);

private:
    void readNextChunk();
    void completeLoading();
    void failLoading(const QString &errorString);
    void resetLoadingState();

    DTabBar       *m_tabBar;
    QList<FileTab> m_tabs;
    QTimer        *m_loadTimer;
    QFile         *m_loadingFile;
    QString        m_loadingContent;
    QStringDecoder m_decoder;
    QString        m_loadingPath;
    qint64         m_loadingSize;
    qint64         m_loadingLineCount;
};

#endif // TABMANAGER_H
