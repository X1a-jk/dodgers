# -*- coding: utf-8 -*-
"""移动端适配修补：顶栏换行+横幅省略号、表格横向滚动、字号微调、organ-item 防溢出"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
p = r'D:\baseball\index.html'
h = io.open(p, encoding='utf-8-sig').read()

# 1) 1024 断点：侧栏横排时允许换行，october-banner 独占一行并省略号，nav 可收缩
OLD1 = '''            .module-layout { grid-template-columns: 1fr; height: auto; }
            .module-sidebar { max-height: 300px; }
        }'''
NEW1 = '''            .module-layout { grid-template-columns: 1fr; height: auto; }
            .module-sidebar { max-height: 300px; }
            .sidebar { flex-wrap: wrap; row-gap: 4px; }
            .brand { flex-shrink: 0; }
            .october-banner {
                flex: 0 0 100%;
                order: 5;
                margin: 6px 0 2px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                min-width: 0;
            }
            nav { min-width: 0; }
        }'''
assert h.count(OLD1) == 1, 'anchor1 %d' % h.count(OLD1)
h = h.replace(OLD1, NEW1)

# 2) 768 断点：markdown 表格横滑、meta 字号、organ 条目防溢出
OLD2 = '''@media (max-width: 768px) {
            .content { padding: 20px 18px; }
            header { padding: 16px 18px; flex-direction: column; align-items: flex-start; gap: 12px; }
            .dashboard-grid { grid-template-columns: 1fr; }
        }'''
NEW2 = '''@media (max-width: 768px) {
            .content { padding: 20px 18px; }
            header { padding: 16px 18px; flex-direction: column; align-items: flex-start; gap: 12px; }
            .dashboard-grid { grid-template-columns: 1fr; }
            .markdown-body table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
            .card-meta, .meta { font-size: 0.85rem; }
            .organ-item { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .organ-panel { right: 12px; bottom: 70px; max-width: calc(100vw - 24px); }
            .organ-fab { right: 12px; bottom: 14px; }
            h1 { font-size: 1.5rem; }
        }'''
assert h.count(OLD2) == 1, 'anchor2 %d' % h.count(OLD2)
h = h.replace(OLD2, NEW2)

io.open(p, 'w', encoding='utf-8', newline='\n').write(h)
print('PATCH_OK, size', len(h))
