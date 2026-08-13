#include "codeview.h"

#include <DGuiApplicationHelper>
#include <DPlainTextEdit>
#include <DPlatformTheme>
#include <QApplication>
#include <QFontDatabase>
#include <QPainter>
#include <QTextBlock>
#include <QTextCursor>
#include <QTimer>
#include <QVBoxLayout>

DWIDGET_USE_NAMESPACE
DGUI_USE_NAMESPACE

namespace {
constexpr qsizetype kAsyncContentThreshold = 1024 * 1024;
constexpr qsizetype kContentChunkSize = 64 * 1024;
}

class CodeEditor;

class LineNumberArea : public QWidget
{
public:
    explicit LineNumberArea(CodeEditor *editor);

    QSize sizeHint() const override;

protected:
    void paintEvent(QPaintEvent *event) override;

private:
    CodeEditor *m_editor;
};

class CodeEditor : public DPlainTextEdit
{
public:
    explicit CodeEditor(QWidget *parent = nullptr)
        : DPlainTextEdit(parent)
        , m_lineNumberArea(new LineNumberArea(this))
    {
        setReadOnly(true);
        setUndoRedoEnabled(false);
        setLineWrapMode(QPlainTextEdit::NoWrap);

        connect(this, &QPlainTextEdit::blockCountChanged,
                this, [this](int) { updateLineNumberAreaWidth(); });
        connect(this, &QPlainTextEdit::updateRequest,
                this, [this](const QRect &rect, int dy) { updateLineNumberArea(rect, dy); });

        updateLineNumberAreaWidth();
    }

    int lineNumberAreaWidth() const
    {
        int digits = 1;
        int blocks = qMax(1, blockCount());
        while (blocks >= 10) {
            blocks /= 10;
            ++digits;
        }

        return 12 + fontMetrics().horizontalAdvance(QLatin1Char('9')) * digits;
    }

    void lineNumberAreaPaintEvent(QPaintEvent *event)
    {
        QPainter painter(m_lineNumberArea);
        const QPalette areaPalette = m_lineNumberArea->palette();
        painter.fillRect(event->rect(), areaPalette.color(QPalette::Window));
        painter.setPen(areaPalette.color(QPalette::PlaceholderText));
        painter.setFont(font());

        QTextBlock block = firstVisibleBlock();
        int blockNumber = block.blockNumber();
        int top = qRound(blockBoundingGeometry(block).translated(contentOffset()).top());
        int bottom = top + qRound(blockBoundingRect(block).height());

        while (block.isValid() && top <= event->rect().bottom()) {
            if (block.isVisible() && bottom >= event->rect().top()) {
                painter.drawText(0,
                                 top,
                                 m_lineNumberArea->width() - 6,
                                 fontMetrics().height(),
                                 Qt::AlignRight | Qt::AlignVCenter,
                                 QString::number(blockNumber + 1));
            }

            block = block.next();
            top = bottom;
            bottom = top + qRound(blockBoundingRect(block).height());
            ++blockNumber;
        }
    }

    void refreshLineNumberArea()
    {
        updateLineNumberAreaWidth();
        m_lineNumberArea->update();
    }

    void setBackgroundOpacity(int percent)
    {
        const int boundedPercent = qBound(0, percent, 100);
        const int alpha = qRound(255.0 * boundedPercent / 100.0);

        QPalette editorPalette = QApplication::palette(this);
        QColor baseColor = editorPalette.color(QPalette::Base);
        QColor windowColor = editorPalette.color(QPalette::Window);
        baseColor.setAlpha(alpha);
        windowColor.setAlpha(alpha);
        editorPalette.setColor(QPalette::Base, baseColor);
        editorPalette.setColor(QPalette::Window, windowColor);

        setPalette(editorPalette);
        viewport()->setPalette(editorPalette);
        m_lineNumberArea->setPalette(editorPalette);
        viewport()->update();
        m_lineNumberArea->update();
    }

protected:
    void resizeEvent(QResizeEvent *event) override
    {
        DPlainTextEdit::resizeEvent(event);

        const QRect contents = contentsRect();
        m_lineNumberArea->setGeometry(
            QRect(contents.left(), contents.top(), lineNumberAreaWidth(), contents.height()));
    }

private:
    void updateLineNumberAreaWidth()
    {
        setViewportMargins(lineNumberAreaWidth(), 0, 0, 0);
    }

    void updateLineNumberArea(const QRect &rect, int dy)
    {
        if (dy != 0) {
            m_lineNumberArea->scroll(0, dy);
        } else {
            m_lineNumberArea->update(0, rect.y(), m_lineNumberArea->width(), rect.height());
        }

        if (rect.contains(viewport()->rect())) {
            updateLineNumberAreaWidth();
        }
    }

    LineNumberArea *m_lineNumberArea;

    friend class LineNumberArea;
};

LineNumberArea::LineNumberArea(CodeEditor *editor)
    : QWidget(editor)
    , m_editor(editor)
{
    setAutoFillBackground(false);
}

QSize LineNumberArea::sizeHint() const
{
    return QSize(m_editor->lineNumberAreaWidth(), 0);
}

