#ifndef CODEVIEW_H
#define CODEVIEW_H

#include <QWidget>

class CodeEditor;
class QTimer;

class CodeView : public QWidget
{
    Q_OBJECT

public:
    explicit CodeView(QWidget *parent = nullptr);

    void setContent(const QString &text);
    void clear();
    void setFontSize(int px);
    void setBackgroundOpacity(int percent);
    int backgroundOpacity() const;
    QString content() const;

signals:
    void contentLoadStarted();
    void contentLoadProgress(int progress);
    void contentLoadFinished();

private:
    void applyEditorFont();
    void insertNextContentChunk();
    void cancelPendingContentLoad(bool emitFinished);

    CodeEditor *m_edit;
    QTimer *m_contentTimer;
    QString m_pendingContent;
    qsizetype m_contentPosition;
    int m_fontSize;
    int m_backgroundOpacity;
};

#endif // CODEVIEW_H
