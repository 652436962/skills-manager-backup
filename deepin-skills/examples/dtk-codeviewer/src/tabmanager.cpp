#include "tabmanager.h"

#include <QFile>
#include <QFileInfo>
#include <QLoggingCategory>
#include <QTimer>
#include <QSignalBlocker>
#include <limits>

Q_LOGGING_CATEGORY(lcFileLoad, "org.deepin.dtk.codeviewer.fileload")

namespace {
constexpr qint64 kReadChunkSize = 256 * 1024;
}

TabManager::TabManager(DTabBar *tabBar, QObject *parent)
    : QObject(parent)
    , m_tabBar(tabBar)
    , m_loadTimer(new QTimer(this))
    , m_loadingFile(nullptr)
    , m_decoder(QStringDecoder::Utf8)
    , m_loadingSize(0)
    , m_loadingLineCount(1)
{
    m_loadTimer->setInterval(0);
    connect(m_loadTimer, &QTimer::timeout, this, &TabManager::readNextChunk);

    connect(m_tabBar, &DTabBar::currentChanged, this, [this](int index) {
        if (index >= 0 && index < m_tabs.size()) {
            emit tabChanged(m_tabs.at(index));
        }
    });

    connect(m_tabBar, &DTabBar::tabCloseRequested, this, [this](int index) {
        removeTab(index);
    });
}

bool TabManager::addTab(const QString &filePath)
{
    if (isLoading()) {
        qCWarning(lcFileLoad) << "Rejected concurrent file load" << filePath;
        emit fileOpenFailed(filePath, tr("Another file is being loaded."));
        return false;
    }

    QFileInfo requestedFile(filePath);
    const QString normalizedPath = requestedFile.canonicalFilePath().isEmpty()
        ? requestedFile.absoluteFilePath()
        : requestedFile.canonicalFilePath();

    // 已经打开的文件直接切换到对应标签页。
    for (int i = 0; i < m_tabs.size(); ++i) {
        if (m_tabs[i].filePath == normalizedPath) {
            if (m_tabBar->currentIndex() != i) {
                m_tabBar->setCurrentIndex(i);
            } else {
                emit tabChanged(m_tabs[i]);
            }
            emit fileOpened(m_tabs[i]);
            return true;
        }
    }

    m_loadingFile = new QFile(normalizedPath, this);
    if (!m_loadingFile->open(QIODevice::ReadOnly)) {
        const QString errorString = m_loadingFile->errorString();
        qCWarning(lcFileLoad) << "Failed to open file" << normalizedPath << errorString;
        m_loadingFile->deleteLater();
        m_loadingFile = nullptr;
        emit fileOpenFailed(normalizedPath, errorString);
        return false;
    }

    m_loadingPath = normalizedPath;
    m_loadingSize = m_loadingFile->size();
    m_loadingLineCount = 1;
    m_loadingContent.clear();
    m_decoder.resetState();

    // ASCII/UTF-8 文本通常不会超过文件字节数对应的 UTF-16 字符数，预留空间减少扩容。
    if (m_loadingSize > 0 && m_loadingSize <= std::numeric_limits<int>::max()) {
        m_loadingContent.reserve(static_cast<int>(m_loadingSize));
    }

    emit fileLoadStarted(m_loadingPath);
    emit fileLoadProgress(m_loadingPath, 0);
    qCInfo(lcFileLoad) << "Reading file" << m_loadingPath << "bytes" << m_loadingSize;
    m_loadTimer->start();
    return true;
}

void TabManager::readNextChunk()
{
    if (!m_loadingFile) {
        m_loadTimer->stop();
        return;
    }

    const QByteArray chunk = m_loadingFile->read(kReadChunkSize);
    if (chunk.isEmpty() && m_loadingFile->error() != QFileDevice::NoError) {
        failLoading(m_loadingFile->errorString());
        return;
    }

    // 每个小块即时解码，避免文件读完后一次性 UTF-8 转换造成明显卡顿和内存峰值。
    m_loadingContent += m_decoder(chunk);
    m_loadingLineCount += chunk.count('\n');

    const int progress = m_loadingSize <= 0
        ? 100
        : qBound(0, static_cast<int>((m_loadingFile->pos() * 100) / m_loadingSize), 100);
    emit fileLoadProgress(m_loadingPath, progress);

    if (m_loadingFile->atEnd()) {
        completeLoading();
    }
}

void TabManager::completeLoading()
{
    const QString filePath = m_loadingPath;
    const QFileInfo fileInfo(filePath);

    FileTab tab;
    tab.filePath = filePath;
    tab.fileName = fileInfo.fileName();
    tab.content = std::move(m_loadingContent);
    tab.fileSize = fileInfo.size();
    tab.lineCount = static_cast<int>(qMin(
        m_loadingLineCount, static_cast<qint64>(std::numeric_limits<int>::max())));

    emit fileLoadProgress(filePath, 100);
    resetLoadingState();

    m_tabs.append(tab);
    int newIndex = -1;
    {
        const QSignalBlocker blocker(m_tabBar);
        newIndex = m_tabBar->addTab(tab.fileName);
        m_tabBar->setTabToolTip(newIndex, tab.filePath);
        m_tabBar->setCurrentIndex(newIndex);
    }
    emit tabChanged(tab);
    emit fileOpened(tab);
    emit fileLoadFinished(filePath);

    qCInfo(lcFileLoad) << "Opened file" << filePath
                       << "bytes" << tab.fileSize
                       << "lines" << tab.lineCount;
}

void TabManager::failLoading(const QString &errorString)
{
    const QString filePath = m_loadingPath;
    qCWarning(lcFileLoad) << "File loading failed" << filePath << errorString;
    resetLoadingState();
    emit fileOpenFailed(filePath, errorString);
    emit fileLoadFinished(filePath);
}

void TabManager::resetLoadingState()
{
    m_loadTimer->stop();
    if (m_loadingFile) {
        m_loadingFile->close();
        m_loadingFile->deleteLater();
        m_loadingFile = nullptr;
    }
    m_loadingContent.clear();
    m_decoder.resetState();
    m_loadingPath.clear();
    m_loadingSize = 0;
    m_loadingLineCount = 1;
}

void TabManager::removeTab(int index)
{
    if (index < 0 || index >= m_tabs.size()) return;

    QString path = m_tabs[index].filePath;
    m_tabs.removeAt(index);
    m_tabBar->removeTab(index);

    qCInfo(lcFileLoad) << "Closed file" << path;

    if (m_tabs.isEmpty()) {
        emit tabsEmpty();
    }
}

FileTab TabManager::currentTab() const
{
    int idx = m_tabBar->currentIndex();
    if (idx >= 0 && idx < m_tabs.size()) {
        return m_tabs.at(idx);
    }
    return FileTab();
}

int TabManager::tabCount() const
{
    return m_tabs.size();
}

int TabManager::currentIndex() const
{
    return m_tabBar->currentIndex();
}

bool TabManager::isLoading() const
{
    return m_loadingFile != nullptr;
}