void LineNumberArea::paintEvent(QPaintEvent *event)
{
    m_editor->lineNumberAreaPaintEvent(event);
}

CodeView::CodeView(QWidget *parent)
    : QWidget(parent)
    , m_edit(new CodeEditor(this))
    , m_contentTimer(new QTimer(this))
    , m_contentPosition(0)
    , m_fontSize(14)
    , m_backgroundOpacity(80)
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(0);
    mainLayout->addWidget(m_edit);

    m_contentTimer->setInterval(0);
    connect(m_contentTimer, &QTimer::timeout, this, &CodeView::insertNextContentChunk);

    auto *guiHelper = DGuiApplicationHelper::instance();
    connect(guiHelper, &DGuiApplicationHelper::fontChanged,
            this, [this] { applyEditorFont(); });
    connect(guiHelper, &DGuiApplicationHelper::applicationPaletteChanged,
            this, [this] { setBackgroundOpacity(m_backgroundOpacity); });

    if (DPlatformTheme *theme = guiHelper->applicationTheme()) {
        connect(theme, &DPlatformTheme::monoFontNameChanged,
                this, [this] { applyEditorFont(); });
    }

    setFontSize(m_fontSize);
    setBackgroundOpacity(m_backgroundOpacity);
}

void CodeView::setContent(const QString &text)
{
    cancelPendingContentLoad(false);

    if (text.size() <= kAsyncContentThreshold) {
        emit contentLoadStarted();
        emit contentLoadProgress(0);
        m_edit->setUpdatesEnabled(false);
        m_edit->setPlainText(text);
        m_edit->moveCursor(QTextCursor::Start);
        m_edit->setUpdatesEnabled(true);
        m_edit->refreshLineNumberArea();
        m_edit->viewport()->update();
        emit contentLoadProgress(100);
        emit contentLoadFinished();
        return;
    }

    // 大文本分批插入文档，让事件循环持续处理绘制和水波动画，避免界面假死。
    m_pendingContent = text;
    m_contentPosition = 0;
    m_edit->clear();
    m_edit->refreshLineNumberArea();
    emit contentLoadStarted();
    emit contentLoadProgress(0);
    m_contentTimer->start();
}

void CodeView::insertNextContentChunk()
{
    if (m_contentPosition >= m_pendingContent.size()) {
        m_contentTimer->stop();
        m_pendingContent.clear();
        m_contentPosition = 0;
        m_edit->moveCursor(QTextCursor::Start);
        m_edit->refreshLineNumberArea();
        m_edit->viewport()->update();
        emit contentLoadProgress(100);
        emit contentLoadFinished();
        return;
    }

    qsizetype length = qMin(kContentChunkSize, m_pendingContent.size() - m_contentPosition);
    const qsizetype endPosition = m_contentPosition + length;
    if (endPosition < m_pendingContent.size()
        && m_pendingContent.at(endPosition - 1).isHighSurrogate()
        && m_pendingContent.at(endPosition).isLowSurrogate()) {
        --length;
    }

    const QString chunk = QStringView(m_pendingContent).mid(m_contentPosition, length).toString();
    QTextCursor cursor(m_edit->document());
    cursor.movePosition(QTextCursor::End);

    m_edit->setUpdatesEnabled(false);
    cursor.insertText(chunk);
    m_edit->setUpdatesEnabled(true);
    m_edit->viewport()->update();

    m_contentPosition += length;
    const int progress = static_cast<int>((m_contentPosition * 100) / m_pendingContent.size());
    emit contentLoadProgress(qBound(0, progress, 100));
}

void CodeView::cancelPendingContentLoad(bool emitFinished)
{
    const bool wasLoading = m_contentTimer->isActive();
    m_contentTimer->stop();
    m_pendingContent.clear();
    m_contentPosition = 0;
    if (wasLoading && emitFinished) {
        emit contentLoadFinished();
    }
}

void CodeView::clear()
{
    cancelPendingContentLoad(true);
    m_edit->clear();
    m_edit->refreshLineNumberArea();
}

void CodeView::setFontSize(int px)
{
    m_fontSize = qMax(1, px);
    applyEditorFont();
}

void CodeView::applyEditorFont()
{
    QFont monoFont = QFontDatabase::systemFont(QFontDatabase::FixedFont);
    if (DPlatformTheme *theme = DGuiApplicationHelper::instance()->applicationTheme()) {
        const QString family = QString::fromUtf8(theme->monoFontName());
        if (!family.isEmpty()) {
            monoFont.setFamily(family);
        }
    }

    monoFont.setPixelSize(m_fontSize);
    monoFont.setStyleHint(QFont::Monospace);
    m_edit->setFont(monoFont);
    m_edit->refreshLineNumberArea();
}

void CodeView::setBackgroundOpacity(int percent)
{
    m_backgroundOpacity = qBound(0, percent, 100);
    m_edit->setBackgroundOpacity(m_backgroundOpacity);
}

int CodeView::backgroundOpacity() const
{
    return m_backgroundOpacity;
}

QString CodeView::content() const
{
    return m_edit->toPlainText();
}
