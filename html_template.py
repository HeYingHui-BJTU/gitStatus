"""
HTML模板生成器 - 紧凑型心流式设计
"""

def get_compact_html_template():
    """返回紧凑型HTML模板字符串"""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{repo_name} - 禾盈慧项目统计</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        html {{ scroll-behavior: smooth; }}
        
        :root {{
            --primary: #667eea;
            --secondary: #764ba2;
            --success: #10b981;
            --danger: #ef4444;
            --dark: #1f2937;
            --light: #f9fafb;
            --border: #e5e7eb;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f3f4f6;
            color: var(--dark);
            line-height: 1.4;
            padding: 16px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        
        /* 紧凑型Header */
        .header {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 24px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .brand {{ font-size: 12px; opacity: 0.9; letter-spacing: 1px; }}
        .header h1 {{ font-size: 28px; margin: 4px 0; }}
        .subtitle {{ font-size: 13px; opacity: 0.85; }}
        
        /* 紧凑型Stats Grid - 强制4列 */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            border-bottom: 1px solid var(--border);
            background: white;
        }}
        
        .stat-card {{
            padding: 16px 12px;
            text-align: center;
            border-right: 1px solid var(--border);
        }}
        
        .stat-card:last-child {{ border-right: none; }}
        
        .stat-card .icon {{ font-size: 24px; margin-bottom: 6px; }}
        .stat-card .label {{ font-size: 11px; color: #6b7280; text-transform: uppercase; margin-bottom: 4px; }}
        .stat-card .value {{ font-size: 24px; font-weight: 700; color: var(--primary); }}
        
        /* 内容区 - 紧凑padding */
        .content {{ padding: 24px 32px; }}
        
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: var(--primary);
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 16px;
        }}
        
        /* Section - 减小间距 */
        .section {{ margin-bottom: 32px; }}
        
        .section-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--border);
        }}
        
        .section-header h2 {{ font-size: 20px; flex: 1; }}
        .section-header .icon {{ font-size: 20px; }}
        
        /* 紧凑型表格 */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        
        .data-table th {{
            background: #f9fafb;
            padding: 8px 12px;
            text-align: left;
            font-size: 11px;
            text-transform: uppercase;
            color: #6b7280;
            font-weight: 600;
        }}
        
        .data-table td {{
            padding: 8px 12px;
            border-top: 1px solid var(--border);
        }}
        
        .data-table tbody tr:hover {{ background: #f9fafb; }}
        
        .badge {{
            display: inline-flex;
            padding: 3px 8px;
            background: var(--primary);
            color: white;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }}
        
        /* 2栏布局 - 图表并列 */
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin: 16px 0;
        }}
        
        .chart-box {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 16px;
        }}
        
        .chart-title {{ font-size: 14px; font-weight: 600; margin-bottom: 12px; color: var(--dark); }}
        
        /* 紧凑型条形图 */
        .bar-chart {{ display: flex; flex-direction: column; gap: 6px; }}
        
        .bar {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .bar-label {{ min-width: 70px; font-size: 12px; color: #4b5563; }}
        
        .bar-track {{
            flex: 1;
            height: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
        }}
        
        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 8px;
            color: white;
            font-size: 11px;
            font-weight: 700;
            min-width: 30px;
        }}
        
        /* 筛选控件 */
        .filter-controls {{
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .filter-controls label {{
            font-size: 12px;
            color: #6b7280;
            font-weight: 600;
        }}
        
        .filter-controls select, .filter-controls input {{
            padding: 6px 12px;
            border: 1px solid var(--border);
            border-radius: 6px;
            font-size: 12px;
            background: white;
            cursor: pointer;
        }}
        
        .filter-controls select:focus, .filter-controls input:focus {{
            outline: none;
            border-color: var(--primary);
        }}
        
        /* 折叠式时间线 */
        .timeline-container {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 16px;
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .timeline {{
            position: relative;
            padding-left: 24px;
        }}
        
        .timeline::before {{
            content: '';
            position: absolute;
            left: 6px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, var(--primary), var(--secondary));
        }}
        
        .timeline-item {{
            position: relative;
            margin-bottom: 12px;
            padding: 8px 12px;
            background: white;
            border-radius: 6px;
            font-size: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}
        
        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -18px;
            top: 12px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: white;
            border: 2px solid var(--primary);
        }}
        
        .timeline-item.merge::before {{ background: var(--success); border-color: var(--success); }}
        
        .timeline-date {{ font-size: 10px; color: #9ca3af; font-weight: 600; }}
        .timeline-author {{ font-weight: 600; color: var(--primary); margin: 2px 0; }}
        .timeline-subject {{ color: #4b5563; line-height: 1.4; }}
        
        /* 打印样式 */
        @media print {{
            body {{ background: white; padding: 0; }}
            .back-link, .timeline-container {{ display: none; }}
            .section {{ page-break-inside: avoid; }}
            .chart-grid {{ grid-template-columns: 1fr; }}
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .chart-grid {{ grid-template-columns: 1fr; }}
            .content {{ padding: 16px; }}
        }}
        
        /* Scrollbar美化 */
        .timeline-container::-webkit-scrollbar {{ width: 6px; }}
        .timeline-container::-webkit-scrollbar-track {{ background: #f1f1f1; }}
        .timeline-container::-webkit-scrollbar-thumb {{ background: var(--primary); border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <div class="brand">禾盈慧 • HEYINGHUI</div>
                <h1>{repo_name}</h1>
                <div class="subtitle">Git 协作统计分析 · {generated_time}</div>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="icon">📝</div>
                <div class="label">总提交数</div>
                <div class="value">{total_commits}</div>
            </div>
            <div class="stat-card">
                <div class="icon">👥</div>
                <div class="label">贡献者</div>
                <div class="value">{total_authors}</div>
            </div>
            <div class="stat-card">
                <div class="icon">📁</div>
                <div class="label">文件总数</div>
                <div class="value">{total_files}</div>
            </div>
            <div class="stat-card">
                <div class="icon">✨</div>
                <div class="label">代码变更</div>
                <div class="value">{total_additions:,}</div>
            </div>
        </div>
        
        <div class="content">
            <a href="../index.html" class="back-link">
                <span>←</span>
                <span>返回总门户</span>
            </a>
            
            <!-- 贡献者排行榜 -->
            <div class="section">
                <div class="section-header">
                    <span class="icon">👥</span>
                    <h2>贡献者排行榜</h2>
                    <button onclick="copyTable()" style="padding: 4px 12px; font-size: 11px; background: var(--primary); color: white; border: none; border-radius: 4px; cursor: pointer;">📋 复制数据</button>
                </div>
                <table class="data-table" id="authorTable">
                    <thead>
                        <tr>
                            <th style="width: 50px;">#</th>
                            <th>贡献者</th>
                            <th style="width: 80px;">提交数</th>
                            <th style="width: 90px;">新增行</th>
                            <th style="width: 90px;">删除行</th>
                            <th style="width: 80px;">文件数</th>
                            <th style="width: 100px;">代码当量</th>
                            <th style="width: 100px;">首次提交</th>
                            <th style="width: 100px;">最近提交</th>
                        </tr>
                    </thead>
                    <tbody>
{authors_rows}
                    </tbody>
                </table>
            </div>
            
            <!-- 提交历史时间线 -->
            <div class="section">
                <div class="section-header">
                    <span class="icon">📅</span>
                    <h2>完整提交时间线</h2>
                    <span style="font-size: 11px; color: #6b7280;">共 {total_commits} 次提交 · 支持筛选排序 · <span style="color: var(--success);">●</span> = Merge</span>
                </div>
                <div class="filter-controls">
                    <label>
                        贡献者:
                        <select id="authorFilter" onchange="filterTimeline()">
                            <option value="all">全部</option>
{author_options}
                        </select>
                    </label>
                    <label>
                        类型:
                        <select id="typeFilter" onchange="filterTimeline()">
                            <option value="all">全部</option>
                            <option value="normal">普通提交</option>
                            <option value="merge">合并提交</option>
                        </select>
                    </label>
                    <label>
                        排序:
                        <select id="sortOrder" onchange="filterTimeline()">
                            <option value="desc">最新优先</option>
                            <option value="asc">最早优先</option>
                        </select>
                    </label>
                    <label>
                        搜索:
                        <input type="text" id="searchText" placeholder="搜索提交信息..." oninput="filterTimeline()" style="width: 200px;">
                    </label>
                </div>
                <div class="timeline-container">
                    <div class="timeline" id="timelineList">
{timeline_items}
                    </div>
                </div>
            </div>
            
            <!-- 活跃时段分析 - 2栏并列 -->
            <div class="section">
                <div class="section-header">
                    <span class="icon">⏰</span>
                    <h2>活跃时段分析</h2>
                </div>
                <div class="chart-grid">
                    <div class="chart-box">
                        <div class="chart-title">按小时分布</div>
                        <div class="bar-chart">
{hour_bars}
                        </div>
                    </div>
                    <div class="chart-box">
                        <div class="chart-title">按星期分布</div>
                        <div class="bar-chart">
{weekday_bars}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 文件类型与月度趋势 - 2栏并列 -->
            <div class="section">
                <div class="section-header">
                    <span class="icon">📊</span>
                    <h2>文件类型 & 提交趋势</h2>
                </div>
                <div class="chart-grid">
                    <div class="chart-box">
                        <div class="chart-title">Top 10 文件类型</div>
                        <div class="bar-chart">
{filetype_bars}
                        </div>
                    </div>
                    <div class="chart-box">
                        <div class="chart-title">最近12个月提交趋势</div>
                        <div class="bar-chart">
{month_bars}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function copyTable() {{
            const table = document.getElementById('authorTable');
            let text = '# 贡献者排行榜\\n\\n';
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {{
                const cells = row.querySelectorAll('td');
                text += `${{cells[0].textContent}} | ${{cells[1].textContent}} | ${{cells[2].textContent}} commits | +${{cells[3].textContent}} | -${{cells[4].textContent}}\\n`;
            }});
            navigator.clipboard.writeText(text).then(() => {{
                alert('✅ 数据已复制到剪贴板！');
            }});
        }}
        
        // 时间线筛选排序
        let allTimelineItems = [];
        
        function initTimeline() {{
            const items = document.querySelectorAll('.timeline-item');
            items.forEach(item => {{
                allTimelineItems.push({{
                    element: item.cloneNode(true),
                    author: item.querySelector('.timeline-author').textContent,
                    subject: item.querySelector('.timeline-subject').textContent,
                    date: item.querySelector('.timeline-date').textContent,
                    isMerge: item.classList.contains('merge'),
                    timestamp: item.querySelector('.timeline-date').textContent
                }});
            }});
        }}
        
        function filterTimeline() {{
            const authorFilter = document.getElementById('authorFilter').value;
            const typeFilter = document.getElementById('typeFilter').value;
            const sortOrder = document.getElementById('sortOrder').value;
            const searchText = document.getElementById('searchText').value.toLowerCase();
            
            let filtered = allTimelineItems.filter(item => {{
                // 作者筛选
                if (authorFilter !== 'all' && item.author !== authorFilter) return false;
                // 类型筛选
                if (typeFilter === 'merge' && !item.isMerge) return false;
                if (typeFilter === 'normal' && item.isMerge) return false;
                // 搜索筛选
                if (searchText && !item.subject.toLowerCase().includes(searchText)) return false;
                return true;
            }});
            
            // 排序
            if (sortOrder === 'asc') {{
                filtered.reverse();
            }}
            
            // 更新显示
            const timeline = document.getElementById('timelineList');
            timeline.innerHTML = '';
            filtered.forEach(item => {{
                timeline.appendChild(item.element.cloneNode(true));
            }});
        }}
        
        // 加载动画
        document.addEventListener('DOMContentLoaded', function() {{
            const rows = document.querySelectorAll('.data-table tbody tr');
            rows.forEach((row, i) => {{
                row.style.opacity = '0';
                row.style.transform = 'translateY(10px)';
                setTimeout(() => {{
                    row.style.transition = 'all 0.3s ease';
                    row.style.opacity = '1';
                    row.style.transform = 'translateY(0)';
                }}, i * 50);
            }});
            
            // 初始化时间线
            initTimeline();
        }});
    </script>
</body>
</html>"""
